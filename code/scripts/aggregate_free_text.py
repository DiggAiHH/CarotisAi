"""Nightly Free-Text Aggregator.

Reads all decision_trees since last run, extracts free_text_notes,
clusters via BERTopic (or fallback: Hermes/Ollama LLM-cluster),
writes topic report to memory/anomalies/triage_week<N>.md.

Trigger: Hermes-Skill aggregate-free-text (cron @ 22:30) or manually.
"""

from __future__ import annotations

import argparse
import json
import logging
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


# ---- Strategy A: BERTopic (preferred if installed) -----------------


def _try_bertopic_cluster(texts: list[str]) -> list[dict]:
    try:
        from bertopic import BERTopic
        from sentence_transformers import SentenceTransformer
    except ImportError:
        return []
    embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    topic_model = BERTopic(
        embedding_model=embedder,
        language="german",
        min_topic_size=3,
        calculate_probabilities=False,
    )
    topics, _ = topic_model.fit_transform(texts)
    info = topic_model.get_topic_info()
    clusters = []
    for _, row in info.iterrows():
        if row["Topic"] == -1:
            continue  # noise
        clusters.append(
            {
                "topic_id": int(row["Topic"]),
                "size": int(row["Count"]),
                "keywords": [w for w, _ in topic_model.get_topic(row["Topic"])[:5]],
                "example_indices": [
                    i for i, t in enumerate(topics) if t == row["Topic"]
                ][:3],
            }
        )
    return clusters


# ---- Strategy B: Hermes/Ollama LLM-Cluster (Fallback) ------------------


def _try_hermes_cluster(texts: list[str]) -> list[dict]:
    """LLM-based cluster analysis via local Ollama endpoint."""
    import requests

    prompt = (
        "Du bist Cluster-Analyst. Hier sind Notizen von Radiologen "
        "nach Befundungen. Gruppiere sie in 3-7 Topics. Pro Topic: "
        "kurzes Label, Schlüsselwörter, Anzahl. NIEMALS einzelne "
        "Snippets zitieren — nur Aggregat. Antworte als JSON-Liste.\n\n"
        + "\n---\n".join(f"[{i}] {t}" for i, t in enumerate(texts[:200]))
    )
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "nous-hermes-3-llama-3.1",
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=120,
        )
        r.raise_for_status()
        return json.loads(r.json()["response"])
    except Exception as e:
        logger.warning("hermes_cluster_failed: %s", e)
        return []


# ---- Strategy C: Simple keyword fallback ----------------------------


def _keyword_fallback(texts: list[str]) -> list[dict]:
    """Simple keyword-based grouping when nothing else works."""
    words = []
    for t in texts:
        words.extend(w.lower() for w in t.split() if len(w) > 4)
    most_common = Counter(words).most_common(10)
    return [
        {
            "topic_id": i,
            "size": sum(1 for t in texts if kw in t.lower()),
            "keywords": [kw],
        }
        for i, (kw, _) in enumerate(most_common[:5])
        if sum(1 for t in texts if kw in t.lower()) >= 2
    ]


# ---- Main aggregation ------------------------------------------------


def aggregate(
    db_path: Path,
    output_dir: Path,
    since_days: int = 7,
) -> Path | None:
    """Main run. Returns path to triage report."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=since_days)

    conn = sqlite3.connect(db_path)
    cur = conn.execute(
        "SELECT data_json FROM decision_trees WHERE captured_at >= ?",
        (cutoff.isoformat(),),
    )
    notes: list[str] = []
    for (data_json,) in cur:
        data = json.loads(data_json)
        text = (data.get("reasoning") or {}).get("free_text_notes")
        if text and len(text.strip()) > 5:
            notes.append(text.strip())
    conn.close()

    if len(notes) < 5:
        logger.info("not_enough_notes count=%d skipping", len(notes))
        return None

    # Try BERTopic, then Hermes, then keyword fallback
    clusters = (
        _try_bertopic_cluster(notes)
        or _try_hermes_cluster(notes)
        or _keyword_fallback(notes)
    )
    if not clusters:
        logger.warning("no_clustering_method_available")
        return None

    # Write report
    week_iso = datetime.now(timezone.utc).strftime("%Y-W%V")
    report_path = output_dir / f"triage_{week_iso}.md"
    output_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Wöchentlicher Triage-Report — {week_iso}",
        "",
        f"**Stand:** {datetime.now(timezone.utc).isoformat()}",
        f"**Notes analysiert:** {len(notes)}",
        f"**Cluster gefunden:** {len(clusters)}",
        "",
        "## Top-Clusters",
        "",
    ]
    for c in clusters:
        label = c.get("topic_id", c.get("label", "?"))
        size = c.get("size", "?")
        lines.append(f"### Topic {label} — Size {size}")
        kw = c.get("keywords", [])
        if kw:
            lines.append(f"**Keywords:** {', '.join(kw)}")
        lines.append("")
    lines.extend(
        [
            "## Vorschläge zur Schema-Erweiterung",
            "",
            "_Lou reviewed wöchentlich. Approved Topics werden zu neuen "
            "deciding_feature-Werten in schemas/decision_tree.schema.json._",
            "",
            "## Compliance-Hinweis",
            "",
            "Dieser Report enthält KEINE einzelnen Note-Snippets — nur "
            "Topic-Cluster. Original-Notes verbleiben in der lokalen "
            "Audit-DB des Klinikums.",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("triage_report_written path=%s", report_path)
    return report_path


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db", type=Path, default=Path("data/db/carotis.db"))
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("memory/anomalies"),
    )
    p.add_argument("--since-days", type=int, default=7)
    args = p.parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    result = aggregate(args.db, args.output_dir, args.since_days)
    if result is None:
        print("No report generated (not enough notes or clustering failed).")
        return 0
    print(f"Report: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
