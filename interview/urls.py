from django.urls import path
from interview import views

urlpatterns = [
    path("upload-resume/", views.upload_resume),
    path('generate-report/', views.generate_report),
    path("reports/", views.get_reports),
    path("reports/<int:report_id>/", views.get_report),
    path(
    "reports/<int:report_id>/resume/",
    views.generate_resume_pdf
),
]
