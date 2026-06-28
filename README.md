# MoodPalette

Minimal local web application that converts text descriptions into color palettes.

Everything runs locally.

No cloud services.

No external APIs.

No CDN dependencies.

---

## Features

* Text → palette generation
* Deterministic palette generation
* Local FastAPI server
* Semantic palette matching
* Palette harmony engine
* Monochromatic mode
* Complementary mode
* Triadic mode
* Creativity control slider
* Palette preview
* Copy individual HEX values
* Copy all HEX values
* Palette history (`localStorage`)
* Download PNG export (800×200)
* Share links
* URL state restoration
* Dark UI
* No external network requests

---

## Preview

Place screenshot here:

```text
screenshots/preview.png
```

---

## Project structure

```text
MoodPalette/
├── moodpalette/
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py
│   ├── generator.py
│   ├── palette.py
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
├── README.md
├── LICENSE
└── .gitignore
```

---

## Installation

Clone repository:

```bash
git clone https://github.com/K0Teu4/MoodPalette.git

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

Install requirements:

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

Open browser:

```text
http://localhost:8080
```

---

## Example prompts

```text
night
forest
winter night
cyberpunk
summer sunrise
freedom
melancholic autumn evening
```

---

## Current functionality checklist

```text
[x] Local server
[x] Text → palette generation
[x] Semantic palette selection
[x] Palette harmony engine
[x] History
[x] Copy HEX
[x] Copy all HEX
[x] Download PNG
[x] Share links
[x] URL restoration
[x] Creativity slider
```

---

## Planned improvements

* sentence-transformers integration
* larger palette dataset
* automated tests
* visual refinements
* accessibility improvements

---

## License

MIT License
