from django.urls import path
from .views      import (
    RegionView, 
    CompanyListView, 
    CompanyDetailView,
    FollowView
)

urlpatterns = [
    path('/region', RegionView.as_view(), name='region'),
    path('/list', CompanyListView.as_view(), name='company_list'),
    path('/<int:company_id>', CompanyDetailView.as_view(), name='company'),
    path('/follow', FollowView.as_view(), name='follow')
]