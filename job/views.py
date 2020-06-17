import json
from django.db.models import Q
from django.views     import View
from django.http      import HttpResponse, JsonResponse
from django.db        import IntegrityError

from company.models   import Company
from job.models       import (
    MainCategory, 
    SubCategory, 
    Job,
    Like,
    Bookmark
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


class LikeView(View):
    def post(self, request):
        try:
            account_id = request.GET.get('account_id', None)
            job_id     = request.GET.get('job_id', None)

            if Like.objects.filter(Q(account_id = account_id)&Q(job_id = job_id)).exists():
                like = Like.objects.get(Q(account_id = account_id)&Q(job_id = job_id))
                
                like.is_like = False if like.is_like else True                
                like.save()
            
            else:
                Like.objects.create(
                    account_id = account_id,
                    job_id     = job_id,
                    is_like = True
                )

            return HttpResponse(status = 200)
        except IntegrityError:
            return JsonResponse({'message':'Invalid Account or Job'}, status=400)
        except KeyError:
            return HttpResponse(status = 400)
    
    def get(self, request):
        try:
            account_id = request.GET.get('account_id', None)
            job_id     = request.GET.get('job_id', None)

            if Like.objects.filter(Q(account_id = account_id)&Q(job_id = job_id)).exists():
                like = Like.objects.get(Q(account_id = account_id)&Q(job_id = job_id))
                return JsonResponse({'is_like' : like.is_like}, status = 200)
            
            return JsonResponse({'message' : "Invalid Like"}, status = 400)

        except KeyError:
            return HttpResponse(status = 400)


class BookmarkView(View):
    def post(self, request):
        try:
            account_id = request.GET.get('account_id', None)
            job_id     = request.GET.get('job_id', None)

            if Bookmark.objects.filter(Q(account_id = account_id)&Q(job_id = job_id)).exists():
                bookmark = Bookmark.objects.get(Q(account_id = account_id)&Q(job_id = job_id))
                
                bookmark.is_bookmark = False if bookmark.is_bookmark else True                
                bookmark.save()
            
            else:
                Bookmark.objects.create(
                    account_id = account_id,
                    job_id     = job_id,
                    is_bookmark = True
                )

            return HttpResponse(status = 200)
        except IntegrityError:
            return JsonResponse({'message':'Invalid Account or Job'}, status=400)
        except KeyError:
            return HttpResponse(status = 400)
    
    def get(self, request):
        try:
            account_id = request.GET.get('account_id', None)
            job_id     = request.GET.get('job_id', None)

            if Bookmark.objects.filter(Q(account_id = account_id)&Q(job_id = job_id)).exists():
                bookmark = Bookmark.objects.get(Q(account_id = account_id)&Q(job_id = job_id))
                return JsonResponse({'is_bookmark' : bookmark.is_bookmark}, status = 200)
            
            return JsonResponse({'message' : "Invalid Bookmark"}, status = 400)

        except KeyError:
            return HttpResponse(status = 400)
