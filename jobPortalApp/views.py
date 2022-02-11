from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.views.decorators.clickjacking import xframe_options_sameorigin


# Create your views here.
def index(request):
    return render(request, "jobPortalApp/index.html")

def redirectLogin(request):
    return redirect('login')

def home(request):
    # return HttpResponse('Home Page')
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        job_title = request.session['job_type']
        user_id = request.session['user_id']
        provider_name = ""
        seeker_name = ""
        if job_title == "Job Seeker":
            seeker_name = SEEKER.objects.get(user_id=user_id)
        elif job_title == "Job Provider":
            provider_name = COMPANY.objects.get(user_id=user_id)
        
        # request.session['job-search'] = job_search
        #         request.session['job-city'] = job_city
        #         request.session['job-country'] = job_country
        #         request.session['job-type'] = job_type
        job_search = request.session['job-search']
        job_type = request.session['job-type']
        job_country = request.session['job-country']
        job_city = request.session['job-city']
        is_non_empty = bool(job_search)
        jobs = []
        company_jobs_ids = []
        skillnames_per_jobs = {}
        applications_per_jobs = {}
        searcher = ""
        # search city country type
        if is_non_empty != False and job_city != False and job_country != False and job_type != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city,country=job_country).exists():
                company_ids = COMPANY.objects.filter(city=job_city,country=job_country)
            if JOB.objects.filter(name__contains=job_search).exists():
                for company_id in company_ids:
                    filtered_jobs = JOB.objects.filter(name__contains=job_search,company_id=company_id.user_id,type=job_type)
                    jobs.append(JOB.objects.filter(name__contains=job_search,company_id=company_id.user_id,type=job_type))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(id=job_id.job_id,company_id=company_id.user_id,type=job_type))
                            filtered_jobs = JOB.objects.filter(id=job_id.job_id,company_id=company_id.user_id,type=job_type)
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " " + job_type + " in " + job_country + " - " + job_city 
        # search city type
        elif is_non_empty != False and job_type != False and job_city != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city).exists():
                company_ids = COMPANY.objects.filter(city=job_city)
            if JOB.objects.filter(name__contains=job_search,type=job_type).exists():
                for company_id in company_ids:
                    filtered_jobs = JOB.objects.filter(name__contains=job_search,type=job_type,company_id=company_id.user_id)
                    jobs.append(JOB.objects.filter(name__contains=job_search,type=job_type,company_id=company_id.user_id))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(id=job_id.job_id,type=job_type,company_id=company_id.user_id))
                            filtered_jobs = JOB.objects.filter(id=job_id.job_id,type=job_type,company_id=company_id.user_id)
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search+ " " + job_type + " in " + job_city
        # search city country
        elif is_non_empty != False and job_country != False and job_city != False:
            company_ids = ""
            if COMPANY.objects.filter(country=job_country,city=job_city).exists():
                company_ids = COMPANY.objects.filter(country=job_country,city=job_city)
            if JOB.objects.filter(name__contains=job_search).exists():
                for company_id in company_ids:
                    filtered_jobs = JOB.objects.filter(name__contains=job_search,company_id=company_id.user_id)
                    jobs.append(JOB.objects.filter(name__contains=job_search,company_id=company_id.user_id))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(id=job_id.job_id,company_id=company_id.user_id))
                            filtered_jobs = JOB.objects.filter(id=job_id.job_id,company_id=company_id.user_id)
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " in " + job_country + " - " + job_city
        # search country type
        elif is_non_empty != False and job_type != False and job_country != False:
            company_ids = ""
            if COMPANY.objects.filter(country=job_country).exists():
                company_ids = COMPANY.objects.filter(country=job_country)
            if JOB.objects.filter(name__contains=job_search,type=job_type).exists():
                for company_id in company_ids:
                    filtered_jobs = JOB.objects.filter(name__contains=job_search,type=job_type,company_id=company_id.user_id)
                    jobs.append(JOB.objects.filter(name__contains=job_search,type=job_type,company_id=company_id.user_id))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(id=job_id.job_id,type=job_type,company_id=company_id.user_id))
                            filtered_jobs = JOB.objects.filter(id=job_id.job_id,type=job_type,company_id=company_id.user_id)
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " " + job_type + " in " + job_country
        # type city country
        elif job_city != False and job_country != False and job_type != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city,country=job_country).exists():
                company_ids = COMPANY.objects.filter(city=job_city,country=job_country)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(type=job_type,company_id=company_id.user_id))
                    filtered_jobs = JOB.objects.filter(type=job_type,company_id=company_id.user_id)
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
                    filtered_jobs = JOB.objects.filter(name__contains=job_search,company_id=company_id.user_id)
                    jobs.append(JOB.objects.filter(name__contains=job_search,company_id=company_id.user_id))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(id=job_id.job_id,company_id=company_id.user_id))
                            filtered_jobs = JOB.objects.filter(id=job_id.job_id,company_id=company_id.user_id)
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
                    filtered_jobs = JOB.objects.filter(name__contains=job_search,company_id=company_id.user_id)
                    jobs.append(JOB.objects.filter(name__contains=job_search,company_id=company_id.user_id))
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        for company_id in company_ids:
                            jobs.append(JOB.objects.filter(id=job_id.job_id,company_id=company_id.user_id))
                            filtered_jobs = JOB.objects.filter(id=job_id.job_id,company_id=company_id.user_id)
                            for filtered_job in filtered_jobs:
                                company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " in " + job_city 
        # search type
        elif is_non_empty != False and job_type != False:
            if JOB.objects.filter(name__contains=job_search,type=job_type).exists():
                jobs.append(JOB.objects.filter(name__contains=job_search,type=job_type))
                filtered_jobs = JOB.objects.filter(name__contains=job_search,type=job_type)
                for filtered_job in filtered_jobs:
                    company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        jobs.append(JOB.objects.filter(id=job_id.job_id,type=job_type))
                        filtered_jobs = JOB.objects.filter(id=job_id.job_id,type=job_type)
                        for filtered_job in filtered_jobs:
                            company_jobs_ids.append(filtered_job.id)
            searcher = job_search + " " + job_type
        # city country
        elif job_city != False and job_country != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city,country=job_country).exists():
                company_ids = COMPANY.objects.filter(city=job_city,country=job_country)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(company_id=company_id.user_id))
                    filtered_jobs = JOB.objects.filter(company_id=company_id.user_id)
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher = "Jobs in " + job_country + " - " + job_city 
        # city type
        elif job_city != False and job_type != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city).exists():
                company_ids = COMPANY.objects.filter(city=job_city)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(company_id=company_id.user_id,type=job_type))
                    filtered_jobs = JOB.objects.filter(company_id=company_id.user_id,type=job_type)
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher = job_type+" in " + job_city 
        # type country
        elif job_type != False and job_country != False:
            company_ids = ""
            if COMPANY.objects.filter(country=job_country).exists():
                company_ids = COMPANY.objects.filter(country=job_country)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(company_id=company_id.user_id,type=job_type))
                    filtered_jobs = JOB.objects.filter(company_id=company_id.user_id,type=job_type)
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher =  job_type+" in " + job_country
        # city
        elif job_city != False:
            company_ids = ""
            if COMPANY.objects.filter(city=job_city).exists():
                company_ids = COMPANY.objects.filter(city=job_city)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(company_id=company_id.user_id))
                    filtered_jobs = JOB.objects.filter(company_id=company_id.user_id)
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher = "Jobs in " + job_city
        # country
        elif job_country != False:
            company_ids = ""
            if COMPANY.objects.filter(country=job_country).exists():
                company_ids = COMPANY.objects.filter(country=job_country)
                for company_id in company_ids:
                    jobs.append(JOB.objects.filter(company_id=company_id.user_id))
                    filtered_jobs = JOB.objects.filter(company_id=company_id.user_id)
                    for filtered_job in filtered_jobs:
                        company_jobs_ids.append(filtered_job.id)
            searcher = "Jobs in " + job_country
        # type
        elif job_type != False:
            if JOB.objects.filter(type=job_type).exists():
                jobs.append(JOB.objects.filter(type=job_type))
                filtered_jobs = JOB.objects.filter(type=job_type)
                for filtered_job in filtered_jobs:
                    company_jobs_ids.append(filtered_job.id)
            searcher = job_type
        # search
        elif is_non_empty != False:
            if JOB.objects.filter(name__contains=job_search).exists():
                jobs.append(JOB.objects.filter(name__contains=job_search))
                filtered_jobs = JOB.objects.filter(name__contains=job_search)
                for filtered_job in filtered_jobs:
                    company_jobs_ids.append(filtered_job.id)
            else:
                if SKILL.objects.filter(skillname=job_search).exists():
                    skillname = SKILL.objects.get(skillname=job_search)
                    job_ids = JOBSKILL.objects.filter(skill_id=skillname.id)
                    for job_id in job_ids:
                        jobs.append(JOB.objects.filter(id=job_id.job_id))
                        filtered_jobs = JOB.objects.filter(id=job_id.job_id)
                        for filtered_job in filtered_jobs:
                            company_jobs_ids.append(filtered_job.id)
            searcher = job_search

        for company_jobs_id in company_jobs_ids:
            job_skillnames_per_jobs = []
            job_skills_per_jobs = JOBSKILL.objects.filter(job_id=company_jobs_id)
            for job_skills_per_job in job_skills_per_jobs:
                skills = SKILL.objects.get(id=job_skills_per_job.skill_id)
                job_skillnames_per_jobs.append(skills.skillname)
            skillnames_per_jobs[company_jobs_id] = job_skillnames_per_jobs
        return render(request,'jobPortalApp/pages/index.html',{'jobs':jobs,'skillnames_per_jobs':skillnames_per_jobs,'searcher':searcher,'seeker_name':seeker_name,'provider_name':provider_name,'user_type':job_title,'job_search':job_search,'job_type':job_type,'job_city':job_city,'job_country':job_country})


