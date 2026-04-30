# Carotis-AI Public Landing Page

Statische Landing Page für `carotis.diggai.de`.

## Quick Deploy

```bash
cd code/website
# Netlify CLI (optional)
npx netlify deploy --prod --dir=.
```

## DNS Setup

1. Netlify-Site erstellen, dieses Verzeichnis als Deploy-Root setzen.
2. Custom Domain hinzufügen: `carotis.diggai.de`.
3. Bei Domain-Provider: CNAME-Record `carotis.diggai.de` → `<netlify-subdomain>.netlify.app`.
4. Netlify prüft DNS und stellt TLS-Zertifikat (Let's Encrypt) automatisch aus.

## Lokaler Test

```bash
cd code/website
python -m http.server 8080
# oder
npx serve .
```

Lighthouse-Check:
```bash
npx lighthouse http://localhost:8080 --preset=desktop --output=html
```

## Struktur

- `index.html` — Einzige Seite (Hero, Problem, Lösung, Trust, Team, FAQ, Kontakt, Footer)
- `style.css` — Eigenes CSS (kein Build-Step)
- `assets/` — SVG-Logo + 3 App-Screenshot-Placeholdern
- `netlify.toml` — Headers (CSP, Cache, Security)

## Hinweise

- Kein Build-Step nötig. Pure HTML + CSS.
- Keine externen Tracker (DSGVO-konform).
- Mailto-Link auf Lou (Engineering-Lead).
- Demo-Link auf `app.carotis.diggai.de` (Token-Gated).
