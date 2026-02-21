import streamlit as st
from utills import extract_text_from_pdf, predict_category, get_jobs

st.set_page_config(
    page_title="ResumeAI · Job Finder",
    page_icon="🎯",
    layout="wide"
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — Dark Professional Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #0a0d14;
    color: #e2e8f0;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    padding: 2.5rem 3rem;
    max-width: 1200px;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero ── */
.hero {
    padding: 56px 0 40px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 40px;
}

.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 100px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 800;
    line-height: 1.1;
    color: #f8fafc;
    margin-bottom: 16px;
}

.hero-title span {
    background: linear-gradient(135deg, #6366f1 0%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-size: 16px;
    color: #64748b;
    max-width: 520px;
    line-height: 1.7;
}

/* ── Upload Panel ── */
.upload-panel {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 32px;
}

.panel-label {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 14px;
}

/* Streamlit file uploader tweak */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(99,102,241,0.35) !important;
    border-radius: 14px !important;
    padding: 8px !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(99,102,241,0.65) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #38bdf8) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0 32px !important;
    height: 52px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.45) !important;
}

/* ── Category Badge ── */
.category-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: rgba(56,189,248,0.1);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 12px;
    padding: 12px 20px;
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: #38bdf8;
    margin: 24px 0 32px;
}

/* ── Section Header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #f1f5f9;
}

.section-count {
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    color: #818cf8;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 13px;
    font-weight: 600;
}

/* ── Job Grid ── */
.jobs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 20px;
    margin-top: 8px;
}

/* ── Job Card ── */
.job-card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
}

.job-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6366f1, #38bdf8);
    opacity: 0;
    transition: opacity 0.25s;
}

.job-card:hover {
    border-color: rgba(99,102,241,0.3);
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.4);
}

.job-card:hover::before { opacity: 1; }

.job-title {
    font-family: 'Syne', sans-serif;
    font-size: 17px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 6px;
    line-height: 1.3;
}

.job-company {
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 16px;
    font-weight: 500;
}

.job-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 20px;
}

.tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 12px;
    color: #94a3b8;
    font-weight: 400;
}

.tag-icon { font-size: 11px; }

.job-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 16px;
    border-top: 1px solid rgba(255,255,255,0.06);
}

.posted-time {
    font-size: 12px;
    color: #475569;
}

.apply-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    color: #818cf8 !important;
    text-decoration: none !important;
    border-radius: 10px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
    transition: all 0.2s;
    cursor: pointer;
}

.apply-btn:hover {
    background: rgba(99,102,241,0.28);
    border-color: rgba(99,102,241,0.6);
    color: #a5b4fc !important;
    text-decoration: none !important;
}

.no-link-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #475569;
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 12px;
}

/* ── Divider ── */
.styled-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.4), transparent);
    margin: 32px 0;
}

