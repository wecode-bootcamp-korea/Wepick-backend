import json, bcrypt, jwt, requests

from django.db.models         import Q
from django.views             import View
from django.http              import HttpResponse, JsonResponse
from django.core.validators   import validate_email
from django.core.exceptions   import ValidationError

from job.models               import (
    MainCategory, 
    SubCategory,
    Like,
    Bookmark,
    Apply
)
from .models                  import (
    Account, 
    Career, 
    Profile
)
from wepick_backend.settings  import SECRET_KEY, ALGORITHM

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = jwt.decode(request.headers['Authorization'], SECRET_KEY, ALGORITHM)
            user = Account.objects.get(id = access_token['account_id'])
            request.user = user
            return func(self, request, *args, **kwargs)

        except Account.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)

    return wrapper

class EmailCheckView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            validate_email(data['email'])
            if Account.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'To Login'}, status=200)
            return JsonResponse({'message' : 'To Signup'}, status = 200)
        except ValidationError:
            return JsonResponse({"message": "INVALID_FORMAT"}, status = 400)

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        if len(data['password']) < 6:
            return JsonResponse({'message': 'PASSWORD_TOO_SHORT'}, status=400)
        if Account.objects.filter(email = data['email']).exists():
            return JsonResponse({'message':'ALREADY_EXIST'}, status=400)
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        Account.objects.create(
                email    = data['email'],
                password = hashed_password,
                username = data['username'],
                )
        return HttpResponse(status=200)
           
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        if Account.objects.filter(email = data['email']).exists():
            if bcrypt.checkpw(data['password'].encode('utf-8'), Account.objects.get(email = data['email']).password.encode('utf-8')):
                account = Account.objects.get(email=data['email'])
                token = jwt.encode({ 'account_id' : account.id }, SECRET_KEY, ALGORITHM).decode('utf-8')
                return JsonResponse({'access_token':token},status=200)
            return JsonResponse({'message':'INVALID_PASSWORD'},status=401)
        return JsonResponse({'message':'INVALID_USER'},status=401)

class SocialLoginView(View):
    def post(self, request):
        id_token     = request.headers.get('Authorization')
        user_request = requests.get(f'https://oauth2.googleapis.com/tokeninfo?access_token={id_token}')
        user_info    = user_request.json()
        user_email   = user_info.get('email')
        if Account.objects.filter(google_id = user_email).exists():
            user  = Account.objects.get(google_id = user_email)
            token = jwt.encode({ 'account_id' : user.id }, SECRET_KEY, ALGORITHM).decode('utf-8')
           
            return JsonResponse({'access_token' : token}, status = 200)
        
        user = Account.objects.create(google_id = user_email)
        token = jwt.encode({ 'account_id' : user.id }, SECRET_KEY, ALGORITHM).decode('utf-8')
        return JsonResponse({'access_token': token}, status = 200)

class JobCategoryView(View):    
    def get(self, request):
        maincategories = MainCategory.objects.all()
        profile = [{
            'id'   : maincategory.id,
            'name' : maincategory.name,
            'sub_category' : [{
                    'id'   : sub.id,
                    'name' : sub.name
                    } for sub in maincategory.subcategory_set.all()]
                }for maincategory in maincategories
            ]
        return JsonResponse({'profiles' : profile}, status=200)

class CareerView(View):
    def get(self, request):
        careers     = Career.objects.all()
        career_data = [{
            'id'   : career.id,
            'name' : career.name
            } for career in careers
        ]
        return JsonResponse({'career' : career_data}, status=200)

class ProfileView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)
        account_id = request.user.id
        account = Account.objects.get(id = account_id)
        profile = Profile(    
            sub_category_id  = data['sub_category_id'],
            main_category_id = data['main_category_id'],
            career_id        = data['career_id']
        ).save()

        account.profile = profile
        account.save()
        return HttpResponse(status=200)
    
    @login_required
    def get(self, request):
        account_id = request.user.id
        account    = Account.objects.get(id = account_id)
        
        if account.profile:
            data = {
                'main_category_name' : account.profile.main_category.name,
                'sub_category_name' : account.profile.sub_category.name,
                'career' : account.profile.career.name,
            }
            return JsonResponse({'data' : data}, status=200)
        else:
            return JsonResponse({'message' : 'No profile'}, status=400)


class MyPageMainView(View):
    @login_required
    def get(self, request):
        try:
            account_id = request.user.id
            account    = Account.objects.get(id = account_id)

            data = {
                'id'        : account.id,
                'name'      : account.username,
                'email'     : account.email,
                'applies'   : account.apply_set.count(),
                'likes'     : account.like_set.filter(is_like = True).count(),
                'bookmarks' : account.bookmark_set.filter(is_bookmark = True).count()
            }
            return JsonResponse({'data' : data}, status = 200)
        except KeyError:
            return HttpResponse(status = 400)

class MyPageLikeView(View):
    @login_required
    def get(self, request):
        try:
            account_id = request.user.id
            
            if Like.objects.filter(Q(account_id = account_id) & Q(is_like = True)).exists():
                likes = Like.objects.filter(Q(account_id = account_id) & Q(is_like = True))

                data = [{
                    'id'            : like.job.id,
                    'name'          : like.job.name,
                    'company'       : like.job.company.name,
                    'region'        : like.job.company.region.name,
                    'country'       : like.job.company.country.name,
                    'reward_amount' : like.job.reward_amount,
                    'thumbnail'     : like.job.company.thumbnail_url,
                    'likes'         : like.job.like_set.filter(is_like = True).count()
                } for like in likes]

                return JsonResponse({'data' : data}, status = 200)
            return JsonResponse({'message' : 'No likes'}, status = 400)
        except KeyError:
            return HttpResponse(status = 400)

class MyPageBookmarkView(View):
    @login_required
    def get(self, request):
        try:
            account_id = request.user.id
            
            if Bookmark.objects.filter(Q(account_id = account_id) & Q(is_bookmark = True)).exists():
                bookmarks = Bookmark.objects.filter(Q(account_id = account_id) & Q(is_bookmark = True))

                data = [{
                    'id'            : bookmark.job.id,
                    'name'          : bookmark.job.name,
                    'company'       : bookmark.job.company.name,
                    'region'        : bookmark.job.company.region.name,
                    'country'       : bookmark.job.company.country.name,
                    'reward_amount' : bookmark.job.reward_amount,
                    'thumbnail'     : bookmark.job.company.thumbnail_url,
                    'bookmarks'     : bookmark.job.bookmark_set.filter(is_bookmark = True).count()
                } for bookmark in bookmarks]

                return JsonResponse({'data' : data}, status = 200)
            return JsonResponse({'message' : 'No bookmarks'}, status = 400)
        except KeyError:
            return HttpResponse(status = 400)

class MyPageApplyView(View):
    @login_required
    def get(self, request):
        try:
            account_id = request.user.id
            
            if Apply.objects.filter(account_id = account_id).exists():
                applies = Apply.objects.filter(account_id = account_id)

                data = { 
                    'total_applies' : applies.count(),
                    'applies'       :
                        [{
                        'id'            : apply.job.id,
                        'company'       : apply.job.company.name,
                        'logo_url'      : apply.job.company.logo_url,
                        'name'          : apply.job.name,
                        'created_at'    : apply.created_at,
                        'status'        : '서류 검토 중',
                        'reward_amount' : apply.job.reward_amount/2
                    } for apply in applies]
                }

                return JsonResponse({'data' : data}, status = 200)
            return JsonResponse({'message' : 'No applies'}, status = 400)
        except KeyError:
            return HttpResponse(status = 400)

