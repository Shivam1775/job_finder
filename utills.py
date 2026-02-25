import pickle
import pdfplumber
from apify_client import ApifyClient
import re
import nltk
from nltk.stem import WordNetLemmatizer
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# ── NLTK packages (runs once) ──────────────────────────────────────────────
nltk_packages = ["stopwords", "punkt", "wordnet", "omw-1.4"]
for pkg in nltk_packages:
    try:
        nltk.data.find(pkg)
    except LookupError:
        nltk.download(pkg, quiet=True)

# ── API Token ──────────────────────────────────────────────────────────────

# NEW — checks .env first, falls back to st.secrets for cloud
APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")

if not APIFY_TOKEN:
    try:
        APIFY_TOKEN = st.secrets["APIFY_API_TOKEN"]
    except Exception:
        APIFY_TOKEN = None

# ── Load ML artefacts ──────────────────────────────────────────────────────
try:
    clf              = pickle.load(open("knc.pkl", "rb"))
    tfidf            = pickle.load(open("tfidf.pkl", "rb"))
    category_mapping = pickle.load(open("mapping.pkl", "rb"))
except FileNotFoundError as e:
    st.error(f"Model file missing: {e}. Make sure knc.pkl, tfidf.pkl and mapping.pkl are present.")
    st.stop()


# ── PDF extraction ─────────────────────────────────────────────────────────
def extract_text_from_pdf(uploaded_file):
    """Extract plain text from every page of an uploaded PDF."""
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception as e:
        st.error(f"Could not read PDF: {e}")
        return ""

    if not text.strip():
        st.warning("The PDF appears to have no extractable text (it may be a scanned image). "
                   "Try a text-based PDF for best results.")
    return text


# ── Text cleaning & preprocessing ─────────────────────────────────────────
def _clean_text(text: str) -> str:
    """Lower-case, strip noise, tokenise, remove stopwords, lemmatise."""
    # Remove URLs, hashtags, mentions, punctuation, non-ASCII, extra spaces
    text = re.sub(r'http\S+\s', ' ', text)
    text = re.sub(r'#\S+',      ' ', text)
    text = re.sub(r'@\S+',      ' ', text)
    text = re.sub(r'[%s]' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', text)
    text = re.sub(r'[^\x00-\x7f]', ' ', text)
    text = re.sub(r'\s+',           ' ', text).strip()

    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    tokens    = tokenizer.tokenize(text)

    stop_words = set(nltk.corpus.stopwords.words('english'))
    tokens     = [t.lower() for t in tokens if t.lower() not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens     = [lemmatizer.lemmatize(t) for t in tokens]

    return ' '.join(tokens)


def build_enriched_text(resume_text: str, skills: str = "",
                         experience: str = "", summary: str = "") -> str:
    """
    Combine resume text with structured profile fields so the TF-IDF
    vectoriser has richer, more targeted signal.

    Skills are repeated intentionally to boost their weight in the
    TF-IDF feature space — a simple but effective trick.
    """
    parts = [resume_text]

    if skills.strip():
        # Repeat skills 3x to increase term frequency weight
        skill_tokens = skills.strip()
        parts.append(skill_tokens)
        parts.append(skill_tokens)
        parts.append(skill_tokens)

    if summary.strip():
        parts.append(summary.strip())

    if experience.strip():
        parts.append(experience.strip())

    return " ".join(parts)

    


# ── Category prediction ────────────────────────────────────────────────────
def predict_category(enriched_text: str) -> str:
    """
    Clean the enriched text, vectorise, and return the predicted
    job category label.
    """
    if not enriched_text.strip():
        return "Unknown"


    

    cleaned    = _clean_text(enriched_text)
    features   = tfidf.transform([cleaned])
    pred_id    = clf.predict(features)[0]
    category   = category_mapping.get(pred_id, "Unknown")
    return category







# ── Job fetching ───────────────────────────────────────────────────────────
def get_jobs(keyword: str) -> list:
    """
    Fetch up to 50 live job listings from Naukri via Apify scraper.
    Returns a list of normalised job dicts.
    """
    if not APIFY_TOKEN:
        st.error("Apify API token not found. Set APIFY_API_TOKEN in your .env or Streamlit secrets.")
        return []

    try:
        client    = ApifyClient(APIFY_TOKEN)
        run_input = {"keyword": keyword, "maxJobs": 50}
        run       = client.actor("muhammetakkurtt~naukri-job-scraper").call(run_input=run_input)

        jobs = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            job_url = (
                item.get("jdURL")
                or item.get("url")
                or item.get("jdUrl")
                or item.get("applyUrl")
                or item.get("link")
            )
            # Validate URL
            if job_url and not isinstance(job_url, str):
                job_url = None
            if job_url and not job_url.startswith("http"):
                job_url = None

            jobs.append({
                "title":      item.get("title")                  or "Not Available",
                "company":    item.get("companyName")            or "Not Available",
                "location":   item.get("location")               or "India",
                "experience": item.get("experience")             or "Not Mentioned",
                "salary":     item.get("salary")                 or "Not Disclosed",
                "posted":     item.get("footerPlaceholderLabel") or "Recently Posted",
                "url":        job_url,
            })

        return jobs

    except Exception as e:
        st.error(f"Failed to fetch jobs: {e}")
        return []