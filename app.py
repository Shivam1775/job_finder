import streamlit as st
from utills import extract_text_from_pdf, predict_category, get_jobs

st.set_page_config(
    page_title="ResumeAI · Job Finder",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: linear-gradient(145deg, #6b8f4e 0%, #4a6e35 35%, #3a5a28 70%, #5a7a40 100%);
    min-height: 100vh;
    font-family: 'DM Sans', sans-serif;
    color: #e8f0dc;
}

.block-container {
    padding: 2.5rem 3rem;
    max-width: 1100px;
}

#MainMenu, footer, header { visibility: hidden; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 10px; }

# /* ── Hero Form Panel ── */
# .hero-panel {
#     background: linear-gradient(135deg, rgba(60,85,38,0.85) 0%, rgba(45,65,28,0.92) 100%);
#     backdrop-filter: blur(20px);
#     -webkit-backdrop-filter: blur(20px);
#     border: 1px solid rgba(180,220,130,0.15);
#     border-radius: 24px;
#     padding: 44px 48px 40px;
#     margin-bottom: 28px;
#     box-shadow: 0 20px 60px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.08);
# }

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(32px, 4.5vw, 48px);
    font-weight: 400;
    color: #e8f0dc;
    line-height: 1.1;
    margin-bottom: 4px;
    letter-spacing: -0.01em;
}

.hero-title em {
    font-style: italic;
    color: #b8e068;
    display: block;
}

.hero-sub {
    font-size: 13px;
    color: rgba(200,225,165,0.5);
    margin-bottom: 36px;
    margin-top: 10px;
    font-weight: 300;
}

/* ── Streamlit input overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(180,220,130,0.3) !important;
    border-radius: 0 !important;
    color: #e8f0dc !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 4px !important;
    transition: border-color 0.2s !important;
    box-shadow: none !important;
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
    color: rgba(200,225,165,0.4) !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-bottom-color: #b8e068 !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label {
    color: rgba(200,225,165,0.6) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSelectbox"] > div > div {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(180,220,130,0.3) !important;
    border-radius: 0 !important;
    color: #e8f0dc !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 4px !important;
    box-shadow: none !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px dashed rgba(180,220,130,0.3) !important;
    border-radius: 12px !important;
    padding: 8px !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(184,224,104,0.6) !important;
}

[data-testid="stFileUploader"] label {
    color: rgba(200,225,165,0.45) !important;
    font-size: 13px !important;
}

/* ── Button ── */
.stButton > button {
    background: #b8e068 !important;
    color: #2a3e18 !important;
    border: none !important;
    border-radius: 100px !important;
    padding: 0 32px !important;
    height: 46px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: auto !important;
    min-width: 120px !important;
}

.stButton > button:hover {
    background: #caed7e !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(184,224,104,0.4) !important;
}

/* ── Welcome Banner ── */
.welcome-banner {
    background: rgba(40,60,25,0.7);
    border: 1px solid rgba(180,220,130,0.18);
    border-left: 3px solid #b8e068;
    border-radius: 16px;
    padding: 20px 26px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    backdrop-filter: blur(10px);
}

.welcome-name {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: #e8f0dc;
    margin-bottom: 4px;
}

.welcome-meta {
    font-size: 13px;
    color: rgba(200,225,165,0.5);
    line-height: 1.6;
}

.welcome-category {
    background: rgba(184,224,104,0.15);
    border: 1px solid rgba(184,224,104,0.35);
    color: #b8e068;
    border-radius: 100px;
    padding: 6px 18px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    white-space: nowrap;
}

/* ── Skill chips ── */
.skills-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 0 0 28px;
}

.skill-chip {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(180,220,130,0.2);
    border-radius: 100px;
    padding: 4px 14px;
    font-size: 12px;
    color: rgba(200,225,165,0.7);
    font-weight: 400;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: rgba(180,220,130,0.12);
    margin: 32px 0;
}

/* ── Jobs outer panel ── */
.jobs-panel {
    background: rgba(160,195,105,0.22);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(180,220,130,0.2);
    border-radius: 24px;
    padding: 28px 28px 32px;
}

