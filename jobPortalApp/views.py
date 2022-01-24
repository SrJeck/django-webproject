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
