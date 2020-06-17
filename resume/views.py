import json
import jwt

from django.http    import HttpResponse, JsonResponse
from django.views   import View

from account.views  import login_required
from .models        import Resume

class ResumeListView(View):
    @login_required
    def get(self,request):
        account     = request.user.id
        resumes     = Resume.objects.filter(account_id = account)
        resume_list = [{
            'id'         : resume.id,
            'title'      : resume.title,
            'intro'      : resume.introduction,
            'updated_at' : resume.updated_at
            } for resume in resumes
        ]  
        return JsonResponse({'resume' : resume_list}, status=200)

class ResumeDetailView(View):
    @login_required
    def post(self,request,resume_id):
        try:
            data    = json.loads(request.body)
            account = request.user 
            resume  = Resume.objects.filter(id=resume_id)
            if resume.exists():
                resume.update(
                    title             = data['title'],
                    introduction      = data['introduction'],
                    work_experiences  = data['comment'],
                    educations        = data['education'],
                    other_experiences = data['other'],
                    languages         = data['language']                    
                    )
                return HttpResponse(status=200)
            Resume(            
                    title             = data['title'],
                    introduction      = data['introduction'],
                    work_experiences  = data['comment'],
                    educations        = data['education'],
                    other_experiences = data['other'],
                    languages         = data['language'],
                    account_id        = account.id
                    ).save()
            return HttpResponse(status=200)
        except KeyError:
            return HttpResponse(status=400)
    
    @login_required
    def get(self,request,resume_id):
        resumes = Resume.objects.filter(id = resume_id)
        if resumes.exists():
            resume = resumes.get()
            resume_detail = [{
                'title'            : resume.title,
                'name'             : request.user.username,
                'email'            : request.user.email,
                'introduction'     : resume.introduction,
                'work_experiences' : resume.work_experiences,
                'education'        : resume.educations,
                'other'            : resume.other_experiences,
                'language'         : resume.languages
            }
        ]
            return JsonResponse({'resume' : resume_detail}, status=200)
        resume_detail = [{
                'name'             : request.user.username,
                'email'            : request.user.email
            }
        ]
        return JsonResponse({'resume' : resume_detail}, status=200)
    
    @login_required
    def delete(self, request,resume_id):
        resumes = Resume.objects.get(id = resume_id).delete()

        return HttpResponse(status=200)
