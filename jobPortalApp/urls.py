from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('creatt/', views.index),
]

# benitez
# for job seeker profile
urlpatterns += [
    path('seeker-info/', views.seeker_no_info, name="seeker_no_info"),
]


from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('creatt/', views.index),
]

# benitez
# for job seeker profile
urlpatterns += [
    path('seeker-info/', views.seeker_no_info, name="seeker_no_info"),
]


# mohammed
# administrator
urlpatterns += [
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
]


# lowell
# for Company/Job Provider
urlpatterns += {
    path('provider-no-info/', views.provider_no_info, name="provider_no_info"),
    path('provider-with-info/', views.provider_with_info, name="provider_with_info"),

    path('provider-edit-info/', views.provider_edit_info, name="provider_edit_info"),

    path('provider-show-job-post/', views.provider_show_job_post, name="provider_show_job_post"),
    path('provider-edit-job-post/', views.provider_edit_job, name="provider_edit_job_post"),

    path('provider-show-applicant/', views.provider_show_applicant, name="provider_show_applicant"),

}

