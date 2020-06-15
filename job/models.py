from django.db import models

from resume.models   import Resume
from company.models  import Company

class MainCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    image_url     = models.URLField(max_length=2000, null=True)

    class Meta:
        db_table = 'main_categories'

class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True)
    name          = models.CharField(max_length=200, unique=True)
    image_url     = models.URLField(max_length=2000, null=True)

    class Meta:
        db_table = 'sub_categories'

class Job(models.Model):
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True)
    sub_category  = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    company       = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    name          = models.CharField(max_length=200)
    article       = models.TextField(null=True)
    deadline      = models.CharField(max_length=200, null=True)
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    likes         = models.ManyToManyField('account.Account', related_name='like_jobs', through='Like')
    bookmarks     = models.ManyToManyField('account.Account', related_name='bookmark_jobs', through='Bookmark')
    applies       = models.ManyToManyField('account.Account', related_name='apply_jobs', through='Apply')
    shares        = models.ManyToManyField('account.Account', related_name='share_jobs', through='Share')


    class Meta:
        db_table = 'jobs'

class Like(models.Model):
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE, default='')
    job     = models.ForeignKey(Job, on_delete=models.CASCADE, default='')
    is_like = models.BooleanField(default=False)

    class Meta:
        db_table = 'likes'

class Bookmark(models.Model):
    account     = models.ForeignKey('account.Account', on_delete=models.CASCADE, default='')
    job         = models.ForeignKey(Job, on_delete=models.CASCADE, default='')
    is_bookmark = models.BooleanField(default=False)

    class Meta:
        db_table = 'bookmarks'

class Apply(models.Model):
    account  = models.ForeignKey('account.Account', on_delete=models.CASCADE, default='')
    job      = models.ForeignKey(Job, on_delete=models.CASCADE,default='')
    resume   = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True)
    is_apply = models.BooleanField(default=False)

    class Meta:
        db_table = 'applies'

class Share(models.Model):
    account   = models.ForeignKey('account.Account', on_delete=models.CASCADE, default='')
    job       = models.ForeignKey(Job, on_delete=models.CASCADE, default='')
    share_url = models.CharField(max_length=200, null=True)
    is_apply  = models.BooleanField(default=False)

    class Meta:
        db_table = 'shares'