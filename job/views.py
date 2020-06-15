import json
from django.views   import View
from django.http    import HttpResponse, JsonResponse

from company.models import Company
from job.models     import (
    MainCategory, 
    SubCategory, 
    Job
)


class CategoryView(View):
    def get(self, request):
        main_categories = MainCategory.objects.all().order_by('id')

        data = [{
            'id'   : main_category.id,
            'name' : main_category.name,
            'background_image' : main_category.image_url,
            'sub_category' : [{
                'id'               : sub_category.id,
                'name'             : sub_category.name,
                'background_image' : sub_category.image_url
            } for sub_category in main_category.subcategory_set.all()]

        } for main_category in main_categories]

        return JsonResponse({'data' : data}, status=200)


class CategoryTabView(View):
    def get(self, request, main_category_id):
        
        try:
            main_category = MainCategory.objects.get(id = main_category_id)

            data = [{
                'id'           : main_category.id,
                'name'         : main_category.name,
                'sub_category' : [{
                    'id'   : sub_category.id,
                    'name' : sub_category.name,
                    'background_image' : sub_category.image_url
                } for sub_category in main_category.subcategory_set.all()]
            }]

            return JsonResponse({'data' : data}, status=200)

        except MainCategory.DoesNotExist:
            return JsonResponse({'message' : "INVALID_MAIN_CATEGORY"}, status=400)


class JobListView(View):
    def get(self, request):
        jobs = Job.objects.all().order_by('id')
        
        offset = int(request.GET.get('offset', 0))     # 맨 처음 20개만 보이도록 pagination 처리 / 쿼리스트링 offset 필요 
        limit  = offset + 20

        data = [{
            'id'            : job.id,
            'name'          : job.name,
            'company'       : job.company.name,
            'region'        : job.company.region.name,
            'country'       : job.company.country.name,
            'reward_amount' : job.reward_amount,
            'thumbnail'     : job.company.thumbnail_url,
            'likes'         : job.likes.count()
        } for job in jobs]

        return JsonResponse({'data' : data[offset:limit]}, status=200)


class JobListCategoryView(View):
    def get(self, request, sub_category_id):
        if SubCategory.objects.filter(id = sub_category_id).exists():
            jobs = Job.objects.filter(sub_category_id = sub_category_id)

            data = [{
                'id'            : job.id,
                'name'          : job.name,
                'company'       : job.company.name,
                'region'        : job.company.region.name,
                'country'       : job.company.country.name,
                'reward_amount' : job.reward_amount,
                'thumbnail'     : job.company.thumbnail_url,
                'likes'         : job.likes.count()
            } for job in jobs]

            return JsonResponse({'data' : data}, status=200)
        
        return JsonResponse({'message' : "INVALID_SUBCATEGORY"}, status=400)


class JobDetailView(View):
    def get(self, request, job_id):
        
        try:
            job = Job.objects.get(id = job_id)
            reward_amount = job.reward_amount / 2

            data = [{
                'id'              : job.id,
                'sub_category_id' : job.sub_category.id,
                'name'            : job.name,
                'company'         : job.company.name,
                'region'          : job.company.region.name,
                'country'         : job.company.country.name,
                'referer_amount'  : reward_amount,
                'fereree_amount'  : reward_amount,
                'likes'           : job.likes.count(),
                'article'         : job.article,
                'deadline'        : job.deadline,
                'location'        : job.company.location,
                'lat'             : job.company.latitude,
                'lng'             : job.company.longitude,
                'logo_url'        : job.company.logo_url,
                'images' : [{
                    'name' : photo.name,
                    'url'  : photo.url
                } for photo in job.company.photo_set.all()]
            }]

            return JsonResponse({'data' : data}, status=200)
        except Job.DoesNotExist:
            return JsonResponse({'message' : "INVALID_JOB"}, status=400)