# job seeker
def seeker_no_info(request):
    return render(request, "jobPortalApp/pages/profile/seeker/no-info.html")

# admin


def admin_dashboard(request):
    return render(request, "jobPortalApp/admin/admin_dashboard.html")


def manage_user(request):
    seeker = SEEKER.objects.all() 
    return render(request, 'jobPortalApp/admin/manage_user.html',{'seeker':seeker})   
    #return render(request, "jobPortalApp/admin/manage_user.html")


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

def logout(request):
    del request.session['user_id']
    del request.session['user_type']
    del request.session['job_type']
    request.session.modified = True
    return redirect( "login")

def login(request):
    if request.method == 'POST':
        usermail = request.POST['usermail']
        password = request.POST['password']
        if User.objects.filter(username=usermail).exists():
            user = User.objects.get(username=usermail)
            user_id = user.id
            if user.check_password(password):
                if SEEKER.objects.filter(user_id=user_id).exists():
                    request.session['user_id'] = user_id
                    request.session['user_type'] = "seeker"
                    request.session['job_type'] = "Job Seeker"
                elif COMPANY.objects.filter(user_id=user_id).exists():
                    request.session['user_id'] = user_id
                    request.session['user_type'] = "provider"
                    request.session['job_type'] = "Job Provider"
                return redirect('profile')
            else:
                message = "Wrong Password"
                return render(request, 'jobPortalApp/pages/login.html',{'message':message})
        elif User.objects.filter(email=usermail).exists():
            user = User.objects.get(username=usermail)
            user_id = user.id
            if user.check_password(password):
                if SEEKER.objects.filter(user_id=user_id).exists():
                    request.session['usermail'] = usermail
                    request.session['user_type'] = "seeker"
                    request.session['job_type'] = "Job Seeker"
                elif COMPANY.objects.filter(user_id=user_id).exists():
                    request.session['usermail'] = usermail
                    request.session['user_type'] = "provider"
                    request.session['job_type'] = "Job Provider"
                return redirect('profile')
            else:
                message = "Wrong Password"
                return render(request, 'jobPortalApp/pages/login.html',{'message':message})
        else:
            message = "Wrong Email or Username"
            return render(request, 'jobPortalApp/pages/login.html',{'message':message})

    return render(request, "jobPortalApp/pages/login.html")

