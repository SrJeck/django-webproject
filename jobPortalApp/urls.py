from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name="Home"),
    path('creatt/', views.index),
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
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('profile/seeker-edit-profile', views.seekerEdit, name="seekerEdit"),
    path('profile/seeker-edit-process', views.seekerEditProcess, name="seekerEditProcess"),
    path('seeker-resume/', views.seekerView, name="seekerView"),
    path('profile/provider-edit-profile', views.providerEdit, name="providerEdit"),
    path('profile/provider-edit-process', views.providerEditProcess, name="providerEditProcess"),
    path('profile/provider-add-job', views.providerAddJob, name="providerAddJob"),
    path('profile/seeker-add-job-process', views.providerAddJobProcess, name="providerAddJobProcess"),
    path('fileupload/', views.fileupload, name="fileupload"),
    path('filedisplay/', views.filedisplay, name="filedisplay"),
]
# mohammed
# administrator
urlpatterns += [
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('manage_user/', views.manage_user, name="manage_user"),
    path('company/', views.company, name="company"),
    path('jobs/', views.jobs, name="jobs"),
]
# lowell
# for Company/Job Provider
urlpatterns += {
    path('provider-no-info/', views.provider_no_info, name="provider_no_info"),
    path('provider-with-info/', views.provider_with_info,
         name="provider_with_info"),

    path('provider-edit-info/', views.provider_edit_info,
         name="provider_edit_info"),

    path('provider-show-job-post/', views.provider_show_job_post,
         name="provider_show_job_post"),
    path('provider-edit-job-post/', views.provider_edit_job,
         name="provider_edit_job_post"),

    path('provider-show-applicant/', views.provider_show_applicant,
         name="provider_show_applicant"),

}
