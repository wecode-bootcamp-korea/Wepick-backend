from django.db import models

class Resume(models.Model):
    account      = models.ForeignKey('account.Account', on_delete = models.CASCADE)
    title        = models.CharField(max_length=500)
    introduction = models.TextField(null = True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    file_url     = models.CharField(max_length=2000)
    
    class Meta:
        db_table = 'resumes'

class WorkExperience(models.Model):
    resume       = models.ForeignKey(Resume, on_delete = models.CASCADE)
    company_name = models.CharField(max_length=200, null = True)
    department   = models.CharField(max_length=200, null = True)
    comment      = models.TextField(null = True)
    start_date   = models.DateTimeField(null = True)
    end_date     = models.DateTimeField(null = True)
    
    
    class Meta:
        db_table = 'work_experiences'

class Education(models.Model):
    resume       = models.ForeignKey(Resume, on_delete = models.CASCADE)
    school_name  = models.CharField(max_length=200)
    major        = models.CharField(max_length=200, null = True)
    comment      = models.TextField(null = True)
    start_date   = models.DateTimeField(null = True)
    end_date     = models.DateTimeField(null = True)
    
    class Meta:
        db_table = 'educations'

class OtherExperience(models.Model):
    resume       = models.ForeignKey(Resume, on_delete = models.CASCADE)
    title        = models.CharField(max_length=200)
    comment      = models.TextField(null = True)
    start_date   = models.DateTimeField(null = True)
    end_date     = models.DateTimeField(null = True)
    
    class Meta:
        db_table = 'other_experiences'

class Language(models.Model):
    resume  = models.ForeignKey(Resume, on_delete = models.CASCADE)
    name    = models.CharField(max_length=200)
    comment = models.TextField(null = True)
    
    class Meta:
        db_table = 'languages'

class Link(models.Model):
    resume  = models.ForeignKey(Resume, on_delete = models.CASCADE)
    url     = models.URLField(max_length = 2000)
    
    class Meta:
        db_table = 'links'
