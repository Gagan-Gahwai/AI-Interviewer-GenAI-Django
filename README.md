# AI Interviewer

AI Interviewer is a Django-based Generative AI project that helps users prepare for job interviews.

The user uploads a resume, adds a job description, and writes a short introduction about themselves. The application analyzes this information using DeepSeek through the Hugging Face Inference API and generates a personalized interview preparation report.

## Features

- User registration and login
- JWT authentication
- Secure logout with refresh token blacklisting
- Resume PDF upload
- Resume text extraction
- Job description analysis
- AI-based job match score
- Technical interview questions
- Behavioral interview questions
- Skill gap analysis
- Personalized preparation plan
- Interview report history
- AI-generated tailored resume PDF
- Django-based frontend using HTML, CSS and JavaScript

## How It Works

```text
Resume PDF
     +
Job Description
     +
Self Description
        ↓
      Django
        ↓
 Resume Text Extraction
        ↓
DeepSeek via Hugging Face
        ↓
  AI Interview Report
        ↓
      SQLite
        ↓
 Report & Interview Preparation
        ↓
 Tailored Resume PDF


 ## Blog

I wrote about this project and what I learned while building it:

[Building an AI Interviewer with Django and DeepSeek]
https://aiinterviewer.hashnode.dev/building-an-ai-interviewer-with-django-and-deepseek