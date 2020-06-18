from django.urls import path

from .views      import (
    EmailCheckView, 
    SignInView, 
    SignUpView, 
    SocialLoginView, 
    JobCategoryView, 
    CareerView, 
    ProfileView,
    MyPageMainView,
    MyPageLikeView,
    MyPageBookmarkView,
    MyPageApplyView
)

urlpatterns = [
    path('/emailcheck', EmailCheckView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/sociallogin', SocialLoginView.as_view()),
    path('/jobcategory', JobCategoryView.as_view()),
    path('/career', CareerView.as_view()),
    path('/profile', ProfileView.as_view()),
    path('/mypage', MyPageMainView.as_view(), name='mypage_main'),
    path('/mypage/like', MyPageLikeView.as_view(), name='mypage_like'),
    path('/mypage/bookmark', MyPageBookmarkView.as_view(), name='mypage_bookmark'),
    path('/mypage/apply', MyPageApplyView.as_view(), name='mypage_apply'),
]
