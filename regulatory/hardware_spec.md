# Hardware-Spezifikation — Carotis-AI Edge-Server

> Stand: 2026-04-29 | Phase: P1-Vorbereitung (blockiert bis Rohde-Go)
> Verantwortlich: Lou (Laith Alshdaifat) | Review: Prof. Rohde, Klinikum-Datenschutz

---

## 1. ZWECK

Der Edge-Server ist die **einzige Hardware**, auf der Carotis-AI Patientendaten verarbeitet. Er steht physisch im Klinikum Dortmund (oder Sarah Hospital, Jordanien in P5) und hat keinen Internet-Zugang. Alle Inferenz, Anonymisierung und Audit-Trail-Erfassung findet lokal statt.

---

## 2. MINIMALE ANFORDERUNGEN

| Komponente | Minimum | Empfohlen | Begründung |
|-----------|---------|-----------|------------|
| **CPU** | 8 Cores / 16 Threads | 16 Cores / 32 Threads | ONNX Runtime parallelisiert über Threads; 16 Cores für < 2s Inferenz pro Slice |
| **GPU** | NVIDIA RTX A4000 (16 GB) | NVIDIA RTX A5000 (24 GB) oder A6000 (48 GB) | MFSD-UNet Forward-Pass auf GPU; 16 GB für 512x512 Batch-Size 4 |
| **RAM** | 32 GB DDR4 ECC | 64 GB DDR4 ECC | PyTorch + ONNX + DICOM-Cache + OS; ECC für Stabilität |
| **Storage** | 1 TB NVMe SSD | 2 TB NVMe SSD (LUKS-verschlüsselt) | Modelle (500 MB), SQLite (wachsend), DICOM-Cache; LUKS per BDSG |
| **Netzwerk** | 1 Gbps Ethernet | 10 Gbps Ethernet (nur Intranet) | DICOM-Transfer zum PVS; kein Internet-Anschluss |
| **Betriebssystem** | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS | Long-term Support, Container-Runtime (Docker/Podman) |
| **Virtualisierung** | Docker | Docker + systemd-nspawn (Backup) | Alle Services containerisiert; Rootless-Container empfohlen |

---

## 3. HARDWARE-OPTIONEN (Preisspanne)

### Option A: Budget (ca. 4.000–5.000 €)
- **Workstation:** Dell Precision T3680 oder HP Z2 Tower
- **CPU:** Intel Core i9-14900K (24 Cores) oder AMD Ryzen 9 7950X
- **GPU:** NVIDIA RTX A4000 16 GB
- **RAM:** 64 GB DDR5 ECC
- **Storage:** 2x 1 TB NVMe SSD (RAID 1, LUKS)
- **Geeignet für:** Entwicklung, Pilot-Phase, < 50 Befundungen/Tag

### Option B: Mittelklasse (ca. 8.000–10.000 €) ⭐ EMPFOHLEN
- **Workstation:** Dell Precision 7865 Tower oder HP Z4/Z6
- **CPU:** AMD Threadripper PRO 5965WX (24 Cores) oder Intel Xeon W7-3465X
- **GPU:** NVIDIA RTX A5000 24 GB
- **RAM:** 128 GB DDR5 ECC
- **Storage:** 2x 2 TB NVMe SSD (RAID 1, LUKS) + 4 TB HDD (Backup)
- **Geeignet für:** Produktion, 50–200 Befundungen/Tag, Multi-User

### Option C: Premium (ca. 15.000–20.000 €)
- **Server:** Supermicro SYS-751GE-TNR oder Dell PowerEdge R760xa
- **CPU:** 2x Intel Xeon Gold 6430 (64 Cores total)
- **GPU:** NVIDIA RTX A6000 48 GB oder 2x A5000
- **RAM:** 256 GB DDR5 ECC
- **Storage:** 4x 2 TB NVMe SSD (RAID 10, LUKS) + 8 TB HDD (Backup)
- **Geeignet für:** Forschung, > 200 Befundungen/Tag, zukünftige Multi-Modell-Inferenz

---

## 4. NETZWERK-TOPOLOGIE

