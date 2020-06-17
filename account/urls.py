from django.urls import path
from .views      import (
    EmailCheckView, 
    SignInView, 
    SignUpView, 
    SocialLoginView, 
    JobCategoryView, 
    CareerView, 
    ProfileView
)
urlpatterns = [
    path('/emailcheck', EmailCheckView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/sociallogin', SocialLoginView.as_view()),
    path('/jobcategory', JobCategoryView.as_view()),
    path('/career', CareerView.as_view()),
    path('/profile', ProfileView.as_view()),
]
