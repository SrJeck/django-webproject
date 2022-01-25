from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, "jobPortalApp/index.html")


def home(request):
    # return HttpResponse('Home Page')
    return render(request, "jobPortalApp/index.html")


# job seeker
def seeker_no_info(request):
    return render(request, "jobPortalApp/pages/profile/seeker/no-info.html")

# admin


def admin_dashboard(request):
    return render(request, "jobPortalApp/admin/admin_dashboard.html")


def manage_user(request):
    return render(request, "jobPortalApp/admin/manage_user.html")


def company(request):
    return render(request, "jobPortalApp/admin/company.html")


def jobs(request):
    return render(request, "jobPortalApp/admin/jobs.html")

# job provider


def provider_no_info(request):
    return render(request, "jobPortalApp/pages/profile/provider/no-info.html")


def provider_with_info(request):
    return render(request, "jobPortalApp/pages/profile/provider/with-info.html")


def provider_edit_info(request):
    return render(request, "jobPortalApp/pages/profile/provider/add-edit-info.html")


def provider_show_job_post(request):
    return render(request, "jobPortalApp/pages/profile/provider/show-job-post.html")


def provider_edit_job(request):
    return render(request, "jobPortalApp/pages/profile/provider/add-edit-job.html")


def provider_show_applicant(request):
    return render(request, "jobPortalApp/pages/profile/provider/show-applicant.html")
