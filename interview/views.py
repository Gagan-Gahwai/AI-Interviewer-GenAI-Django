from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .servieces import extract_resume_text
from django.http import JsonResponse,HttpResponse


from rest_framework_simplejwt.tokens import AccessToken

from users.models import User

from .servieces import (
    extract_resume_text,
    generate_interview_report,
    create_resume_pdf
)

from .models import InterviewReport

# Create your views here.

@csrf_exempt
def upload_resume(request):

    if request.method != 'POST':
        return JsonResponse({
            'message': 'Only POST request allowed'
        }, status = 405)

    resume = request.FILES.get("resume")

    if not resume:
        return JsonResponse({
            'message': "Resume PDF is required"
        },status = 400)

    if resume.size > 3 * 1024 * 1024:
        return JsonResponse({
            'message' : "resume must be less than 3MB"
        }, status = 400)

    try :
        resume_text = extract_resume_text(resume)

        return JsonResponse({
            'message': "Resume extracted successfully",
            'resume_text' : resume_text
        })
    except Exception as e:
        return JsonResponse({
            'message': "Failed to read PDF",
            'error' : str(e)

        }, status = 400)

@csrf_exempt
def generate_report(request):

    if request.method != "POST":
        return JsonResponse({
            "message": "Only POST request allowed"
        }, status=405)

    # Get access token
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse({
            "message": "Authorization token required"
        }, status=401)

    try:
        token = auth_header.split(" ")[1]

        access_token = AccessToken(token)

        user_id = access_token["user_id"]

        user = User.objects.get(id=user_id)

    except Exception:
        return JsonResponse({
            "message": "Invalid or expired token"
        }, status=401)

    # Get form data
    resume = request.FILES.get("resume")
    job_description = request.POST.get("job_description")
    self_description = request.POST.get("self_description")

    if not resume:
        return JsonResponse({
            "message": "Resume PDF is required"
        }, status=400)

    if not job_description:
        return JsonResponse({
            "message": "Job description is required"
        }, status=400)

    if not self_description:
        return JsonResponse({
            "message": "Self description is required"
        }, status=400)

    try:

        # Extract text from PDF
        resume_text = extract_resume_text(resume)

        # Send data to DeepSeek
        report = generate_interview_report(
            resume=resume_text,
            self_description=self_description,
            job_description=job_description
        )

        # Save report in database
        interview_report = InterviewReport.objects.create(
            user=user,
            job_description=job_description,
            resume=resume_text,
            self_description=self_description,
            match_score=report.get("matchScore"),
            technical_questions=report.get("technicalQuestions", []),
            behavioral_questions=report.get("behavioralQuestions", []),
            skill_gaps=report.get("skillGaps", []),
            preparation_plan=report.get("preparationPlan", []),
            title=report.get("title", "Interview Report")
        )

        return JsonResponse({
            "message": "Interview report generated successfully",
            "report_id": interview_report.id,
            "report": report
        }, status=201)

    except Exception as e:

        return JsonResponse({
            "message": "Failed to generate interview report",
            "error": str(e)
        }, status=500)


@csrf_exempt
def get_reports(request):

    if request.method != "GET":
        return JsonResponse({
            "message": "Only GET request allowed"
        }, status=405)

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse({
            "message": "Authorization token required"
        }, status=401)

    try:
        token = auth_header.split(" ")[1]
        access_token = AccessToken(token)
        user_id = access_token["user_id"]

        user = User.objects.get(id=user_id)

    except Exception:
        return JsonResponse({
            "message": "Invalid or expired token"
        }, status=401)

    reports = InterviewReport.objects.filter(
        user=user
    ).order_by("-created_at")

    data = []

    for report in reports:
        data.append({
            "id": report.id,
            "title": report.title,
            "match_score": report.match_score,
            "created_at": report.created_at,
        })

    return JsonResponse({
        "reports": data
    })

@csrf_exempt
def get_report(request, report_id):

    if request.method != "GET":
        return JsonResponse({
            "message": "Only GET request allowed"
        }, status=405)

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse({
            "message": "Authorization token required"
        }, status=401)

    try:
        token = auth_header.split(" ")[1]
        access_token = AccessToken(token)
        user_id = access_token["user_id"]

        user = User.objects.get(id=user_id)

    except Exception:
        return JsonResponse({
            "message": "Invalid or expired token"
        }, status=401)

    try:
        report = InterviewReport.objects.get(
            id=report_id,
            user=user
        )
    except InterviewReport.DoesNotExist:
        return JsonResponse({
            "message": "Report not found"
        }, status=404)

    return JsonResponse({
        "id": report.id,
        "title": report.title,
        "job_description": report.job_description,
        "resume": report.resume,
        "self_description": report.self_description,
        "match_score": report.match_score,
        "technical_questions": report.technical_questions,
        "behavioral_questions": report.behavioral_questions,
        "skill_gaps": report.skill_gaps,
        "preparation_plan": report.preparation_plan,
        "created_at": report.created_at,
        "updated_at": report.updated_at,
    })

def generate_resume_pdf(request, report_id):

    if request.method != "GET":
        return JsonResponse({
            "message": "Only GET request allowed"
        }, status=405)

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JsonResponse({
            "message": "Authorization token required"
        }, status=401)

    try:
        token = auth_header.split(" ")[1]
        access_token = AccessToken(token)
        user_id = access_token["user_id"]

        user = User.objects.get(id=user_id)

    except Exception:
        return JsonResponse({
            "message": "Invalid or expired token"
        }, status=401)

    try:
        report = InterviewReport.objects.get(
            id=report_id,
            user=user
        )
    except InterviewReport.DoesNotExist:
        return JsonResponse({
            "message": "Report not found"
        }, status=404)

    try:

        pdf_data = create_resume_pdf(
        resume=report.resume,
        self_description=report.self_description,
        job_description=report.job_description
    )

        response = HttpResponse(
            pdf_data,
            content_type="application/pdf"
        )

        response["Content-Disposition"] = (
            f'attachment; filename="resume_{report.id}.pdf"'
        )

        return response

    except Exception as e:
        return JsonResponse({
            "message": "Failed to generate resume",
            "error": str(e)
        }, status=500)
    