.jobs-panel-label {
    font-size: 14px;
    font-weight: 500;
    color: rgba(200,225,165,0.65);
    margin-bottom: 20px;
    letter-spacing: 0.01em;
}

/* ── Job cards grid ── */
.jobs-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
}

.job-card {
    background: linear-gradient(145deg, #2e4a1e, #253d18);
    border: 1px solid rgba(180,220,130,0.12);
    border-radius: 16px;
    padding: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
}

.job-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.3);
    border-color: rgba(184,224,104,0.25);
}

.job-card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 16px;
    font-weight: 400;
    color: #e8f0dc;
    margin-bottom: 4px;
    line-height: 1.3;
}

.job-card-company {
    font-size: 12px;
    color: rgba(200,225,165,0.5);
    margin-bottom: 14px;
    font-weight: 300;
}

.job-card-divider {
    height: 1px;
    background: rgba(180,220,130,0.1);
    margin-bottom: 12px;
}

.job-card-meta {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
    margin-bottom: 14px;
}

.job-card-meta-item {
    font-size: 11px;
    color: rgba(200,225,165,0.55);
    line-height: 1.4;
}

.job-card-meta-label {
    font-size: 10px;
    color: rgba(200,225,165,0.35);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 2px;
}

.job-card-footer {
    display: flex;
    justify-content: flex-end;
    margin-top: 4px;
}

.job-apply-btn {
    display: inline-block;
    background: #b8e068;
    color: #2a3e18 !important;
    text-decoration: none !important;
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
    transition: background 0.2s, transform 0.2s;
    letter-spacing: 0.02em;
}

.job-apply-btn:hover {
    background: #caed7e;
    transform: translateY(-1px);
    text-decoration: none !important;
}

.job-no-link {
    font-size: 11px;
    color: rgba(200,225,165,0.2);
    padding: 6px 0;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: rgba(40,60,25,0.6) !important;
    border: 1px solid rgba(180,220,130,0.2) !important;
    border-radius: 12px !important;
    color: rgba(200,225,165,0.7) !important;
}

