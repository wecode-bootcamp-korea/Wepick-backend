from django.db import models


class Account(models.Model):
    email       = models.EmailField(max_length = 200, unique = True, null=True)
    google_id   = models.EmailField(max_length = 200, unique = True, null=True)
    password    = models.CharField(max_length = 255, null = True)
    username    = models.CharField(max_length = 200, null = True)
    phone       = models.CharField(max_length = 200, null = True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    profile     = models.OneToOneField('Profile', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'accounts'

class Profile(models.Model):
    main_category = models.ForeignKey('job.MainCategory', on_delete=models.SET_NULL, null=True)
    sub_category  = models.ForeignKey('job.SubCategory', on_delete=models.SET_NULL, null=True)
    career        = models.OneToOneField('Career', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'profiles'

class Career(models.Model):
    name = models.CharField(max_length = 200, default='')
    
    class Meta:
        db_table = 'careers'

class Skill(models.Model):
    name    = models.CharField(max_length = 200, null = True)
    profile = models.ForeignKey(Profile, on_delete = models.SET_NULL, null = True)
    
    class Meta:
        db_table = 'skills'