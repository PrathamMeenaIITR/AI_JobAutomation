# LinkedIn Easy Apply (Bitwarden‑enabled)

A small, open‑source Python tool that automatically:

* logs into LinkedIn using credentials stored in **Bitwarden**
* searches for jobs matching a list of keywords & locations
* detects “Easy Apply” opportunities
* evaluates the job description against your résumé (via `job_analyzer`)
* records every application attempt (title, URL, status, match % …) in a **Google Sheet**

All secrets are never hard‑coded – they are pulled at runtime from a Bitwarden vault, keeping your passwords and Google service‑account keys safe.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How it works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

---

## Features

| ✅ | Description |
|---|-------------|
| **Secure secret handling** | Bitwarden vault supplies LinkedIn login and Google Sheets service‑account JSON. |
| **Playwright‑driven UI** | Headed (or headless) Chromium automation, no Selenium headaches. |
| **Job‑fit analysis** | Uses `job_analyzer.analyze_job_fit` to compare job description with résumé skills. |
| **Google Sheets logger** | Every attempt is appended to a sheet (timestamp, company, title, URL, status, match %…). |
| **Customizable search** | Edit `KEYWORDS` and `LOCATIONS` in `linkedin_easy_apply_bw.py`. |
| **Modular** | Separate modules for credential fetching, logging, and analysis. |

---

## Prerequisites

| Tool | Why? |
|------|------|
| **Python 3.9+** | Core language. |
| **Playwright** | Browser automation (`pip install playwright && playwright install`). |
| **Bitwarden CLI (`bw`)** | Securely retrieve credentials at runtime. |
| **Google service‑account JSON** | Needed for Sheets API (stored as a Bitwarden secure note). |
| **A Google Sheet** | Destination for logs – create one and note its ID. |
| **Resume files** | `resume.txt` (plain‑text version) and `resume_pratham_meena.pdf` (optional attachment). |

---

## Installation

```bash
# Clone the repo
git clone https://github.com/<YOUR_USERNAME>/linkedin-easy-apply-bw.git
cd linkedin-easy-apply-bw

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
