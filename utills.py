import pickle
import pdfplumber
from apify_client import ApifyClient
import re
import nltk
from nltk.stem import WordNetLemmatizer
import os
from dotenv import load_dotenv
load_dotenv()

# ---- API Token (stored here, not in UI) ----
try:
    APIFY_TOKEN = st.secrets["APIFY_API_TOKEN"]
except:
    # fallback for local .env
    APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")


# Load model and vectorizer
clf = pickle.load(open("knc.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))
category_mapping = pickle.load(open("mapping.pkl", "rb"))


# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    return text


# Text cleaning & preprocessing
def resumeKeywords(text):
    cleanText = re.sub(r'http\S+\s', ' ', text)
    cleanText = re.sub(r'#\S+\s', ' ', cleanText)
    cleanText = re.sub(r'@\S+', '  ', cleanText)
    cleanText = re.sub(r'[%s]' % re.escape(r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText)
    cleanText = cleanText.strip()

    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(cleanText)

    words = [word.lower() for word in tokens]

    stop_words = nltk.corpus.stopwords.words('english')
    words_filtered = [word for word in words if word not in stop_words]

    wn = WordNetLemmatizer()
    lemm_text = [wn.lemmatize(word) for word in words_filtered]

    return ' '.join(lemm_text)


# Predict resume category
def predict_category(resume_text):
    cleaned = resumeKeywords(resume_text)
    features = tfidf.transform([cleaned])
    prediction_id = clf.predict(features)[0]
    category = category_mapping.get(prediction_id, "Unknown")
    return category


# Extract best available job URL from Apify item
def _extract_url(item):
    """Try multiple known Apify field names to get a valid job URL."""
    candidates = [
        item.get("url"),
        item.get("jdUrl"),
        item.get("job_url"),
        item.get("applyUrl"),
        item.get("link"),
        item.get("href"),
    ]
    for url in candidates:
        if url and isinstance(url, str) and url.startswith("http"):
            return url
    return None


# Fetch jobs from Apify Naukri scraper
def get_jobs(keyword):
    client = ApifyClient(APIFY_TOKEN)

    run_input = {
        "keyword": keyword,
        "maxJobs": 50
    }

    run = client.actor("muhammetakkurtt~naukri-job-scraper").call(run_input=run_input)

    jobs = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        job_url = item.get("jdURL") 

        jobs.append({
            

            "title":      item.get("title")                  or "Not Available",
            "company":    item.get("companyName")            or "Not Available",
            "location":   item.get("location")               or "India",
            "experience": item.get("experience")             or "Not Mentioned",
            "salary":     item.get("salary")                 or "Not Disclosed",
            "posted":     item.get("footerPlaceholderLabel") or "Recently Posted",
            "url":        job_url,  # kept as None intentionally — checked before use
        })

    return jobs