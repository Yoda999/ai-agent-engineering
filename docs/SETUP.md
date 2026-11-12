# Setup: van nul naar week 1

Dit is de eenmalige inrichting. Reken 2-3 uur, verspreid over twee dagen. Daarna
kost de dagelijkse routine enkele minuten.

## 1. Wat je nodig hebt

| Onderdeel | Minimum | Advies |
|---|---|---|
| Laptop | 8 GB RAM, 20 GB vrij | 16 GB RAM |
| Python | 3.11+ | 3.12 of 3.13 |
| Git | recent | recent |
| Docker | Engine + Compose | Engine + Compose |
| GitHub | account | branch protection + Actions |
| VPS | 2 GB RAM | 4 GB RAM, 2 vCPU (Hetzner CX22/CX32) |
| API-toegang | één provider | DeepSeek of OpenAI + lokaal via Ollama |
| Budget | EUR 10-30/maand | VPS + tokens; eval-kosten zijn meestal klein |

Je hebt **geen** GPU nodig. Voor de meeste oefeningen volstaan API-calls; Ollama
is handig voor offline experimenten.

## 2. Deze repo klaarzetten

```bash
git clone https://github.com/Yoda999/ai-agent-engineering.git
cd ai-agent-engineering
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

aae doctor
aae plan
aae today
```

Werkt `aae` niet meteen:

```bash
PYTHONPATH=src python3 -m aae doctor
```

De voortgang staat standaard in `.aae/progress.db` in de map waar je `aae`
uitvoert (gitignored). Wil je hem ergens anders:

```bash
export AAE_HOME="$HOME/.local/share/aae"
```

## 3. Boeken en naslag

De PDF's staan in:

```text
/home/yoda/Documents/Boeken/AI Boeken/pdf
```

De leeskaart verwijst naar gedrukte paginanummers. Maak eventueel een tekstversie
voor snelle zoekopdrachten (niet committen; auteursrecht):

```bash
mkdir -p ~/boeken-tekst
for f in "/home/yoda/Documents/Boeken/AI Boeken/pdf"/*.pdf; do
  pdftotext -layout "$f" "$HOME/boeken-tekst/$(basename "${f%.pdf}").txt"
done
```

## 4. API-keys en providers

Maak een `.env` in je **projectrepo** (nooit in deze curriculumrepo):

```bash
# .env.example
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
DEEPSEEK_API_KEY=
OLLAMA_BASE_URL=http://localhost:11434/v1
```

Laad lokaal:

```bash
set -a; source .env; set +a
```

Providers:

| Provider | Gebruik | Opmerking |
|---|---|---|
| DeepSeek | dagelijks oefenen | OpenAI-compatibel; stel base_url in |
| OpenAI | kwaliteit en tooling | duurder; gebruik kleine modellen voor tests |
| Anthropic | Claude-modellen | sterke tool-use; let op kosten |
| Ollama | offline en privacy | lokaal, langzamer; ideaal voor unit-tests |

PydanticAI is provider-agnostisch. Configureer het model expliciet, bijvoorbeeld
met een OpenAI-compatibele provider voor DeepSeek of Ollama, en lees de actuele
documentatie voor de exacte constructor.

**Regels:**

- Geen key in code, prompt, commit, image of log.
- Gebruik aparte keys per project en rotatie na een lek.
- Zet een harde uitgavenlimiet bij je provider.
- Test met `TestModel`; echte calls alleen in integratie- of evaltests.

## 5. GitHub

### 5.1 Nieuwe repo

Deze repo is de basis. Maak hem aan op GitHub (leeg, zonder README) en push:

```bash
git init
git add .
git commit -m "feat: 24-weeks agent engineering curriculum"
git branch -M main
git remote add origin https://github.com/Yoda999/ai-agent-engineering.git
git push -u origin main
```

### 5.2 Token

De bestaande credential-helper leest een PAT uit:

```text
/home/yoda/Documents/deepseek-harness/pat/pat.txt
```

Regel 1 moet een **geldige** GitHub-token zijn (klassiek of fine-grained met
`repo`-rechten). Vervang hem als hij verlopen is:

