import json

from django.db.models import Q
from django.views     import View
from django.http      import HttpResponse, JsonResponse
from django.db        import IntegrityError

from account.views  import login_required
from company.models import (
    Country, 
    Region, 
    Company, 
    Photo, 
    News,
    Follow
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


class FollowView(View):
    @login_required
    def post(self, request):
        account_id = request.user.id
        
        try:
            company_id = request.GET.get('company_id', None)

            if Follow.objects.filter(Q(account_id = account_id)&Q(company_id = company_id)).exists():
                follow = Follow.objects.get(Q(account_id = account_id)&Q(company_id = company_id))
                
                follow.is_follow = False if follow.is_follow else True                
                follow.save()
            
            else:
                Follow.objects.create(
                    account_id = account_id,
                    company_id = company_id,
                    is_follow = True
                )

            return HttpResponse(status = 200)            
        except IntegrityError:
            return JsonResponse({'message':'Invalid Account or Company'}, status=400)
        except KeyError:
            return HttpResponse(status = 400)
    
    @login_required
    def get(self, request):
        #import pdb; pdb.set_trace()
        try:
            account_id = request.user.id
            company_id = request.GET.get('company_id', None)

            if Follow.objects.filter(Q(account_id = account_id)&Q(company_id = company_id)).exists():
                follow = Follow.objects.get(Q(account_id = account_id)&Q(company_id = company_id))
                return JsonResponse({'is_follow' : follow.is_follow}, status = 200)
            
            return JsonResponse({'message' : "Invalid Follow"}, status = 400)

        except KeyError:
            return HttpResponse(status = 400)



