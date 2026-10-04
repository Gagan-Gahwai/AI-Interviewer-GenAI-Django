from pypdf import PdfReader
import os 
import json
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from pypdf import PdfReader
from xhtml2pdf import pisa
from io import BytesIO

load_dotenv()

client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)

def extract_resume_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def generate_interview_report(resume, self_description, job_description):

    prompt = f"""
You are an AI interview preparation assistant.

Analyze the candidate based on:

RESUME:
{resume}

SELF DESCRIPTION:
{self_description}

JOB DESCRIPTION:
{job_description}

Return ONLY valid JSON.

JSON format:

{{
    "matchScore": 0,
    "technicalQuestions": [],
    "behavioralQuestions": [],
    "skillGaps": [],
    "preparationPlan": [],
    "title": ""
}}

Rules:
- matchScore must be between 0 and 100.
- technicalQuestions should contain interview questions with:
  question, intention, answer
- behavioralQuestions should contain:
  question, intention, answer
- skillGaps should contain:
  skill, severity
- preparationPlan should contain:
  day, focus, tasks
- title should contain the job title.
"""

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    content = response.choices[0].message.content

    # Sometimes models return JSON inside ```json ... ```
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()


    return json.loads(content)

def create_resume_pdf(resume, self_description, job_description):

    prompt = f"""
You are a professional resume writer.

Create a professional, ATS-friendly resume for this candidate.

RESUME:
{resume}

SELF DESCRIPTION:
{self_description}

JOB DESCRIPTION:
{job_description}

Return ONLY valid HTML.

Requirements:
- Simple professional design
- ATS friendly
- 1 to 2 pages
- Tailor content to the job description
- Do not invent experience, skills, education or achievements
- Use clean HTML
- Include sections:
  Name / Contact
  Summary
  Skills
  Experience
  Education
  Projects
  Certifications if available
- Make it look like a real human-written resume
"""

    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3-0324",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    html_content = response.choices[0].message.content.strip()

    if html_content.startswith("```"):
        html_content = html_content.replace("```html", "")
        html_content = html_content.replace("```", "")
        html_content = html_content.strip()

    pdf_file = BytesIO()

    pisa.CreatePDF(
        html_content,
        dest=pdf_file
    )

    pdf_file.seek(0)

    return pdf_file.getvalue()