```bash
# voorbeeld: vervang regel 1, laat andere regels staan
python3 - <<'PY'
from pathlib import Path
p = Path.home() / "Documents/deepseek-harness/pat/pat.txt"
lines = p.read_text().splitlines()
lines[0] = "ghp_VERVANG_MIJ"
p.write_text("\n".join(lines) + "\n")
PY
```

Of zet tijdelijk een token in je shell:

```bash
export GITHUB_TOKEN=...
git -c credential.helper='!f() { echo "username=x-access-token"; echo "password=$GITHUB_TOKEN"; }; f' push
```

Maak een fine-grained token met:

- **Repository access:** alleen de repo's die je nodig hebt.
- **Permissions:** Contents (read/write), Actions (read), Packages (read/write)
  en Metadata (read).
- **Expiry:** 90 dagen; zet een reminder.

### 5.3 Branch protection

Op GitHub: Settings -> Branches -> protect `main`:

- [ ] Require a pull request before merging (ook voor jezelf).
- [ ] Require status checks: de CI-job.
- [ ] Require conversation resolution.
- [ ] Geen force pushes.

Zo dwing je dezelfde discipline af als in de rest van het programma.

### 5.4 Actions en GHCR

- Settings -> Actions -> General: laat GitHub Actions toe.
- Workflows krijgen `permissions: contents: read, packages: write`.
- Images gaan naar `ghcr.io/<user>/<repo>:<sha>`.
- Nooit `latest` als enige tag; gebruik `sha` of een versienummer.

## 6. VPS

### 6.1 Basis

```bash
# als root, eenmalig
adduser deploy
usermod -aG sudo,docker deploy
mkdir -p /home/deploy/.ssh
# zet je publieke sleutel in authorized_keys
```

`/etc/ssh/sshd_config`:

```text
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

Firewall:

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow in on tailscale0
ufw enable
```

### 6.2 Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
tailscale ip -4
```

Dashboard en healthchecks blijven privé; alleen via Tailscale of localhost.

### 6.3 Docker en secrets

```bash
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker
```

Secrets op de VPS:

```bash
sudo install -d -m 700 -o deploy -g deploy /home/deploy/secrets
sudo -u deploy sh -c 'umask 077; cat > /home/deploy/secrets/agent.env'
```

Bestandsinhoud:

```text
OPENAI_API_KEY=...
AGENT_DASHBOARD_TOKEN=...
```

Nooit in git, nooit in het image, nooit in een Docker-label.

### 6.4 Back-up en restore

- Maak dagelijks een back-up van de SQLite-database en `.env`-loze configuratie.
- Versleutel de back-up (age of GPG) en bewaar hem buiten de VPS.
- Test een restore **voordat** je hem nodig hebt. Dat is een fase-4-gate.

## 7. Eerste week checklist

- [ ] `aae doctor` is groen (Docker mag ontbreken als je lokaal begint).
- [ ] `aae today` toont week 1.
- [ ] `agent-lab-01` bestaat, met een eerste commit.
- [ ] CI draait en is groen.
- [ ] Je hebt 60 minuten per dag geblokkeerd.
- [ ] Je hebt een provider-key met een uitgavenlimiet.
- [ ] Je weet waar je boeken staan en hebt de leeskaart geopend.

## 8. Problemen oplossen

| Symptoom | Oorzaak | Oplossing |
|---|---|---|
| `aae: command not found` | niet geinstalleerd | `pip install -e .` of `PYTHONPATH=src` |
| `Kan de curriculumroot niet vinden` | verkeerde map | `cd` naar de repo of zet `AAE_ROOT` |
| `401` bij GitHub | PAT verlopen | nieuwe token in `pat.txt` |
| `ModuleNotFoundError: yaml` | dependency ontbreekt | `pip install pyyaml` |
| Tests willen netwerk | echte client in unit-test | injecteer een fake/TestModel |
| Hoge kosten | retries of grote context | UsageLimits, caching, kleiner model |
| Container start niet | env of poort | `docker compose logs`, healthcheck |
| Geen verbinding met VPS | firewall/Tailscale | `tailscale status`, `ufw status` |

## 9. Dagelijkse routine

```bash
aae today
aae cards
# 15 min lezen, 25 min bouwen
aae exam --week N     # op testdagen
aae log 60 --note "buildstap X"
aae gate --week N     # op zaterdag
```