```
┌─────────────────────────────────────────────────────────────┐
│                    KLINIKUM DORTMUND                         │
│                    (Intranet, kein Internet)                 │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐     ┌──────────┐   │
│  │  PVS / KIS   │◄────►│  FHIR-Bridge │◄───►│ Firewall │   │
│  │  (Medico*)   │      │  (HL7→FHIR)  │     │ (strict) │   │
│  └──────────────┘      └──────┬───────┘     └────┬─────┘   │
│                               │                   │         │
│                        ┌──────┴──────┐            │         │
│                        │ Edge-Server │◄───────────┘         │
│                        │ Carotis-AI  │  (nur 443/80)        │
│                        │             │                      │
│                        │ ┌─────────┐ │                      │
│                        │ │ ONNX RT │ │                      │
│                        │ │ SQLite  │ │                      │
│                        │ │ Docker  │ │                      │
│                        │ └─────────┘ │                      │
│                        └─────────────┘                      │
│                               │                             │
│                        ┌──────┴──────┐                      │
│                        │   NAS-Box   │  (Nightly Backup)    │
│                        │  (Air-Gap)  │                      │
│                        └─────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

*Medico, Orbis, or similar KIS used at Klinikum Dortmund.

### Netzwerk-Regeln
- **Kein Internet:** Edge-Server hat keinen Default-Gateway.
- **Nur eingehend:** Port 443 (HTTPS API), Port 80 (Health-Check Redirect).
- **Kein SSH von außen:** Administrativer Zugriff nur über lokale Konsole oder Klinikum-Jumphost.
- **FHIR-Bridge:** Einweg-Synchronisation (nur lesend aus PVS, nie schreibend).

---

## 5. BACKUP-STRATEGIE

| Ebene | Methode | Frequenz | Retention | Verantwortlich |
|-------|---------|----------|-----------|----------------|
| **SQLite Audit-DB** | `sqlite3 .backup` + rsync zu NAS | Stündlich | 10 Jahre | Automatisiert |
| **DICOM-Cache** | Kein Backup — ephemer | — | 24h | Automatisiert (tmpfs) |
| **Modell-Dateien** | SHA-256 Checksummen + USB-Stick (verschlüsselt) | Bei Update | Alle Versionen | Lou |
| **System-Konfig** | Ansible-Playbook in Git | Bei Änderung | Git-History | Lou |
| **Gesamt-Image** | Clonezilla Disk-Image zu NAS | Monatlich | 3 Monate | Klinikum-IT |

---
## 6. SICHERHEIT & COMPLIANCE

- **LUKS-Verschlüsselung:** Full-Disk-Encryption für alle SSDs. Key auf TPM 2.0 Chip.
- **Secure Boot:** Aktiviert, nur signierte Kernel.
- **Container-Sicherheit:** Non-root User für alle Services, read-only Filesystem wo möglich.
- **Physische Sicherheit:** Rack im Serverraum Klinikum, Zugangskontrolle, Überwachungskamera.
- **Stromversorgung:** Online-UPS (≥ 1500 VA), Autonomie ≥ 30 Minuten.

---

## 7. LEBENSZYKLUS

| Phase | Zeitraum | Hardware-Zustand |
|-------|----------|------------------|
| **P1–P2** (Setup) | 2026-Q3 | Option A oder B beschafft |
| **P3–P4** (Training) | 2026-Q4 – 2027-Q2 | Volle Nutzung, Monitoring |
| **P5–P6** (Multi-Site) | 2027-Q3 – 2028-Q1 | Zweite identische Hardware für Sarah Hospital |
| **P7+** (Maintenance) | 2028+ | Ersatzbeschaffung alle 5 Jahre |

---

## 8. OFFENE PUNKTE

- [ ] Klinikum-IT: Rack-Platz + Stromanschluss bestätigen
- [ ] Klinikum-IT: VLAN für Edge-Server einrichten
- [ ] Klinikum-Datenschutz: LUKS-Key-Eskrow-Verfahren klären
- [ ] Lou: Ansible-Playbook für automatisierte Installation

---

*Letztes Update: 2026-04-29 | Nächste Review: nach Rohde-Go*
