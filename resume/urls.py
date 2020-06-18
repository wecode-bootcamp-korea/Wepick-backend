from django.urls import path, include
from .views      import (
   ResumeListView, 
   ResumeDetailView, 
)

urlpatterns = [
    path('/list', ResumeListView.as_view()),
    path('/detail/<int:resume_id>', ResumeDetailView.as_view()),
]
