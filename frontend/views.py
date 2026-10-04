from django.shortcuts import render


def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")


def dashboard_page(request):
    return render(request, "dashboard.html")


def new_interview_page(request):
    return render(request, "new_interview.html")


def reports_page(request):
    return render(request, "reports.html")


def report_page(request, report_id):
    return render(request, "report.html")


def profile_page(request):
    return render(request, "profile.html")