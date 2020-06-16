import json
from django.test    import TestCase, Client

from company.models import (
    Country, 
    Region, 
    Company, 
    Photo, 
    News
)

from job.models     import (
    MainCategory, 
    SubCategory, 
    Job
)

class CategoryView(TestCase):
    def setUp(self):
        MainCategory.objects.create(
            id = 1,
            name = 'dev'
        )

        SubCategory.objects.create(
            main_category_id = 1,
            id = 1,
            name = 'server'
        )
    
    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
    
    def test_category_get_success(self):
        client = Client() 
        response = client.get('/job/category')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json(), 
        {'data' : [{
            'id' : 1,
            'name' : 'dev',
            'background_image' : None,
            'sub_category' : [{
                'id' : 1,
                'name' : 'server',
                'background_image' : None}]}]
        })
    
    def test_category_get_not_found(self):
        client = Client() 
        response = client.get('/job/categories')
        self.assertEqual(response.status_code, 404) 


class CategoryTabView(TestCase):
    def setUp(self):
        MainCategory.objects.create(
            id = 1,
            name = 'dev'
        )

        SubCategory.objects.create(
            main_category_id = 1,
            id = 1,
            name = 'server'
        )

        SubCategory.objects.create(
            main_category_id = 1,
            id = 2,
            name = 'android'
        )
    
    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
    
    def test_categorytab_get_success(self):
        client = Client() 
        response = client.get('/job/category/1')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json(), 
        {'data' : [{
            'id' : 1,
            'name' : 'dev',
            #'background_image' : None,
            'sub_category' : [{
                'id' : 1,
                'name' : 'server',
                'background_image' : None
                },
                {
                'id' : 2,
                'name' : 'android',
                'background_image' : None
                }]}]
        })

    def test_categorytab_get_fail(self):
        client = Client()
        response = client.get('/job/category/100')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {'message' : "INVALID_MAIN_CATEGORY"}
        )

    def test_categorytab_get_not_found(self):
        client = Client() 
        response = client.get('/job?category_id=100')
        self.assertEqual(response.status_code, 404) 


class JobListView(TestCase):
    def setUp(self):
        Country.objects.create(
            id = 1,
            name = 'korea'
        )

        Region.objects.create(
            country_id = 1,
            id = 1,
            name = 'seoul'
        )

        Company.objects.create(
            id = 1,
            country_id = 1,
            region_id = 1,
            name = 'wecode'
        )

        MainCategory.objects.create(
            id = 1,
            name = 'dev'
        )

        SubCategory.objects.create(
            main_category_id = 1,
            id = 1,
            name = 'server'
        )

        Job.objects.create(
            main_category_id = 1,
            sub_category_id = 1,
            company_id = 1,
            id = 1,
            name = 'android 개발'
        )
    
    def tearDown(self):
        Job.objects.all().delete()
    
    def test_joblist_get_success(self):
        client = Client() 
        response = client.get('/job/list')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json(), 
        {'data' : [{
            'id' : 1,
            'name' : 'android 개발',
            'company' : 'wecode',
            'country' : 'korea', 
            'region' : 'seoul',
            'reward_amount' : None,
            'thumbnail' : None,
            'likes' : 0}]
        })
    
    def test_joblist_get_not_found(self):
        client = Client() 
        response = client.get('/job/lists')
        self.assertEqual(response.status_code, 404) 


class JobListCategoryView(TestCase):
    def setUp(self):
        Country.objects.create(
            id = 1,
            name = 'korea'
        )

        Region.objects.create(
            country_id = 1,
            id = 1,
            name = 'seoul'
        )

        Company.objects.create(
            country_id = 1,
            region_id = 1,
            id = 1,
            name = 'wecode'
        )

        MainCategory.objects.create(
            id = 1,
            name = 'dev'
        )

        SubCategory.objects.create(
            main_category_id = 1,
            id = 1,
            name = 'server'
        )

        Job.objects.create(
            main_category_id = 1,
            sub_category_id = 1,
            company_id = 1,
            id = 1,
            name = 'server 개발'
        )

    def tearDown(self):
        Country.objects.all().delete()
        Region.objects.all().delete()
        Company.objects.all().delete()
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Job.objects.all().delete()
    
    def test_joblistcategory_get_success(self):
        client = Client() 
        response = client.get('/job/list/1')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json(), 
        {'data' : [{
            'id' : 1,
            'name' : 'server 개발',
            'company' : 'wecode',
            'country' : 'korea', 
            'region' : 'seoul',
            'reward_amount' : None,
            'thumbnail' : None,
            'likes' : 0}]
        })

    def test_joblistcategory_get_fail(self):
        client = Client() 
        response = client.get('/job/list/10')

        self.assertEqual(response.status_code, 400) 
        self.assertEqual(response.json(), {'message' : "INVALID_SUBCATEGORY"})

    def test_joblistcategory_get_not_found(self):
        client = Client() 
        response = client.get('/job/lists/10')
        self.assertEqual(response.status_code, 404)


class JobDetailView(TestCase):
    def setUp(self):
        Country.objects.create(
            id = 1,
            name = 'korea'
        )

        Region.objects.create(
            country_id = 1,
            id = 1,
            name = 'seoul'
        )

        Company.objects.create(
            country_id = 1,
            region_id = 1,
            id = 1,
            name = 'wecode'
        )

        Photo.objects.create(
            company_id = 1,
            id = 1
        )

        MainCategory.objects.create(
            id = 1,
            name = 'dev'
        )

        SubCategory.objects.create(
            main_category_id = 1,
            id = 1,
            name = 'server'
        )

        Job.objects.create(
            main_category_id = 1,
            sub_category_id = 1,
            company_id = 1,
            id = 1,
            name = 'server 개발',
            reward_amount = 100
        )

    def tearDown(self):
        Country.objects.all().delete()
        Region.objects.all().delete()
        Company.objects.all().delete()
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Job.objects.all().delete()
    
    def test_jobdetail_get_success(self):
        client = Client() 
        response = client.get('/job/1')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json(), 
        {'data' : [{
            'id' : 1,
            'sub_category_id' : 1,
            'name' : 'server 개발',
            'company' : 'wecode',
            'region' : 'seoul',
            'country' : 'korea',
            'referer_amount' : '50.00',
            'fereree_amount' : '50.00',
            'likes' : 0,
            'article' : None,
            'deadline' : None,
            'location' : None,
            'lat' : None,
            'lng' : None,
            'logo_url' : None,
            'images' : [{
                    'name' : None,
                    'url' : None}]
            }]
        })

    def test_jobdetail_get_fail(self):
        client = Client() 
        response = client.get('/job/2')
        self.assertEqual(response.status_code, 400) 
        self.assertEqual(response.json(), {'message' : "INVALID_JOB"})

    def test_jobdetail_get_not_found(self):
        client = Client() 
        response = client.get('/job')
        self.assertEqual(response.status_code, 404)