.stSpinner > div { color: #b8e068 !important; }

[data-testid="stExpander"] {
    background: rgba(40,60,25,0.5) !important;
    border: 1px solid rgba(180,220,130,0.15) !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary {
    color: rgba(200,225,165,0.55) !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* result count tag */
.result-count-tag {
    display: inline-block;
    background: rgba(184,224,104,0.12);
    border: 1px solid rgba(184,224,104,0.25);
    border-radius: 100px;
    padding: 3px 12px;
    font-size: 11px;
    color: #b8e068;
    font-weight: 500;
    letter-spacing: 0.04em;
    margin-left: 10px;
    vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HERO PANEL
# ─────────────────────────────────────────────
st.markdown('<div class="hero-panel">', unsafe_allow_html=True)
st.markdown("""
<div class="hero-title">
    Find work that fits
    <em>who you are.</em>
</div>
<div class="hero-sub">Fill in your profile and upload your resume — our ML model finds the best matching live jobs from Naukri.</div>
""", unsafe_allow_html=True)



col1, col2 = st.columns([1, 1], gap="large")

with col1:
    name         = st.text_input("Your Name", placeholder="e.g. Arjun Sharma")
    experience   = st.selectbox("Years of Experience", ["Fresher (0 yr)", "1 – 2 yrs", "3 – 5 yrs", "6 – 9 yrs", "10+ yrs"])
    preferred_location = st.text_input("Preferred Location", placeholder="e.g. Bangalore, Remote")
    skills_input = st.text_input("Key Skills", placeholder="e.g. Python, Machine Learning, SQL")

with col2:
    summary = st.text_area(
        "Professional Summary (optional)",
        placeholder="Your domain focus, key achievements, or target role...",
        height=168
    )

st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], label_visibility="collapsed")

st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)



if uploaded_file:
    col_btn, col_sp = st.columns([1, 5])
    with col_btn:
        analyze = st.button("Analyze & Find Jobs")
else:
    analyze = False
    st.info("Upload your PDF resume above to get started.")

st.markdown('</div>', unsafe_allow_html=True)  # close hero-panel


# ─────────────────────────────────────────────
#  MAIN LOGIC
# ─────────────────────────────────────────────
if uploaded_file and analyze:

    with st.spinner("Reading your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)


        profile_context = ""
        if skills_input.strip():
            profile_context += f" skills: {skills_input}"
        if summary.strip():
            profile_context += f" {summary}"
        if experience:
            profile_context += f" experience: {experience}"

        enriched_text = resume_text + " " + profile_context
        category      = predict_category(enriched_text)

        

    # ── Welcome Banner ──
    display_name = name.strip() if name.strip() else "there"
    skills_list  = [s.strip() for s in skills_input.split(",") if s.strip()]
    loc_display  = preferred_location.strip() if preferred_location.strip() else "India"
    summary_clip = (summary.strip()[:80] + "...") if len(summary.strip()) > 80 else summary.strip()

    summary_clean = (summary or "").strip()

    if summary_clean:
        summary_clip = summary_clean[:80] + "..." if len(summary_clean) > 80 else summary_clean
        summary_html = f"&nbsp;&nbsp;·&nbsp;&nbsp;{summary_clip}"
    else:
        summary_html = ""

    welcome_html = f"""
    <div class="welcome-banner">
        <div>
            <div class="welcome-name">Hello, {display_name}.</div>
            <div class="welcome-meta">
                {experience}&nbsp;&nbsp;·&nbsp;&nbsp;{loc_display}{summary_html}
            </div>
        </div>
        <div class="welcome-category">{category}</div>
    </div>
    """

    st.markdown(welcome_html, unsafe_allow_html=True)
    if skills_list:
        chips_html = '<div class="skills-row">'
        for s in skills_list:
            chips_html += f'<span class="skill-chip">{s}</span>'
        chips_html += '</div>'
        st.markdown(chips_html, unsafe_allow_html=True)

    with st.expander("View extracted resume text"):
        st.text(resume_text[:3000] + ("..." if len(resume_text) > 3000 else ""))

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Fetch jobs ──
    search_query = category
    if preferred_location.strip():
        search_query += f" {preferred_location.strip()}"

    with st.spinner(f"Fetching live listings for {category}..."):
        jobs = get_jobs(search_query)

    if not jobs:
        st.warning("No listings found. Try a different resume or adjust your profile.")
        st.stop()

    # ── Jobs panel ──
    st.markdown(f"""
    <div class="jobs-panel">
        <div class="jobs-panel-label">
            Recommended Openings
            <span class="result-count-tag">{len(jobs)} found · {category}</span>
        </div>
        <div class="jobs-grid">
    """, unsafe_allow_html=True)

    cards_html = ""
    for job in jobs:
        title   = job.get("title")      or "Not Available"
        company = job.get("company")    or "Not Available"
        loc     = job.get("location")   or "India"
        exp     = job.get("experience") or "—"
        salary  = job.get("salary")     or "Not Disclosed"
        url     = job.get("url")

        apply_html = (
            f'<a class="job-apply-btn" href="{url}" target="_blank" rel="noopener noreferrer">Apply</a>'
            if url else
            '<span class="job-no-link">No link</span>'
        )

        cards_html += f"""
        <div class="job-card">
            <div class="job-card-title">{title}</div>
            <div class="job-card-company">{company}</div>
            <div class="job-card-divider"></div>
            <div class="job-card-meta">
                <div>
                    <div class="job-card-meta-label">Location</div>
                    <div class="job-card-meta-item">{loc}</div>
                </div>
                <div>
                    <div class="job-card-meta-label">Experience</div>
                    <div class="job-card-meta-item">{exp}</div>
                </div>
                <div>
                    <div class="job-card-meta-label">Salary</div>
                    <div class="job-card-meta-item">{salary}</div>
                </div>
            </div>
            <div class="job-card-footer">{apply_html}</div>
        </div>
        """

    st.markdown(cards_html + "</div></div>", unsafe_allow_html=True)