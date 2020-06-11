from django.db import models

from account.models import Account

class Country(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'countries'

class Region(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name    = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'regions'

class Company(models.Model):
    country       = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    region        = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    name          = models.CharField(max_length=200, unique=True)
    logo_url      = models.URLField(max_length=2000, null=True)
    thumbnail_url = models.URLField(max_length=2000, null=True)
    article       = models.TextField(null=True)
    salary_new    = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    salary_all    = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    employees     = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    location      = models.CharField(max_length=250, null=True)
    latitude      = models.CharField(max_length=250, null=True)
    longitude     = models.CharField(max_length=250, null=True)
    follows       = models.ManyToManyField(Account, through='Follow')
    tags          = models.ManyToManyField('Tag', related_name='tags', through='CompanyTag')

    class Meta:
        db_table = 'companies'

class Follow(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, default='')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'follows'

class Photo(models.Model):
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    url     = models.URLField(max_length=2000, null=True)
    name    = models.CharField(max_length=2000, null=True)

    class Meta:
        db_table = 'photos'

class News(models.Model):
    company  = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    name     = models.CharField(max_length=250, null=True)
    source   = models.CharField(max_length=250, null=True)
    link_url = models.URLField(max_length=2000, null=True)

    class Meta:
        db_table = 'news'

class Tag(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        db_table = 'tags'

class CompanyTag(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default='')
    tag     = models.ForeignKey(Tag, on_delete=models.CASCADE, default='')

    class Meta:
        db_table = 'company_tag'
