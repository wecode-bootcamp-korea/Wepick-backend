import json
from django.views import View
from django.http  import HttpResponse, JsonResponse

from company.models import (
    Country, 
    Region, 
    Company, 
    Photo, 
    News
)

from job.models     import (
    MainCategory, 
    SubCategory, 
    Job
)

class RegionView(View):
    def get(self, request):
        query          = request.GET.get('country_id', None)
        filtering_data = {}
        if query:
            filtering_data['country_id'] = query
        
        if Region.objects.filter(**filtering_data).exists():
            regions = Region.objects.filter(**filtering_data)
        
            data = [{
                'id'   : region.id,
                'name' : region.name
            } for region in regions]

            return JsonResponse({'data' : data}, status=200)

        return JsonResponse({'message' : "INVALID_COUNTRY"}, status=400)


class CompanyListView(View):
    def get(self, request):
        COMPANY_LIMIT = 5
        companies = Company.objects.all()[:COMPANY_LIMIT]

        data = [{
            'id'               : company.id,
            'name'             : company.name,
            'logo_url'         : company.logo_url,
            'thumbnail_url'    : company.thumbnail_url,
            'number_positions' : company.job_set.count()
        } for company in companies]
    
        return JsonResponse({'data' : data}, status=200)

class CompanyDetailView(View):
    def get(self, request, company_id):
        try:
            company = Company.objects.get(id = company_id)

            data = [{
                'id'         : company.id,
                'name'       : company.name,
                'logo_url'   : company.logo_url,
                'article'    : company.article,
                'salary_new' : company.salary_new,
                'salary_all' : company.salary_all,
                'employees'  : company.employees,
                'images' : [{
                    'name' : photo.name,
                    'url'  : photo.url
                } for photo in company.photo_set.all()],
                'news' : [{
                    'name'   : news.name,
                    'source' : news.source,
                    'url'    : news.link_url,
                } for news in company.news_set.all()],
                'jobs' : [{
                    'name'          : job.name,
                    'reward_amount' : job.reward_amount,
                    'deadline'      : job.deadline,
                    'likes'         : job.likes.count(),
                } for job in company.job_set.all()]
            }]
        
            return JsonResponse({'data' : data}, status=200)
        
        except Company.DoesNotExist:
            return JsonResponse({'message' : "INVALID_COMPANY"}, status=400)