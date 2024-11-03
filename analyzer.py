import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from langchain_groq import ChatGroq
import docx
import fitz

# Ensure nltk data is downloaded
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

# Initialize stopwords and lemmatizer
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


llm = ChatGroq(
    temperature=0,
    groq_api_key='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',
    model_name="llama-3.1-70b-versatile"
)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    tokens = [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]
    return " ".join(tokens)

def extract_keywords(text):
    prompt = f"Extract key skills and responsibilities from the following text:\n\n{text}"
    response = llm.invoke(prompt)
    skills = re.findall(r'\d+\.\s*(.*?)\n', response.content)
    return [skill.strip().lower() for skill in skills if skill.strip()]

def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = sum(a ** 2 for a in vec_a) ** 0.5
    magnitude_b = sum(b ** 2 for b in vec_b) ** 0.5
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    return dot_product / (magnitude_a * magnitude_b)

def contextual_similarity(job_description, resume_text):
    # Preprocess the texts
    job_description = preprocess_text(job_description)
    resume_text = preprocess_text(resume_text)

    # Vectorization
    all_words = list(set(job_description.split() + resume_text.split()))
    job_vector = [job_description.split().count(word) for word in all_words]
    resume_vector = [resume_text.split().count(word) for word in all_words]

    # Compute cosine similarity
    sim_score = cosine_similarity(job_vector, resume_vector)
    return f"Contextual similarity score: {sim_score * 100:.2f}%"

def extract_experience_level(resume_text):
    prompt = f"Identify the experience level (e.g., entry, mid, senior) based on this resume:\n\n{resume_text}"
    response = llm.invoke(prompt)
    return response.content.strip()

def job_market_insights(role):
    prompt = f"Provide insights or trends related to the job market for the role: {role}. Include in-demand skills and common career paths."
    response = llm.invoke(prompt)
    return response.content.strip()

def calculate_cv_compatibility(job_description, resume_text):
    prompt = f"Evaluate how compatible the following resume is with the job description:\n\nJob Description: {job_description}\n\nResume: {resume_text}\n\nProvide a compatibility rating from 0 to 100."
    response = llm.invoke(prompt)
    return response.content.strip()

def extract_text_from_uploaded_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        return text

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text

    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    return ""
