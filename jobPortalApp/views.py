from fileinput import filename
import imp
from pydoc import describe
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.core.mail import send_mail
from django.http import FileResponse
import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
# from .models import Event, Venue
# from .forms import VenueForm, EventForm

# Create your views here.
def index(request):
    return render(request, "jobPortalApp/index.html")


def redirectLogin(request):
    return redirect('login')

def homeRedirect(request):
    if 'job-search' in request.session:
        del request.session['job-search']
    if 'job-type' in request.session:
        del request.session['job-type']
    if 'job-country' in request.session:
        del request.session['job-country']
    if 'job-city' in request.session:
        del request.session['job-city']
    return redirect('home')

def home(request):
    # return HttpResponse('Home Page')
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        job_title = request.session['job_type']
        user_id = request.session['user_id']
        profile = PROFILE.objects.filter(user_id=user_id)
        user_name = ""
        if job_title == "Job Seeker":
            seeker_name = SEEKER.objects.get(user_id=user_id)
            user_name = seeker_name.fullname
        elif job_title == "Job Provider":
            provider_name = COMPANY.objects.get(user_id=user_id)
            user_name = provider_name.name
        job_search = ""
        job_type = False
        job_country = False
        job_city = False
        default_all_jobs = JOB.objects.filter(status='Activated')
        default_all_jobs_skills = {}
        default_all_jobs_apllication = {}
        for default_all_job in default_all_jobs:
            job_skillnames_per_jobs = []
            job_skills_per_jobs = JOBSKILL.objects.filter(
                job_id=default_all_job.id)
            application_per_jobs = APPLICATION.objects.filter(
                job_id=default_all_job.id).count()
            default_all_jobs_apllication[default_all_job.id] = str(application_per_jobs)
            for job_skills_per_job in job_skills_per_jobs:
                skills = SKILL.objects.get(id=job_skills_per_job.skill_id)
                job_skillnames_per_jobs.append(skills.skillname)
            default_all_jobs_skills[default_all_job.id] = job_skillnames_per_jobs
        if 'job-search' and 'job-type' and 'job-country' and 'job-city' in request.session:
            job_search = request.session['job-search']
            job_type = request.session['job-type']
            job_country = request.session['job-country']
            job_city = request.session['job-city']
            if job_country == "":
                job_country = False
            if job_type == "":
                job_type = False
            if job_city == "":
                job_city = False
        is_non_empty = bool(job_search)
        jobs = []
        company_jobs_ids = []
        skillnames_per_jobs = {}
        applications_per_jobs = {}
        applications_per_jobs = {}
        searcher = ""
        # search city country type
        if is_non_empty != False and job_city != False and job_country != False and job_type != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city, country=job_country).exists():
                company_ids = COMPANY.objects.filter(
                    city=job_city, country=job_country)
            if JOB.objects.filter(name__contains=job_search,status="Activated").exists():
                for company_id in company_ids:
                    filtered_jobs = JOB.objects.filter(
                        name__contains=job_search, company_id=company_id.user_id, type=job_type)
                    jobs.append(JOB.objects.filter(
                        name__contains=job_search, company_id=company_id.user_id, type=job_type))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(
                                id=job_id.job_id, company_id=company_id.user_id, type=job_type,status="Activated"))
                            filtered_jobs = JOB.objects.filter(
                                id=job_id.job_id, company_id=company_id.user_id, type=job_type,status="Activated")
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " " + job_type + " in " + job_country + " - " + job_city
        # search city type
        elif is_non_empty != False and job_type != False and job_city != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city).exists():
                company_ids = COMPANY.objects.filter(city=job_city)
            if JOB.objects.filter(name__contains=job_search, type=job_type).exists():
                for company_id in company_ids:
                    filtered_jobs = JOB.objects.filter(
                        name__contains=job_search, type=job_type, company_id=company_id.user_id,status="Activated")
                    jobs.append(JOB.objects.filter(
                        name__contains=job_search, type=job_type, company_id=company_id.user_id,status="Activated"))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(
                                id=job_id.job_id, type=job_type, company_id=company_id.user_id,status="Activated"))
                            filtered_jobs = JOB.objects.filter(
                                id=job_id.job_id, type=job_type, company_id=company_id.user_id,status="Activated")
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " " + job_type + " in " + job_city
        # search city country
        elif is_non_empty != False and job_country != False and job_city != False:
            company_ids = ""
            if COMPANY.objects.filter(country=job_country, city=job_city).exists():
                company_ids = COMPANY.objects.filter(
                    country=job_country, city=job_city)
            if JOB.objects.filter(name__contains=job_search).exists():
                for company_id in company_ids:
                    filtered_jobs = JOB.objects.filter(
                        name__contains=job_search, company_id=company_id.user_id,status="Activated")
                    jobs.append(JOB.objects.filter(
                        name__contains=job_search, company_id=company_id.user_id,status="Activated"))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(
                                id=job_id.job_id, company_id=company_id.user_id,status="Activated"))
                            filtered_jobs = JOB.objects.filter(
                                id=job_id.job_id, company_id=company_id.user_id,status="Activated")
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " in " + job_country + " - " + job_city
        # search country type
        elif is_non_empty != False and job_type != False and job_country != False:
            company_ids = ""
            if COMPANY.objects.filter(country=job_country).exists():
                company_ids = COMPANY.objects.filter(country=job_country)
            if JOB.objects.filter(name__contains=job_search, type=job_type).exists():
                for company_id in company_ids:
                    filtered_jobs = JOB.objects.filter(
                        name__contains=job_search, type=job_type, company_id=company_id.user_id,status="Activated")
                    jobs.append(JOB.objects.filter(
                        name__contains=job_search, type=job_type, company_id=company_id.user_id,status="Activated"))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(
                                id=job_id.job_id, type=job_type, company_id=company_id.user_id,status="Activated"))
                            filtered_jobs = JOB.objects.filter(
                                id=job_id.job_id, type=job_type, company_id=company_id.user_id,status="Activated")
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " " + job_type + " in " + job_country
        # type city country
        elif job_city != False and job_country != False and job_type != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city, country=job_country).exists():
                company_ids = COMPANY.objects.filter(
                    city=job_city, country=job_country)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(
                        type=job_type, company_id=company_id.user_id,status="Activated"))
                    filtered_jobs = JOB.objects.filter(
                        type=job_type, company_id=company_id.user_id,status="Activated")
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher = job_type + " in " + job_country + " - " + job_city
        # search country
        elif is_non_empty != False and job_country != False:
            company_ids = ""
            if COMPANY.objects.filter(country=job_country).exists():
                company_ids = COMPANY.objects.filter(country=job_country)
            if JOB.objects.filter(name__contains=job_search).exists():
                for company_id in company_ids:
                    filtered_jobs = JOB.objects.filter(
                        name__contains=job_search, company_id=company_id.user_id,status="Activated")
                    jobs.append(JOB.objects.filter(
                        name__contains=job_search, company_id=company_id.user_id,status="Activated"))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(
                                id=job_id.job_id, company_id=company_id.user_id,status="Activated"))
                            filtered_jobs = JOB.objects.filter(
                                id=job_id.job_id, company_id=company_id.user_id,status="Activated")
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " in " + job_country
        # search city
        elif is_non_empty != False and job_city != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city).exists():
                company_ids = COMPANY.objects.filter(city=job_city)
            if JOB.objects.filter(name__contains=job_search).exists():
                for company_id in company_ids:
                    filtered_jobs = JOB.objects.filter(
                        name__contains=job_search, company_id=company_id.user_id,status="Activated")
                    jobs.append(JOB.objects.filter(
                        name__contains=job_search, company_id=company_id.user_id,status="Activated"))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(
                                id=job_id.job_id, company_id=company_id.user_id,status="Activated"))
                            filtered_jobs = JOB.objects.filter(
                                id=job_id.job_id, company_id=company_id.user_id,status="Activated")
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " in " + job_city
        # search type
        elif is_non_empty != False and job_type != False:
            if JOB.objects.filter(name__contains=job_search, type=job_type).exists():
                jobs.append(JOB.objects.filter(
                    name__contains=job_search, type=job_type,status="Activated"))
                filtered_jobs = JOB.objects.filter(
                    name__contains=job_search, type=job_type,status="Activated")
                for filtered_job in filtered_jobs:
                    company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        jobs.append(JOB.objects.filter(
                            id=job_id.job_id, type=job_type,status="Activated"))
                        filtered_jobs = JOB.objects.filter(
                            id=job_id.job_id, type=job_type,status="Activated")
                        for filtered_job in filtered_jobs:
                            company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " " + job_type
        # city country
        elif job_city != False and job_country != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city, country=job_country).exists():
                company_ids = COMPANY.objects.filter(
                    city=job_city, country=job_country)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(
                        company_id=company_id.user_id,status="Activated"))
                    filtered_jobs = JOB.objects.filter(
                        company_id=company_id.user_id,status="Activated")
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher = "Jobs in " + job_country + " - " + job_city
        # city type
        elif job_city != False and job_type != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city).exists():
                company_ids = COMPANY.objects.filter(city=job_city)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(
                        company_id=company_id.user_id, type=job_type,status="Activated"))
                    filtered_jobs = JOB.objects.filter(
                        company_id=company_id.user_id, type=job_type,status="Activated")
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher = job_type+" in " + job_city
        # type country
        elif job_type != False and job_country != False:
            company_ids = ""
            if COMPANY.objects.filter(country=job_country).exists():
                company_ids = COMPANY.objects.filter(country=job_country)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(
                        company_id=company_id.user_id, type=job_type,status="Activated"))
                    filtered_jobs = JOB.objects.filter(
                        company_id=company_id.user_id, type=job_type,status="Activated")
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher = job_type+" in " + job_country
        # city
        elif job_city != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city).exists():
                company_ids = COMPANY.objects.filter(city=job_city)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(
                        company_id=company_id.user_id,status="Activated"))
                    filtered_jobs = JOB.objects.filter(
                        company_id=company_id.user_id,status="Activated")
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher = "Jobs in " + job_city
        # country
        elif job_country != False:
            company_ids = ""
            if COMPANY.objects.filter(country=job_country).exists():
                company_ids = COMPANY.objects.filter(country=job_country)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(
                        company_id=company_id.user_id,status="Activated"))
                    filtered_jobs = JOB.objects.filter(
                        company_id=company_id.user_id,status="Activated")
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher = "Jobs in " + job_country
        # type
        elif job_type != False:
            if JOB.objects.filter(type=job_type).exists():
                jobs.append(JOB.objects.filter(type=job_type,status="Activated"))
                filtered_jobs = JOB.objects.filter(type=job_type,status="Activated")
                for filtered_job in filtered_jobs:
                    company_jobs_ids.append(filtered_job.id)
            searcher = job_type
        # search
        elif is_non_empty != False:
            if JOB.objects.filter(name__contains=job_search).exists():
                jobs.append(JOB.objects.filter(name__contains=job_search,status="Activated"))
                filtered_jobs = JOB.objects.filter(name__contains=job_search,status="Activated")
                for filtered_job in filtered_jobs:
                    company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        jobs.append(JOB.objects.filter(id=job_id.job_id,status="Activated"))
                        filtered_jobs = JOB.objects.filter(id=job_id.job_id,status="Activated")
                        for filtered_job in filtered_jobs:
                            company_jobs_ids.append(filtered_job.id)
            searcher = job_search

        results = ""
        if len(jobs) == 0:
            results = "No Results"
        for company_jobs_id in company_jobs_ids:
            job_skillnames_per_jobs = []
            job_skills_per_jobs = JOBSKILL.objects.filter(
                job_id=company_jobs_id)
            application_per_jobs = APPLICATION.objects.filter(
                job_id=company_jobs_id).count()
            applications_per_jobs[company_jobs_id] = str(application_per_jobs)
            for job_skills_per_job in job_skills_per_jobs:
                skills = SKILL.objects.get(id=job_skills_per_job.skill_id)
                job_skillnames_per_jobs.append(skills.skillname)
            skillnames_per_jobs[company_jobs_id] = job_skillnames_per_jobs
        return render(request, 'jobPortalApp/pages/index.html', {'jobs': jobs, 'skillnames_per_jobs': skillnames_per_jobs, 'searcher': searcher, 'user_name': user_name, 'user_type': job_title, 'job_search': job_search, 'job_type': job_type, 'job_city': job_city, 'job_country': job_country, 'applications_per_jobs': applications_per_jobs, 'results': results,'profile':profile,'default_all_jobs':default_all_jobs,'default_all_jobs_skills':default_all_jobs_skills,'default_all_jobs_apllication':default_all_jobs_apllication})

