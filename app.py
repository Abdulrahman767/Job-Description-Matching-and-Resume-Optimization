import streamlit as st
from analyzer import extract_text_from_uploaded_file, contextual_similarity, extract_experience_level, job_market_insights, calculate_cv_compatibility, extract_keywords

st.title("Resume-Job Compatibility Checker")

# Job Description and Resume Upload
job_description_input = st.text_area("Job Description", "Enter the job description here.")
uploaded_file = st.file_uploader("Upload your Resume", type=["pdf", "docx", "txt"])

if st.button("Analyze"):
    # Extract text from the uploaded resume
    if uploaded_file:
        resume_text = extract_text_from_uploaded_file(uploaded_file)
    else:
        st.error("Please upload a resume file.")
        resume_text = ""

    if resume_text:
        # Analyze contextual similarity and experience level
        job_description = job_description_input
        resume_keywords = extract_keywords(resume_text)
        job_keywords = extract_keywords(job_description)

        compatibility_score = calculate_cv_compatibility(job_keywords, resume_keywords)
        similarity_analysis = contextual_similarity(job_description, resume_text)
        experience_level = extract_experience_level(resume_text)
        market_insights = job_market_insights(job_description)

        # Display the results without rewriting the job description and resume text
        st.subheader("Analysis Results")
        st.markdown(f"### Compatibility Score: {compatibility_score}%")
        st.markdown(f"### Contextual Analysis:\n{similarity_analysis}")
        st.markdown(f"### Extracted Experience Level: {experience_level}")
        st.markdown(f"### Job Market Insights:\n{market_insights}")
