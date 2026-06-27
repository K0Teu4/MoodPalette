# MoodPalette

Minimal local web application that converts text descriptions into color palettes.

No cloud services. No external APIs. Everything runs locally in Python.

---

## Features

* Text → palette generation
* Deterministic results
* Local FastAPI server
* 5-color palette preview
* Copy individual HEX values
* Copy all HEX values
* Palette history (localStorage)
* Download palette as PNG (800×200)
* Dark UI
* No external requests
* No CDN dependencies

---

## Preview

Add screenshot:

```text
screenshots/preview.png
```

---

## Project structure

```text
moodpalette/
├── moodpalette/
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py
│   ├── generator.py
│   └── export.py
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── data/
│   └── palettes.jsonl
│
├── tests/
│   └── test_generator.py
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Installation

Clone repository:

```bash
git clone https://github.com/USERNAME/MoodPalette.git

cd MoodPalette
```

Create virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run

Run locally:

```bash
python -m moodpalette
```

or:

```bash
moodpalette
```

Open:

```text
http://localhost:8080
```

---

## Example inputs

```text
night
forest
melancholic autumn evening
cyberpunk
summer sunrise
freedom
```

---

## Planned improvements

* Share links (?q=...)
* Harmony schemes
* Creativity slider
* sentence-transformers integration
* Larger palette dataset
* Automated tests

---

## License

MIT