def admin_activate_user(request):
    if request.method == "POST":
        user_id = request.POST['user-id']
        SEEKER.objects.filter(user_id=user_id).update(status="Activated")
    return redirect('manage_user')


def admin_deactivate_user(request):
    if request.method == "POST":
        user_id = request.POST['user-id']
        SEEKER.objects.filter(user_id=user_id).update(status="Deactivated")
    return redirect('manage_user')

def admin_deactivate_company(request):
    if request.method == "POST":
        user_id = request.POST['user-id']
        COMPANY.objects.filter(user_id=user_id).update(status="Deactivated")
    return redirect('company')


def admin_activate_company(request):
    if request.method == "POST":
        user_id = request.POST['user-id']
        COMPANY.objects.filter(user_id=user_id).update(status="Activated")
    return redirect('company')

def admin_login(request):
    return render(request,'jobPortalApp/admin/login.html')

def admin_login_process(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        message = ""
        if User.objects.filter(username=username,is_staff=True).exists():
            user = User.objects.get(username=username,is_staff=True)
            if user.check_password(password):
                request.session['admin_id'] = user.id
                return redirect('manage_user')
            else:
                message = "Wrong Password"
                return render(request,'jobPortalApp/admin/login.html',{'message':message})
        else:
            message = "Wrong Username"
            return render(request,'jobPortalApp/admin/login.html',{'message':message})


def admin_logout(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        del request.session['admin_id']
        return redirect('login')


def admin_activate_jobs(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        if request.method == "POST":
            job_id = request.POST['job-id']
            JOB.objects.filter(id=job_id).update(status="Activated")
        return redirect('jobs')


def admin_deactivate_jobs(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        if request.method == "POST":
            job_id = request.POST['job-id']
            JOB.objects.filter(id=job_id).update(status="Deactivated")
        return redirect('jobs')


def manage_user(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        activated_users_list = {}
        deactivated_users_list = {}
        activated_seekers = SEEKER.objects.filter(status="Activated")
        deactivated_seekers = SEEKER.objects.filter(status="Deactivated")

        for activated_seeker in activated_seekers:
            activated_users_list[activated_seeker.user_id] = User.objects.filter(
                id=activated_seeker.user_id)
        for deactivated_seeker in deactivated_seekers:
            deactivated_users_list[deactivated_seeker.user_id] = User.objects.filter(
                id=deactivated_seeker.user_id)
        return render(request, 'jobPortalApp/admin/manage_user.html', {'deactivated_seekers': deactivated_seekers, 'activated_seekers': activated_seekers, 'deactivated_users_list': deactivated_users_list, 'activated_users_list': activated_users_list})


def company(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        activated_company_list = {}
        deactivated_company_list = {}
        activated_companys = COMPANY.objects.filter(status="Activated")
        deactivated_companys = COMPANY.objects.filter(status="Deactivated")

        for activated_company in activated_companys:
            activated_company_list[activated_company.user_id] = User.objects.filter(
                id=activated_company.user_id)

        for deactivated_company in deactivated_companys:
            deactivated_company_list[deactivated_company.user_id] = User.objects.filter(
                id=deactivated_company.user_id)

        return render(request, "jobPortalApp/admin/company.html", {'activated_companys': activated_companys, 'activated_company_list': activated_company_list, 'deactivated_companys': deactivated_companys, 'deactivated_company_list': deactivated_company_list})


def jobs(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:

        activated_jobs = JOB.objects.filter(status="Activated")
        deactivated_jobs = JOB.objects.filter(status="Deactivated")

        return render(request, "jobPortalApp/admin/jobs.html", {'activated_jobs': activated_jobs, 'deactivated_jobs': deactivated_jobs})


def admin_edit_user(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        user_id = ""
        if request.method == 'POST':
            user_id = request.POST['user-id']
        skills = SKILL.objects.all()
        skillnames = []
        seeker = SEEKER.objects.get(user_id=user_id)
        seekerskills = SEEKERSKILL.objects.filter(user_id=user_id)
        for seekerskill in seekerskills:
            skill = SKILL.objects.get(id=seekerskill.skill_id)
            skillnames.append(skill.skillname)
        return render(request, "jobPortalApp/admin/admin-edit-user.html",{'seeker':seeker,'skillnames':skillnames,'skills':skills})

def admin_edit_user_process(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        user_id = ""
        if request.method == 'POST':
            user_id = request.POST['edit-id']
            user_fullname = request.POST['edit-fullname']
            user_about = request.POST['edit-about']
            user_experience = request.POST['edit-experience']
            job_skills = request.POST.getlist('skill')
            SEEKER.objects.filter(user_id=user_id).update(fullname=user_fullname)
            SEEKER.objects.filter(user_id=user_id).update(about=user_about)
            SEEKER.objects.filter(user_id=user_id).update(experience=user_experience)
            if len(job_skills) > 0:
                past_skills = SEEKERSKILL.objects.filter(user_id=user_id)
                past_skills.delete()
            for job_skill in job_skills:
                SEEKERSKILL.objects.create(user_id=user_id,skill_id=job_skill)
        return redirect('manage_user')


def admin_edit_company(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        user_id = ""
        if request.method == 'POST':
            user_id = request.POST['user-id']
        provider = COMPANY.objects.get(user_id=user_id)
        return render(request, "jobPortalApp/admin/admin-edit-company.html",{'provider':provider})

def admin_edit_company_process(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        if request.method == 'POST':
            user_id = request.POST['edit-id']
            user_name = request.POST['edit-name']
            user_description = request.POST['edit-description']
            user_city = request.POST['edit-city']
            user_country = request.POST['edit-country']
            COMPANY.objects.filter(user_id=user_id).update(name=user_name)
            COMPANY.objects.filter(user_id=user_id).update(description=user_description)
            COMPANY.objects.filter(user_id=user_id).update(city=user_city)
            COMPANY.objects.filter(user_id=user_id).update(country=user_country)
        return redirect('company')


def admin_edit_job(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        job_id = ""
        if request.method == 'POST':
            job_id = request.POST['job-id']
        skills = SKILL.objects.all()
        skillnames = []
        job = JOB.objects.get(id=job_id)
        seekerskills = JOBSKILL.objects.filter(job_id=job_id)
        for seekerskill in seekerskills:
            skill = SKILL.objects.get(id=seekerskill.skill_id)
            skillnames.append(skill.skillname)
        return render(request, "jobPortalApp/admin/admin-edit-job.html",{'job':job,'skills':skills,'skillnames':skillnames})

def admin_edit_job_process(request):
    if 'admin_id' not in request.session:
       return redirect('login')
    else:
        if request.method == 'POST':
            job_id = request.POST['job-id']
            job_name = request.POST['job-name']
            job_salary = request.POST['job-salary']
            job_description = request.POST['job-description']
            job_type = request.POST['job-type']
            job_skills = request.POST.getlist('skill')
            
            JOB.objects.filter(id=job_id).update(name=job_name)
            JOB.objects.filter(id=job_id).update(description=job_description)
            JOB.objects.filter(id=job_id).update(salary=job_salary)
            JOB.objects.filter(id=job_id).update(type=job_type)
            if len(job_skills) > 0:
                past_skills = JOBSKILL.objects.filter(job_id=job_id)
                past_skills.delete()
            for job_skill in job_skills:
                JOBSKILL.objects.create(job_id=job_id,skill_id=job_skill)
        return redirect('jobs')

def seekerDeleteAccount(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        ACTIVITY.objects.create(name="Delete", description="Delete Account", user_id=user_id)
        seeker = SEEKER.objects.filter(user_id=user_id)
        seekerskill = SEEKERSKILL.objects.filter(user_id=user_id)
        application = APPLICATION.objects.filter(user_id=user_id)
        user = User.objects.filter(id=user_id)
        profile = PROFILE.objects.filter(user_id=user_id)
        resume = RESUME.objects.filter(user_id=user_id)
        seeker.delete()
        seekerskill.delete()
        application.delete()
        user.delete()
        profile.delete()
        resume.delete()
        return redirect('logout')

def providerDeleteAccount(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        ACTIVITY.objects.create(name="Delete", description="Delete Account", user_id=user_id)
        provider = COMPANY.objects.filter(user_id=user_id)
        jobs = JOB.objects.filter(company_id=user_id)
        for job in jobs:
            jobskill = JOBSKILL.objects.filter(job_id=job.id)
            jobskill.delete()
            application = APPLICATION.objects.filter(job_id=job.id)
            application.delete()
        jobs.delete()
        user = User.objects.filter(id=user_id)
        user.delete()
        profile = PROFILE.objects.filter(user_id=user_id)
        profile.delete()
        resume = RESUME.objects.filter(user_id=user_id)
        resume.delete()
        provider.delete()
        return redirect('logout')


def activity_logs(request):
    user_per_acts = {}
    activitys = ACTIVITY.objects.all()
    for activity in activitys:
        if User.objects.filter(id=activity.user_id).exists():
            user = User.objects.get(id=activity.user_id)
            user_per_acts[activity.user_id] = user.username
        else:
            user_per_acts[activity.user_id] = "Deleted Account"

    return render(request, "jobPortalApp/admin/activity_logs.html",{'activitys':activitys,'user_per_acts':user_per_acts})

def logout(request):
    user_id = request.session['user_id']
    ACTIVITY.objects.create(
        name="Logged", description="Logged Out", user_id=user_id)
    del request.session['user_id']
    del request.session['user_type']
    del request.session['job_type']
    if 'job-search' and 'job-type' and 'job-country' and 'job-city' in request.session:
        del request.session['job-search']
        del request.session['job-type']
        del request.session['job-city']
        del request.session['job-country']
    request.session.modified = True
    return redirect("login")


def login(request):
    if 'user_id' in request.session:
        return redirect('profile')
    else:
        return render(request, "jobPortalApp/pages/login.html")

def loginProcess(request):
    if request.method == 'POST':
            usermail = request.POST['usermail']
            password = request.POST['password']
            if User.objects.filter(username=usermail).exists():
                user = User.objects.get(username=usermail)
                user_id = user.id
                message = ""
                if user.check_password(password):
                    if SEEKER.objects.filter(user_id=user_id).exists():
                        status = SEEKER.objects.get(user_id=user_id)
                        if status.status == "Activated":
                            request.session['user_id'] = user_id
                            request.session['user_type'] = "seeker"
                            request.session['job_type'] = "Job Seeker"
                            ACTIVITY.objects.create(name="Logged", description="Logged In", user_id=user_id)
                            return redirect('profile')
                        else:
                            message = "Account Seems to be Deactivated"
                            return render(request, 'jobPortalApp/pages/login.html', {'message': message})
                    elif COMPANY.objects.filter(user_id=user_id).exists():
                        status = COMPANY.objects.get(user_id=user_id)
                        if status.status == "Activated":
                            request.session['user_id'] = user_id
                            request.session['user_type'] = "provider"
                            request.session['job_type'] = "Job Provider"
                            ACTIVITY.objects.create(name="Logged", description="Logged In", user_id=user_id)
                            return redirect('profile')
                        else:
                            message = "Account Seems to be Deactivated"
                            return render(request, 'jobPortalApp/pages/login.html', {'message': message})
                else:
                    message = "Wrong Password"
                    return render(request, 'jobPortalApp/pages/login.html', {'message': message})
            elif User.objects.filter(email=usermail).exists():
                user = User.objects.get(email=usermail)
                user_id = user.id
                if user.check_password(password):
                    if SEEKER.objects.filter(user_id=user_id).exists():
                        status = SEEKER.objects.get(user_id=user_id)
                        if status.status == "Activated":
                            request.session['user_id'] = user_id
                            request.session['user_type'] = "seeker"
                            request.session['job_type'] = "Job Seeker"
                            ACTIVITY.objects.create(name="Logged", description="Logged In", user_id=user_id)
                            return redirect('profile')
                        else:
                            message = "Account Seems to be Deactivated"
                            return render(request, 'jobPortalApp/pages/login.html', {'message': message})   
                    elif COMPANY.objects.filter(user_id=user_id).exists():
                        status = COMPANY.objects.get(user_id=user_id)
                        if status.status == "Activated":
                            request.session['user_id'] = user_id
                            request.session['user_type'] = "provider"
                            request.session['job_type'] = "Job Provider"
                            ACTIVITY.objects.create(name="Logged", description="Logged In", user_id=user_id)
                            return redirect('profile')
                        else:
                            message = "Account Seems to be Deactivated"
                            return render(request, 'jobPortalApp/pages/login.html', {'message': message})
                else:
                    message = "Wrong Password"
                    return render(request, 'jobPortalApp/pages/login.html', {'message': message})
            else:
                message = "Wrong Email or Username"
                return render(request, 'jobPortalApp/pages/login.html', {'message': message})


def profile(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        job_type = request.session['job_type']
        user_details = User.objects.get(id=user_id)
        profile = PROFILE.objects.filter(user_id=user_id)
        all_user = User.objects.filter(is_staff=True)
        if user_type == 'seeker':
            if SEEKER.objects.filter(user_id=user_id).exists():
                seeker_skills = []
                if SEEKERSKILL.objects.filter(user_id=user_id).exists():
                    seeker_skills_id = SEEKERSKILL.objects.filter(user_id=user_id)
                    for i in seeker_skills_id:
                        skill_name = SKILL.objects.get(id=i.skill_id)
                        seeker_skills.append(skill_name)
                seeker_details = SEEKER.objects.get(user_id=user_id)
                seeker_resume = ""
                if RESUME.objects.filter(user_id=user_id).exists():
                    seeker_resume = RESUME.objects.get(user_id=user_id)
                return render(request, 'jobPortalApp/pages/profile/seeker/with-info.html', {'user_details': user_details, 'seeker_details': seeker_details, 'seeker_skills': seeker_skills, 'user_type': job_type, 'seeker_resume': seeker_resume, 'all_user': all_user, 'profile': profile})
        elif user_type == 'provider':
            if COMPANY.objects.filter(user_id=user_id).exists():
                company_details = COMPANY.objects.get(user_id=user_id)
                company_jobs = JOB.objects.filter(company_id=user_id)
                company_jobs_ids = []
                skillnames_per_jobs = {}
                applications_per_jobs = {}
                for company_job in company_jobs:
                    company_jobs_ids.append(company_job.id)

                for company_jobs_id in company_jobs_ids:
                    job_skillnames_per_jobs = []
                    job_skills_per_jobs = JOBSKILL.objects.filter(
                        job_id=company_jobs_id)
                    application_per_jobs = APPLICATION.objects.filter(
                        job_id=company_jobs_id).count()
                    applications_per_jobs[company_jobs_id] = str(
                        application_per_jobs)
                    for job_skills_per_job in job_skills_per_jobs:
                        skills = SKILL.objects.get(
                            id=job_skills_per_job.skill_id)
                        job_skillnames_per_jobs.append(skills.skillname)
                    skillnames_per_jobs[company_jobs_id] = job_skillnames_per_jobs
                return render(request, 'jobPortalApp/pages/profile/provider/with-info.html', {'company_details': company_details, 'user_details': user_details, 'user_type': job_type, 'company_jobs': company_jobs, 'skillnames_per_jobs': skillnames_per_jobs, 'applications_per_jobs': applications_per_jobs, 'profile': profile})


@xframe_options_sameorigin
def seekerView(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        job_type = request.session['job_type']
        seeker_details = SEEKER.objects.get(user_id=user_id)
        profile = PROFILE.objects.filter(user_id=user_id)
        seeker = RESUME.objects.get(user_id=user_id)
        return render(request, 'jobPortalApp/pages/profile/seeker/view-resume.html', {'seeker': seeker, 'user_type': job_type, 'seeker_details': seeker_details})


def seekerEdit(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        seeker = SEEKER.objects.get(user_id=user_id)
        job_type = request.session['job_type']
        profile = PROFILE.objects.filter(user_id=user_id)
        seeker_details = SEEKER.objects.get(user_id=user_id)
        form = resumeForm(use_required_attribute=False)
        seeker_skills = []
        if SEEKERSKILL.objects.filter(user_id=user_id).exists():
            seeker_skills_id = SEEKERSKILL.objects.filter(user_id=user_id)
            for i in seeker_skills_id:
                skill_name = SKILL.objects.get(id=i.skill_id)
                seeker_skills.append(skill_name)
        seeker_resume = ""
        if RESUME.objects.filter(user_id=user_id).exists():
            seeker_resume = RESUME.objects.get(user_id=user_id)
        skills = SKILL.objects.all()
        return render(request, 'jobPortalApp/pages/profile/seeker/add-edit-info.html', {'skills': skills, 'seeker_details': seeker_details, 'form': form, 'seeker_skills': seeker_skills, 'seeker_resume': seeker_resume, 'user_type': job_type,'profile':profile})


def providerEdit(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        user_type = request.session['job_type']
        profile = PROFILE.objects.filter(user_id=user_id)
        provider = COMPANY.objects.get(user_id=user_id)
        return render(request, 'jobPortalApp/pages/profile/provider/add-edit-info.html', {'provider': provider,'user_type':user_type,'profile':profile})


def providerAddJob(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        user_type = request.session['job_type']
        profile = PROFILE.objects.filter(user_id=user_id)
        provider = COMPANY.objects.get(user_id=user_id)
        skills = SKILL.objects.all()
        return render(request, 'jobPortalApp/pages/profile/provider/add-job.html', {'skills': skills,'user_type':user_type,'profile':profile,'provider':provider})

def providerDeactivateJob(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        if request.method == "POST":
            job_id = request.POST['job-id']
            JOB.objects.filter(id=job_id).update(status="Deactivated")
        return redirect('profile')

def providerActivateJob(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        if request.method == "POST":
            job_id = request.POST['job-id']
            JOB.objects.filter(id=job_id).update(status="Activated")
        return redirect('profile')


def providerEditJob(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        job_type = request.session['job_type']
        provider_details = COMPANY.objects.get(user_id=user_id)
        if request.method == "POST":
            job_id = request.POST['job-id']
            job = JOB.objects.get(id=job_id)
            job_skillnames_per_jobs = []
            job_skills_per_jobs = JOBSKILL.objects.filter(job_id=job_id)
            for job_skills_per_job in job_skills_per_jobs:
                skills = SKILL.objects.get(id=job_skills_per_job.skill_id)
                job_skillnames_per_jobs.append(skills.skillname)
            skills = SKILL.objects.all()
        return render(request, 'jobPortalApp/pages/profile/provider/edit-job.html', {'skills': skills, 'provider_details': provider_details, 'job_skills': job_skillnames_per_jobs, 'user_type': job_type, 'job': job})


def jobSearch(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        if request.method == "POST":
            job_search = request.POST['job-search']
            job_city = request.POST.get('job-city', False)
            job_country = request.POST.get('job-country', False)
            job_type = request.POST.get('job-type', False)
            request.session['job-search'] = job_search
            request.session['job-city'] = job_city
            request.session['job-type'] = job_type
            request.session['job-country'] = job_country

        return redirect('home')


def indexViewPost(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        job_type = request.session['job_type']
        user_id = request.session['user_id']
        user = User.objects.filter(id=user_id)
        profile = PROFILE.objects.filter(user_id=user_id)
        if request.method == "POST":
            id = request.POST['job-id']
            request.session['prev_job'] = id
            request.session.modified = True

        job_id = request.session['prev_job']
        job = JOB.objects.get(id=job_id)
        job_skillnames_per_jobs = []
        job_skills_per_jobs = JOBSKILL.objects.filter(job_id=job_id)
        for job_skills_per_job in job_skills_per_jobs:
            skills = SKILL.objects.get(id=job_skills_per_job.skill_id)
            job_skillnames_per_jobs.append(skills.skillname)
        if job_type == "Job Seeker":
            seeker_info = SEEKER.objects.get(user_id=user_id)
            resume = RESUME.objects.filter(user_id=user_id)
            seeker_skills = SEEKERSKILL.objects.filter(user_id=user_id)
            application_check = ""
            if APPLICATION.objects.filter(user_id=user_id, job_id=job_id).exists():
                application_check = "Already Applied"
            return render(request, 'JobPortalApp/pages/view-posted-job-as-seeker.html', {'job': job, 'job_skills': job_skillnames_per_jobs, 'seeker_info': seeker_info, 'resume': resume, 'seeker_skills': seeker_skills, 'application_check': application_check,'job_type':job_type,'user':user,'profile':profile})

        elif job_type == "Job Provider":
            provider_info = COMPANY.objects.get(user_id=user_id)
            return render(request, 'JobPortalApp/pages/view-posted-job-as-provider.html', {'job': job, 'job_skills': job_skillnames_per_jobs,'job_type':job_type,'provider_info':provider_info,'profile':profile})


def providerViewApplicantResume(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        company_id = request.session['user_id']
        profile = PROFILE.objects.filter(user_id=company_id)
        provider = COMPANY.objects.get(user_id=company_id)
        user_type = request.session['job_type']
        if request.method == "POST":
            job_type = request.session['job_type']
            user_id = request.session['user_id']
            applicant_id = request.POST['applicant-id']
            seeker_details = COMPANY.objects.get(user_id=user_id)
            seeker = RESUME.objects.get(user_id=applicant_id)
            return render(request, 'jobPortalApp/pages/profile/provider/view-resume.html', {'seeker': seeker, 'user_type': job_type, 'seeker_details': seeker_details,'profile':profile,'provider':provider,'user_type':user_type})


def providerViewApplicant(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        seeker = ""
        skillnames = []
        resume = ""
        user_id = ""
        company_id = request.session['user_id']
        profile = PROFILE.objects.filter(user_id=company_id)
        provider = COMPANY.objects.get(user_id=company_id)
        user_type = request.session['job_type']
        if request.method == "POST":
            user_id = request.POST['applicant-id']
            if SEEKER.objects.filter(user_id=user_id).exists():
                seeker = SEEKER.objects.get(user_id=user_id)
            if SEEKERSKILL.objects.filter(user_id=user_id).exists():
                seeker_skills = SEEKERSKILL.objects.filter(user_id=user_id)
                for seeker_skill in seeker_skills:
                    skill = SKILL.objects.get(id=seeker_skill.skill_id)
                    skillnames.append(skill.skillname)
            if RESUME.objects.filter(user_id=user_id).exists():
                resume = RESUME.objects.get(user_id=user_id)
        return render(request, 'JobPortalApp/pages/profile/provider/show-applicant.html', {'seeker': seeker, 'skillnames': skillnames, 'resume': resume,'user_type':user_type,'profile':profile,'provider':provider})


def providerViewPost(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        company_id = request.session['user_id']
        profile = PROFILE.objects.filter(user_id=company_id)
        provider = COMPANY.objects.get(user_id=company_id)
        user_type = request.session['job_type']
        if request.method == "POST":
            job_id = request.POST['job-id']
            job = JOB.objects.get(id=job_id)
            job_skillnames_per_jobs = []
            job_skills_per_jobs = JOBSKILL.objects.filter(job_id=job_id)
            applicants = []
            applicants_date = {}
            if APPLICATION.objects.filter(job_id=job_id).exists():
                applicant_ids = APPLICATION.objects.filter(job_id=job_id)
                for applicant_id in applicant_ids:
                    applicants.append(SEEKER.objects.filter(
                        user_id=applicant_id.user_id))
                    applicants_date[applicant_id.user_id] = applicant_ids
            for job_skills_per_job in job_skills_per_jobs:
                skills = SKILL.objects.get(id=job_skills_per_job.skill_id)
                job_skillnames_per_jobs.append(skills.skillname)

        return render(request, 'JobPortalApp/pages/profile/provider/show-job-post.html', {'job': job, 'job_skills': job_skillnames_per_jobs, 'applicants': applicants, 'applicants_date': applicants_date,'profile':profile,'provider':provider,'user_type':user_type})


def seekerEditProcess(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        if request.method == "POST":
            selected_skills = request.POST.getlist('skill')
            fullname = request.POST['fullname']
            about = request.POST['about']
            experience = request.POST['experience']
            resume = request.FILES.get('resume', False)
            if len(selected_skills) > 0:
                remove_skills = SEEKERSKILL.objects.filter(user_id=user_id)
                remove_skills.delete()
                for i in selected_skills:
                    SEEKERSKILL.objects.create(skill_id=i, user_id=user_id)

            SEEKER.objects.filter(user_id=user_id).update(fullname=fullname)
            SEEKER.objects.filter(user_id=user_id).update(about=about)
            SEEKER.objects.filter(user_id=user_id).update(
                experience=experience)
            if resume != False:
                refresh = RESUME.objects.filter(user_id=user_id)
                refresh.delete()
                object = RESUME.objects.create(user_id=user_id, resume=resume)
                object.save()
            ACTIVITY.objects.create(
                name="EDIT", description="Edited Seeker Information", user_id=user_id)
            return redirect('profile')


def providerAddJobProcess(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        if request.method == "POST":
            selected_skills = request.POST.getlist('skill')
            job_name = request.POST['job-name']
            job_description = request.POST['job-description']
            job_types = request.POST['job-types']
            salary = request.POST['salary']

            JOB.objects.create(name=job_name, description=job_description,
                               salary=salary, type=job_types, company_id=user_id,status="Activated")

            ACTIVITY.objects.create(
                name="POST", description="Posted New Job", user_id=user_id)
            job_id = (JOB.objects.last()).id
            if len(selected_skills) > 0:
                remove_skills = JOBSKILL.objects.filter(job_id=job_id)
                remove_skills.delete()

            seeker_emails_dict = {}
            for i in selected_skills:
                JOBSKILL.objects.create(skill_id=i, job_id=job_id)
                skillname = SKILL.objects.get(id=i)
                seeker_emails = []
                if SEEKERSKILL.objects.filter(skill_id=i).exists():
                    seeker_ids = SEEKERSKILL.objects.filter(skill_id=i)
                    for seeker_id in seeker_ids:
                        user_email = User.objects.get(id=seeker_id.user_id)
                        seeker_emails.append(user_email.email)
                seeker_emails_dict[skillname.skillname] = seeker_emails

            for keys, values in seeker_emails_dict.items():
                send_mail("Posted Job Met your Skills", "A job with required "+keys +
                          " skills has been posted in the job portal.", "creattjobportal@gmail.com", values, fail_silently=False)

            return redirect('profile')


def providerEditJobProcess(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        provider_details = COMPANY.objects.get(user_id=user_id)
        if request.method == "POST":
            selected_skills = request.POST.getlist('skill')
            job_name = request.POST['job-name']
            job_description = request.POST['job-description']
            job_types = request.POST['job-type']
            salary = request.POST['job-salary']
            job_id = request.POST['job-id']

            if len(selected_skills) > 0:
                job_skills = JOBSKILL.objects.filter(job_id=job_id)
                job_skills.delete()
            for selected_skill in selected_skills:
                JOBSKILL.objects.create(skill_id=selected_skill, job_id=job_id)
            JOB.objects.filter(id=job_id).update(name=job_name)
            JOB.objects.filter(id=job_id).update(description=job_description)
            JOB.objects.filter(id=job_id).update(type=job_types)
            JOB.objects.filter(id=job_id).update(salary=salary)

            ACTIVITY.objects.create(
                name="EDIT", description="Edited Job Detail/s", user_id=user_id)
            return redirect('profile')


def providerEditProcess(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        if request.method == "POST":
            name = request.POST['name']
            description = request.POST['description']
            city = request.POST.get('city', False)
            country = request.POST.get('country', False)
            COMPANY.objects.filter(user_id=user_id).update(name=name)
            COMPANY.objects.filter(user_id=user_id).update(
                description=description)
            if city != False:
                COMPANY.objects.filter(user_id=user_id).update(city=city)
            if country != False:
                COMPANY.objects.filter(user_id=user_id).update(country=country)
            ACTIVITY.objects.create(
                name="EDIT", description="Edited Company Information", user_id=user_id)
            return redirect('profile')


def fileupload(request):
    form = resumeForm(use_required_attribute=False)
    if request.method == 'POST':
        user_id = 1
        upload2 = request.FILES.get('resume', False)
        refresh = RESUME.objects.filter(user_id=user_id)
        refresh.delete()
        object = RESUME.objects.create(user_id=user_id, resume=upload2)
        object.save()
    return redirect('profile')


def filedisplay(request):

    object = RESUME.objects.all()
    return render(request, 'jobPortalApp/pages/profile/seeker/file-display.html', {'object': object})


def providerPost(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        check1 = COMPANY.objects.get(user_id=user_id)
        if request.method == "POST":
            selected_skills = request.POST.getlist('skills')
            fullname = request.POST['fullname']
            about = request.POST['about']
            experience = request.POST['experience']
            resume = request.FILES['resume']
        return render(request, 'jobPortalApp/pages/profile/provider/no-info.html')


def applyJob(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        if request.method == "POST":
            job_id = request.POST["job-id"]
            if APPLICATION.objects.filter(user_id=user_id, job_id=job_id).exists():
                request.session['prev_job'] = job_id
                return redirect('indexViewPost')
            else:
                request.session['prev_job'] = job_id
                APPLICATION.objects.create(user_id=user_id, job_id=job_id)
                return redirect('indexViewPost')


# maverick
def register(request):
    if request.method == 'POST':
        type = request.POST['user-type']
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                Message = "Email already Used"
                return render(request, 'jobPortalApp/pages/register.html', {'form': form, 'Message': Message})
            else:
                username = form.cleaned_data.get('username')
                form.save()
                user = User.objects.get(username=username)
                user_id = user.id
                if type == 'Job Seeker':
                    SEEKER.objects.create(user_id=user_id, username=username,status="Activated")
                    return redirect('login')
                elif type == 'Job Provider':
                    COMPANY.objects.create(user_id=user_id, username=username,status="Activated")
                    return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'jobPortalApp/pages/register.html', {'form': form})


def fileupload(request):
    form = resumeForm()
    if request.method == 'POST':
        user_id = 1
        upload2 = request.FILES.get('resume', False)
        refresh = RESUME.objects.filter(user_id=user_id)
        refresh.delete()
        object = RESUME.objects.create(user_id=user_id, resume=upload2)
        object.save()
    return redirect('profile')


def seekerChangeProfle(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        user_type = request.session['job_type']
        profile = PROFILE.objects.filter(user_id=user_id)
        seeker_details = SEEKER.objects.get(user_id=user_id)
        form = profileForm()
        profile = PROFILE.objects.filter(user_id=user_id)
        if request.method == 'POST':
            profile = request.FILES['profile']
            refresh = PROFILE.objects.filter(user_id=user_id)
            refresh.delete()
            object = PROFILE.objects.create(user_id=user_id, profile=profile)
            object.save()
            return redirect('seekerChangeProfle')
        return render(request, 'jobPortalApp/pages/profile/seeker/change-profile.html', {'form': form, 'profile': profile,'user_type':user_type,'seeker_details':seeker_details})


def providerChangeProfle(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        user_type = request.session['job_type']
        provider = COMPANY.objects.get(user_id=user_id)
        profile = PROFILE.objects.filter(user_id=user_id)
        form = profileForm()
        if request.method == 'POST':
            profile = request.FILES['profile']
            refresh = PROFILE.objects.filter(user_id=user_id)
            refresh.delete()
            object = PROFILE.objects.create(user_id=user_id, profile=profile)
            object.save()
            return redirect('providerChangeProfle')
        return render(request, 'jobPortalApp/pages/profile/provider/change-profile.html', {'form': form, 'profile': profile,'user_type':user_type,'provider':provider})


def seekerChangePassword(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        user_type = request.session['job_type']
        profile = PROFILE.objects.filter(user_id=user_id)
        seeker_details = SEEKER.objects.get(user_id=user_id)
        if request.method == 'POST':
            old_pass = request.POST['old_password']
            new_pass = request.POST['new_password']
            con_pass = request.POST['confirm_password']
            message = ""
            user = User.objects.get(id=user_id)
            if user.check_password(old_pass) == False:
                message = "Old password does not match in Database"
            if old_pass == new_pass:
                message = "New password is same with Old password"
            if new_pass != con_pass:
                message = "New password does not match Confirm password"
            is_non_empty = bool(message)
            if is_non_empty != False:
                return render(request, 'jobPortalApp/pages/profile/seeker/change-password.html', {'message': message})
            else:
                user.set_password(new_pass)
                user.save()
                return redirect('profile')
        return render(request, 'jobPortalApp/pages/profile/seeker/change-password.html',{'user_type':user_type,'profile':profile,'seeker_details':seeker_details})


def providerChangePassword(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        user_type = request.session['job_type']
        profile = PROFILE.objects.filter(user_id=user_id)
        provider = COMPANY.objects.get(user_id=user_id)
        if request.method == 'POST':
            old_pass = request.POST['old_password']
            new_pass = request.POST['new_password']
            con_pass = request.POST['confirm_password']
            message = ""
            user = User.objects.get(id=user_id)
            if user.check_password(old_pass) == False:
                message = "Old password doesn't match in Database"
            if old_pass == new_pass:
                message = "New password is same with Old password"
            if new_pass != con_pass:
                message = "New password doesn't match Confirm password"
            is_non_empty = bool(message)
            if is_non_empty != False:
                return render(request, 'jobPortalApp/pages/profile/provider/change-password.html', {'message': message})
            else:
                user.set_password(new_pass)
                user.save()
                return redirect('profile')
        return render(request, 'jobPortalApp/pages/profile/provider/change-password.html',{'user_type':user_type,'profile':profile,'provider':provider})

#markjoseph
def users_report(request):
    buff = io.Bytes.IO()
    canv = canvas.Canvas(buff, pagesize = letter, bottomup=0)
    text = canv.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont("Arial", 16)

    seeker = SEEKER.objects.all()
    users = []
    for user in seeker:
        users.append("List of Users")
        users.append(user.fullname)

    canv.drawText()
    canv.showPage()
    canv.save()
    buff.seek(0)

    return FileResponse(buff, as_attachment=True, filename='users.pdf')

def activity_report(request):
    buff = io.Bytes.IO()
    canv = canvas.Canvas(buff, pagesize = letter, bottomup=0)
    text = canv.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont("Arial", 16)

    activity = ACTIVITY.objects.all()
    activity_log = []
    for act in activity:
        activity_log.append("Activity Logs")
        activity_log.append(act.name)
        activity_log.append(act.user_id)

    canv.drawText()
    canv.showPage()
    canv.save()
    buff.seek(0)

    return FileResponse(buff, as_attachment=True, filename='activity-log.pdf')

def job_report(request):
    buff = io.Bytes.IO()
    canv = canvas.Canvas(buff, pagesize = letter, bottomup=0)
    text = canv.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont("Arial", 16)

    job = JOB.objects.all()
    job_list = []
    for jobs in job:
        job_list.append("Job List")
        job_list.append(jobs.name)
        job_list.append(jobs.description)
        job_list.append(jobs.type)
        job_list.append(jobs.salary)

    canv.drawText()
    canv.showPage()
    canv.save()
    buff.seek(0)

    return FileResponse(buff, as_attachment=True, filename='job-list.pdf')

def company_report(request):
    buff = io.Bytes.IO()
    canv = canvas.Canvas(buff, pagesize = letter, bottomup=0)
    text = canv.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont("Arial", 16)

    company = COMPANY.objects.all()
    company_list = []
    for comp in company:
        company_list.append("List of Companies")
        company_list.append(comp.name)
        company_list.append(comp.description)
        company_list.append(comp.city)
        company_list.append(comp.country)

    canv.drawText()
    canv.showPage()
    canv.save()
    buff.seek(0)

    return FileResponse(buff, as_attachment=True, filename='company-list.pdf')


def filedisplay(request):

    object = RESUME.objects.all()
    return render(request, 'jobPortalApp/pages/profile/seeker/file-display.html', {'object': object})