def profile(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        job_type = request.session['job_type']
        user_details = User.objects.get(id=user_id)
        if user_type == 'seeker':
            if SEEKER.objects.filter(user_id=user_id).exists():
                seeker_skills = []
                if SEEKERSKILL.objects.filter(user_id=user_id).exists():
                    seeker_skills_id = SEEKERSKILL.objects.filter(user_id=user_id)
                    for i in seeker_skills_id:
                        skill_name = SKILL.objects.get(id=i.skill_id)
                        seeker_skills.append(skill_name)
                seeker_details = SEEKER.objects.get(user_id=user_id)
                seeker_resume = RESUME.objects.get(user_id=user_id)
                return render(request,'jobPortalApp/pages/profile/seeker/with-info.html',{'user_details':user_details,'seeker_details':seeker_details,'seeker_skills':seeker_skills,'user_type':job_type,'seeker_resume':seeker_resume})
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
                    job_skills_per_jobs = JOBSKILL.objects.filter(job_id=company_jobs_id)
                    for job_skills_per_job in job_skills_per_jobs:
                        skills = SKILL.objects.get(id=job_skills_per_job.skill_id)
                        job_skillnames_per_jobs.append(skills.skillname)
                    skillnames_per_jobs[company_jobs_id] = job_skillnames_per_jobs     
                return render(request,'jobPortalApp/pages/profile/provider/with-info.html',{'company_details':company_details,'user_details':user_details,'user_type':job_type,'company_jobs':company_jobs,'skillnames_per_jobs':skillnames_per_jobs})

@xframe_options_sameorigin
def seekerView(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        job_type = request.session['job_type']
        seeker_details = SEEKER.objects.get(user_id=user_id)
        seeker = RESUME.objects.get(user_id=user_id)
        return render(request,'jobPortalApp/pages/profile/seeker/view-resume.html',{'seeker':seeker,'user_type':job_type,'seeker_details':seeker_details})

def seekerEdit(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        job_type = request.session['job_type']
        seeker = SEEKER.objects.get(user_id=user_id)
        form = resumeForm(use_required_attribute=False)
        seeker_skills = []
        if SEEKERSKILL.objects.filter(user_id=user_id).exists():
            seeker_skills_id = SEEKERSKILL.objects.filter(user_id=user_id)
            for i in seeker_skills_id:
                skill_name = SKILL.objects.get(id=i.skill_id)
                seeker_skills.append(skill_name)
        seeker_details = SEEKER.objects.get(user_id=user_id)
        seeker_resume = RESUME.objects.get(user_id=user_id)
        skills = SKILL.objects.all()
        return render(request,'jobPortalApp/pages/profile/seeker/add-edit-info.html',{'skills':skills,'seeker_details':seeker_details,'form':form,'seeker_skills':seeker_skills,'seeker_resume':seeker_resume,'user_type':job_type})

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
                        SEEKERSKILL.objects.create(skill_id=i,user_id=user_id)
                
                SEEKER.objects.filter(user_id=user_id).update(fullname=fullname)
                SEEKER.objects.filter(user_id=user_id).update(about=about)
                SEEKER.objects.filter(user_id=user_id).update(experience=experience)
                if resume != False:
                    refresh = RESUME.objects.filter(user_id=user_id)
                    refresh.delete()
                    object = RESUME.objects.create(user_id=user_id,resume=resume)
                    object.save()
                return redirect('profile')

def providerEdit(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        provider = COMPANY.objects.get(user_id=user_id)
        return render(request,'jobPortalApp/pages/profile/provider/add-edit-info.html',{'provider':provider})

def providerAddJob(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        skills = SKILL.objects.all()
        return render(request,'jobPortalApp/pages/profile/provider/add-job.html',{'skills':skills})

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
            if  APPLICATION.objects.filter(user_id=user_id,job_id=job_id).exists():
                application_check = "Already Applied"
            return render(request,'JobPortalApp/pages/view-posted-job-as-seeker.html',{'job':job,'job_skills':job_skillnames_per_jobs,'seeker_info':seeker_info,'resume':resume,'seeker_skills':seeker_skills,'application_check':application_check})

        elif job_type == "Job Provider":
            provider_info = COMPANY.objects.get(user_id=user_id)
            return render(request,'JobPortalApp/pages/view-posted-job-as-provider.html',{'job':job,'job_skills':job_skillnames_per_jobs})

def providerViewPost(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        if request.method == "POST":
            job_id = request.POST['job-id']
            job = JOB.objects.get(id=job_id)
            job_skillnames_per_jobs = []
            job_skills_per_jobs = JOBSKILL.objects.filter(job_id=job_id)
            for job_skills_per_job in job_skills_per_jobs:
                skills = SKILL.objects.get(id=job_skills_per_job.skill_id)
                job_skillnames_per_jobs.append(skills.skillname)
            
        return render(request,'JobPortalApp/pages/profile/provider/show-job-post.html',{'job':job,'job_skills':job_skillnames_per_jobs})

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
        return render(request,'jobPortalApp/pages/profile/provider/edit-job.html',{'skills':skills,'provider_details':provider_details,'job_skills':job_skillnames_per_jobs,'user_type':job_type,'job':job})

def providerEditJobProcess(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        provider_details = COMPANY.objects.get(user_id=user_id)
        if request.method == "POST":
            job_id = request.POST['job-id']
            job_type = request.session['job_type']
            job = JOB.objects.get(id=job_id)
            job_skills = []
            if JOBSKILL.objects.filter(job_id=job_id).exists():
                job_skills_ids = JOBSKILL.objects.filter(job_id=job_id)
                for job_skills_id in job_skills_ids:
                    skill_name = SKILL.objects.get(id=job_skills_id.skill_id)
                    job_skills.append(skill_name)
            skills = SEEKER.objects.all()
            return render(request,'jobPortalApp/pages/profile/provider/edit-job.html',{'skills':skills,'provider_details':provider_details,'job_skills':job_skills,'user_type':job_type,'job':job})

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
                
                JOB.objects.create(name=job_name,description=job_description,salary=salary,type=job_types,company_id=user_id)
                job_id = (JOB.objects.last()).id
                if len(selected_skills) > 0:
                    remove_skills = JOBSKILL.objects.filter(job_id=job_id)
                    remove_skills.delete()
                for i in selected_skills:
                   JOBSKILL.objects.create(skill_id=i,job_id=job_id)
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
            COMPANY.objects.filter(user_id=user_id).update(description=description)
            if city != False:
                COMPANY.objects.filter(user_id=user_id).update(city=city)
            if country != False:
                COMPANY.objects.filter(user_id=user_id).update(country=country)
            return redirect('profile')

            
def fileupload(request):
    form = resumeForm(use_required_attribute=False)
    if request.method=='POST':  
            user_id = 1   
            upload2=request.FILES.get('resume', False)
            refresh = RESUME.objects.filter(user_id=user_id)
            refresh.delete()
            object = RESUME.objects.create(user_id=user_id,resume=upload2)
            object.save()
    return redirect('profile')

def filedisplay(request):
    
    object = RESUME.objects.all()
    return render(request,'jobPortalApp/pages/profile/seeker/file-display.html',{'object':object})


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
        return render(request,'jobPortalApp/pages/profile/provider/no-info.html')
def applyJob(request):
    if 'user_id' not in request.session:
        return redirect('login')
    else:
        user_id = request.session['user_id']
        if request.method == "POST":
            job_id = request.POST["job-id"]
            if  APPLICATION.objects.filter(user_id=user_id,job_id=job_id).exists():
                request.session['prev_job'] = job_id
                return redirect('indexViewPost')
            else:
                request.session['prev_job'] = job_id
                APPLICATION.objects.create(user_id=user_id,job_id=job_id)
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
                return render(request, 'jobPortalApp/pages/register.html',{'form':form,'Message':Message})
            else:
                username = form.cleaned_data.get('username')
                form.save()
                user = User.objects.get(username=username)
                user_id = user.id
                if type == 'Job Seeker':
                    SEEKER.objects.create(user_id=user_id,username=username)
                    return redirect('login')
                elif type == 'Job Provider':
                    COMPANY.objects.create(user_id=user_id,username=username)
                    return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'jobPortalApp/pages/register.html',{'form':form})


def fileupload(request):
    form = resumeForm(use_required_attribute=False)
    if request.method=='POST':  
            user_id = 1   
            upload2=request.FILES.get('resume', False)
            refresh = RESUME.objects.filter(user_id=user_id)
            refresh.delete()
            object = RESUME.objects.create(user_id=user_id,resume=upload2)
            object.save()
    return redirect('profile')

def filedisplay(request):
    
    object = RESUME.objects.all()
    return render(request,'jobPortalApp/pages/profile/seeker/file-display.html',{'object':object})
