import json, bcrypt, jwt, requests


from django.views             import View
from django.http              import HttpResponse, JsonResponse
from django.core.validators   import validate_email
from django.core.exceptions   import ValidationError

from job.models               import (
    MainCategory, 
    SubCategory
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
                return HttpResponse(status=401)
            return HttpResponse(status = 200)
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
        account = Account.objects.get(id = request.user.id)
        profile = Profile(    
            sub_category_id  = data['sub_category_id'],
            main_category_id = data['main_category_id'],
            career_id        = data['career_id']
                ).save()

        account.profile = profile
        account.save()
        return HttpResponse(status=200)

