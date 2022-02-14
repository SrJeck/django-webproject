from unicodedata import name
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name="home"),
    path('', views.redirectLogin, name="redirectLogin"),
    path('creatt/', views.index),
    path('home/apply-job', views.applyJob, name="applyJob"),
    path('job-search/', views.jobSearch, name="jobSearch"),
]


# benitez
# for job seeker profile
urlpatterns += [
    path('seeker-info/', views.seeker_no_info, name="seeker_no_info"),
]
# maverick
# register
urlpatterns += [
    path('register/', views.register, name="register"),
]

# jack
# seeker
urlpatterns += [
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('profile/seeker-edit-profile', views.seekerEdit, name="seekerEdit"),
    path('profile/seeker-change-profile',views.seekerChangeProfle, name="seekerChangeProfle"),
    path('profile/seeker-change-password',views.seekerChangePassword, name="seekerChangePassword"),
    path('seeker-resume/', views.seekerView, name="seekerView"),
    path('profile/seeker-edit-process',views.seekerEditProcess, name="seekerEditProcess"),
    
]

# provider
urlpatterns += [
    path('profile/provider-change-profile',views.providerChangeProfle, name="providerChangeProfle"),
    path('profile/provider-change-password',views.providerChangePassword, name="providerChangePassword"),
    path('profile/provider-edit-profile',views.providerEdit, name="providerEdit"),
    path('profile/provider-edit-process',views.providerEditProcess, name="providerEditProcess"),
    path('profile/provider-add-job', views.providerAddJob, name="providerAddJob"),
    path('profile/provider-add-job-process',views.providerAddJobProcess, name="providerAddJobProcess"),
    path('profile/view-post/', views.providerViewPost, name="providerViewPost"),
    path('profile/view-applicant', views.providerViewApplicant,name="providerViewApplicant"),
    path('profile/view-applicant-resume', views.providerViewApplicantResume,name="providerViewApplicantResume"),
    path('home/view-post/', views.indexViewPost, name="indexViewPost"),
    path('profile/provider-edit-job',views.providerEditJob, name="providerEditJob"),
    path('profile/provider-edit-job-process',views.providerEditJobProcess, name="providerEditJobProcess"),
]
# mohammed
# administrator
urlpatterns += [
    path('manage_user/', views.manage_user, name="manage_user"),
    path('manage_user/edit_user', views.admin_edit_user, name="admin_edit_user"),
    path('manage_user/activate_user', views.admin_activate_user, name="admin_activate_user"),
    path('manage_user/deactivate_user', views.admin_deactivate_user, name="admin_deactivate_user"),
    path('company/', views.company, name="company"),
    path('company/edit_company', views.admin_edit_company, name="admin_edit_company"),
    path('company/activate_company', views.admin_deactivate_company, name="admin_deactivate_company"),
    path('company/deactivate_company', views.admin_activate_company, name="admin_activate_company"),
    path('jobs/', views.jobs, name="jobs"),
    path('jobs/edit_job', views.admin_edit_jobs, name="admin_edit_jobs"),
    path('jobs/activate_job', views.admin_activate_jobs, name="admin_activate_jobs"),
    path('jobs/deactivate_job', views.admin_deactivate_jobs, name="admin_deactivate_jobs"),
    path('activity_logs/', views.activity_logs, name="activity_logs"),
]
# lowell
# for Company/Job Provider
urlpatterns += {
    path('provider-no-info/', views.provider_no_info, name="provider_no_info"),
    path('provider-with-info/', views.provider_with_info,
         name="provider_with_info"),

    path('provider-edit-info/', views.provider_edit_info,
         name="provider_edit_info"),

    path('fileupload/', views.fileupload, name="fileupload"),
    path('filedisplay/', views.filedisplay, name="filedisplay"),
    path('provider-show-job-post/', views.provider_show_job_post,
         name="provider_show_job_post"),
    path('provider-edit-job-post/', views.provider_edit_job,
         name="provider_edit_job_post"),

    path('provider-show-applicant/', views.provider_show_applicant,
         name="provider_show_applicant"),

}
