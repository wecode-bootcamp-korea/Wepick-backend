from django.urls import path
from .views      import (
    CategoryView, 
    CategoryTabView, 
    JobListView, 
    JobListCategoryView, 
    JobDetailView
)

urlpatterns = [
    path('/category', CategoryView.as_view(), name='category'),
    path('/category/<int:main_category_id>', CategoryTabView.as_view(), name='category_tab'),
    path('/list', JobListView.as_view(), name='job_list_all'),
    path('/list/<int:sub_category_id>', JobListCategoryView.as_view(), name='job_list_category'),
    path('/<int:job_id>', JobDetailView.as_view(), name='job_detail'),

]