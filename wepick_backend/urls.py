from django.urls import path, include

urlpatterns = [
    path('account', include('account.urls')),
    path('job', include('job.urls')),
    path('company', include('company.urls')),
    path('resume', include('resume.urls')),
    ]
