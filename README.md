# FBO Pitch Deck Generator

A web app that lets anyone fill out a form and instantly download a completed real estate investor pitch deck (PPTX).

Built with [Streamlit](https://streamlit.io) — free to host publicly.

---

## Files

| File | Purpose |
|------|---------|
| `app.py` | The Streamlit web app (all form UI) |
| `generate_deck.py` | PPTX generation logic |
| `template.pptx` | Your pitch deck template — **do not rename** |
| `requirements.txt` | Python dependencies |

---

## Deploying to Streamlit Cloud (Free — ~5 min)

### Step 1 — Push to GitHub

1. Create a free account at [github.com](https://github.com) if you don't have one
2. Create a new **public** repository (e.g. `fbo-pitch-deck`)
3. Upload all four files (`app.py`, `generate_deck.py`, `requirements.txt`, `template.pptx`) to the repo

   The easiest way: click **Add file → Upload files** in the GitHub interface

### Step 2 — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **New app**
3. Select your repo, branch (`main`), and set **Main file path** to `app.py`
4. Click **Deploy**

Streamlit Cloud will install dependencies and launch the app. You'll get a public URL like:
```
https://your-app-name.streamlit.app
```

Share that link with anyone — no login required to use it.

---

## Running Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## How It Works

1. The user fills in each section of the form (organized by slide)
2. Financial totals are calculated automatically in real time (visible in the sidebar)
3. Clicking **Generate Deck** fills all placeholder text in `template.pptx` and streams the result as a download
4. The downloaded `.pptx` can be opened in PowerPoint or imported into Google Slides

---

## Customizing the Template

If you update `template.pptx`, make sure the placeholder text strings in the template exactly match what `generate_deck.py` expects. The key placeholders are listed at the top of `generate_deck.py` in the `replacements` dictionary.

---

## Questions?

Contact the team at the info on the contact slide of the deck.