/* ── Spinner text ── */
.stSpinner > div { color: #818cf8 !important; }

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🎯 AI-Powered · India Jobs</div>
    <div class="hero-title">Find Jobs That Match<br><span>Your Resume</span></div>
    <div class="hero-sub">Upload your resume and our ML model instantly identifies your skill category and pulls live job listings from Naukri.com.</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  UPLOAD PANEL
# ─────────────────────────────────────────────
st.markdown('<div class="upload-panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-label">Upload Resume</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    label="Drop your PDF resume here",
    type=["pdf"],
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ANALYZE BUTTON
# ─────────────────────────────────────────────
if uploaded_file:
    col_btn, col_space = st.columns([1, 3])
    with col_btn:
        analyze = st.button("🔍 Analyze & Find Jobs")
else:
    analyze = False
    st.info("👆 Upload your PDF resume above to get started.")


# ─────────────────────────────────────────────
#  MAIN LOGIC
# ─────────────────────────────────────────────
if uploaded_file and analyze:

    # Step 1 — Predict category
    with st.spinner("Analyzing your resume with ML model..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        category = predict_category(resume_text)

    st.markdown(f"""
    <div class="category-badge">
        🎯 Detected Category &nbsp;—&nbsp; {category}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="styled-divider"></div>', unsafe_allow_html=True)

    # Step 2 — Fetch jobs
    with st.spinner(f"Fetching live jobs for '{category}' from Naukri..."):
        jobs = get_jobs(category)

    if not jobs:
        st.warning("No jobs found for this category. Try uploading a different resume.")
        st.stop()

    # Section header
    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">🇮🇳 Recommended Jobs</div>
        <div class="section-count">{len(jobs)} found</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Inject card CSS separately (plain string, no f-string to avoid brace conflicts) ──
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

.jg-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    margin-top: 8px;
}

.jc {
    background: linear-gradient(145deg, #131c2e, #0f172a);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 20px;
    padding: 26px 24px 20px;
    position: relative;
    overflow: hidden;
    transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
    font-family: 'DM Sans', sans-serif;
}

.jc::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #38bdf8, #6366f1);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
    border-radius: 20px 20px 0 0;
}

.jc::after {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 140px; height: 140px;
    background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
    pointer-events: none;
}

@keyframes shimmer {
    0%   { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

.jc:hover {
    transform: translateY(-6px);
    border-color: rgba(99,102,241,0.45);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 0 1px rgba(99,102,241,0.1);
}

.jc-header { margin-bottom: 14px; }

.jc-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 800;
    color: #f1f5f9;
    margin: 0 0 5px;
    line-height: 1.3;
    letter-spacing: -0.01em;
}

.jc-company {
    font-size: 13px;
    color: #64748b;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 5px;
}

.jc-company-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #6366f1;
    display: inline-block;
    flex-shrink: 0;
}

.jc-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    margin: 14px 0 18px;
}

.jc-tag {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 11px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 500;
    border: 1px solid transparent;
    white-space: nowrap;
}

.jc-tag.loc {
    background: rgba(56,189,248,0.08);
    border-color: rgba(56,189,248,0.2);
    color: #7dd3fc;
}

.jc-tag.exp {
    background: rgba(167,139,250,0.08);
    border-color: rgba(167,139,250,0.2);
    color: #c4b5fd;
}

.jc-tag.sal {
    background: rgba(52,211,153,0.08);
    border-color: rgba(52,211,153,0.2);
    color: #6ee7b7;
}

.jc-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 15px;
    border-top: 1px solid rgba(255,255,255,0.05);
}

.jc-posted {
    font-size: 11px;
    color: #475569;
    letter-spacing: 0.02em;
}

.jc-apply {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: linear-gradient(135deg, rgba(99,102,241,0.22), rgba(56,189,248,0.15));
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc;
    text-decoration: none;
    border-radius: 10px;
    padding: 8px 18px;
    font-size: 13px;
    font-weight: 700;
    font-family: 'Syne', sans-serif;
    letter-spacing: 0.01em;
    transition: all 0.2s ease;
    cursor: pointer;
}

.jc-apply:hover {
    background: linear-gradient(135deg, rgba(99,102,241,0.4), rgba(56,189,248,0.3));
    border-color: rgba(99,102,241,0.7);
    color: #e0e7ff;
    text-decoration: none;
    box-shadow: 0 4px 18px rgba(99,102,241,0.35);
    transform: translateY(-1px);
}

.jc-noapply {
    font-size: 11px;
    color: #334155;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px;
    padding: 7px 12px;
}
</style>
""", unsafe_allow_html=True)

    # ── Build cards HTML using string concatenation (no f-string for CSS) ──
    cards_html = '<div class="jg-grid">'

    for job in jobs:
        title   = job.get("title")   or "Not Available"
        company = job.get("company") or "Not Available"
        loc     = job.get("location") or "India"
        exp     = job.get("experience") or "Not Mentioned"
        salary  = job.get("salary") or "Not Disclosed"
        posted  = job.get("posted") or "Recently Posted"
        url     = job.get("url") or None

        if url:
            apply_html = (
                '<a class="jc-apply" href="' + url + '" target="_blank" rel="noopener noreferrer">'
                'Apply Now &#8599;</a>'
            )
        else:
            apply_html = '<span class="jc-noapply">Link Unavailable</span>'

        cards_html += (
            '<div class="jc">'
                '<div class="jc-header">'
                    '<div class="jc-title">' + title + '</div>'
                    '<div class="jc-company">'
                        '<span class="jc-company-dot"></span>'
                        + company +
                    '</div>'
                '</div>'
                '<div class="jc-tags">'
                    '<span class="jc-tag loc">&#128205; ' + loc + '</span>'
                    '<span class="jc-tag exp">&#128188; ' + exp + '</span>'
                    '<span class="jc-tag sal">&#128176; ' + salary + '</span>'
                '</div>'
                '<div class="jc-footer">'
                    '<span class="jc-posted">&#128336; ' + posted + '</span>'
                    + apply_html +
                '</div>'
            '</div>'
        )

    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)