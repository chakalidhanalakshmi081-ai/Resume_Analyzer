from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Extract text from PDF
def extract_text_from_pdf(pdf_path):

    text = ""

    reader = PdfReader(pdf_path)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files.get("resume")

    if not resume:
        return "Please upload a resume."

    resume_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(resume_path)

    # Extract resume text
    resume_text = extract_text_from_pdf(resume_path)

    # Convert text to lowercase
    text = resume_text.lower()


    # Skills to search
    skill_list = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "flask",
        "django",
        "machine learning",
        "data science",
        "c++",
        "git"
    ]


    # Find skills
    skills = []

    for skill in skill_list:

        if skill in text:
            skills.append(skill.title())


    # Calculate score
    score = min(len(skills) * 8, 100)


    # Job role recommendation
    if "python" in text and ("flask" in text or "django" in text):
        job_role = "Python Developer"

    elif "java" in text:
        job_role = "Java Developer"

    elif "machine learning" in text or "data science" in text:
        job_role = "Data Scientist"

    elif "javascript" in text:
        job_role = "Web Developer"

    else:
        job_role = "Software Developer"


    # Job role score
    role_score = min(score + 10, 100)


    return render_template(
        "result.html",
        score=score,
        skills=skills,
        job_role=job_role,
        role_score=role_score
    )


if __name__ == "__main__":
    app.run(debug=True)