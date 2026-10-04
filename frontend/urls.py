from django.urls import path

from .views import (
    login_page,
    register_page,
    dashboard_page,
    new_interview_page,
    reports_page,
    report_page,
    profile_page,
)

urlpatterns = [
    path("", login_page),
    path("register/", register_page),

    path("dashboard/", dashboard_page),

    path(
        "interview/new/",
        new_interview_page
    ),

    path(
        "reports/",
        reports_page
    ),

    path(
        "reports/<int:report_id>/",
        report_page
    ),

    path(
        "profile/",
        profile_page
    ),
]