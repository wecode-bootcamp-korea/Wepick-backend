
from django.urls import path, include

urlpatterns = [
    path('account', include('account.urls')),
    path('resume', include('resume.urls')),
    path('company', include('company.urls')),
    path('job', include('job.urls')),
]
