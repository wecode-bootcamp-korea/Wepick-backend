import json
from django.test    import (
    TestCase, 
    Client, 
    TransactionTestCase
)

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
    Job,
    Like,
    Bookmark,
    Apply
)

from account.models import Account
from resume.models  import Resume

import google_login
google_login = google_login.GoogleLoginTest


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
            'company_id' : 1,
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

class LikeTest(TransactionTestCase):
    def setUp(self):
        Job.objects.create(
            id = 1,
            name = 'frontend'
        )

        Job.objects.create(
            id = 2,
            name = 'backend'
        )

        google_login.setUp(self)
        account = Account.objects.get(google_id="abcd@abcd.com")

        Like.objects.create(
            account_id = account.id,
            job_id = 1,
            is_like = True
        )
    
    def tearDown(self): 
        Account.objects.all().delete()
        Job.objects.all().delete()
        Like.objects.all().delete()
    
    def test_like_get_success(self):
        client = Client()
        access_token = google_login.test_account_google_account(self)
        header = {"HTTP_AUTHORIZATION":access_token}
        response = client.get('/job/like?job_id=1', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {'is_like' : True}
        )
    
    def test_like_get_fail(self):
        client = Client()
        access_token = google_login.test_account_google_account(self)
        header = {"HTTP_AUTHORIZATION":access_token}
        response = client.get('/job/like?job_id=100', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {'message' : "Invalid Like"}
        )

    def test_like_post_success(self):
        client = Client()
        access_token = google_login.test_account_google_account(self)
        header = {"HTTP_AUTHORIZATION":access_token}
        response = client.post('/job/like?job_id=2', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)
    
    def test_like_post_fail(self):
        client = Client()
        access_token = google_login.test_account_google_account(self)
        header = {"HTTP_AUTHORIZATION":access_token}
        response = client.post('/job/like?job_id=200', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {'message':'Invalid Account or Job'}
        )


class BookmarkTest(TransactionTestCase):
    def setUp(self):
        Job.objects.create(
            id = 1,
            name = 'frontend'
        )

        Job.objects.create(
            id = 2,
            name = 'backend'
        )

        google_login.setUp(self)
        account = Account.objects.get(google_id="abcd@abcd.com")

        Bookmark.objects.create(
            account_id = account.id,
            job_id = 1,
            is_bookmark = True
        )
    
    def tearDown(self): 
        Account.objects.all().delete()
        Job.objects.all().delete()
        Bookmark.objects.all().delete()
    
    def test_bookmark_get_success(self):
        client = Client()
        access_token = google_login.test_account_google_account(self)
        header = {"HTTP_AUTHORIZATION":access_token}
        response = client.get('/job/bookmark?job_id=1', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {'is_bookmark' : True}
        )
    
    def test_bookmark_get_fail(self):
        client = Client()
        access_token = google_login.test_account_google_account(self)
        header = {"HTTP_AUTHORIZATION":access_token}
        response = client.get('/job/bookmark?job_id=100', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {'message' : "Invalid Bookmark"}
        )

    def test_bookmark_post_success(self):
        client = Client()
        access_token = google_login.test_account_google_account(self)
        header = {"HTTP_AUTHORIZATION":access_token}
        response = client.post('/job/bookmark?job_id=2', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)
    
    def test_bookmark_post_fail(self):
        client = Client()
        access_token = google_login.test_account_google_account(self)
        header = {"HTTP_AUTHORIZATION":access_token}
        response = client.post('/job/bookmark?job_id=200', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {'message':'Invalid Account or Job'}
        )

class ApplyTest(TransactionTestCase):
    def setUp(self):
        Job.objects.create(
            id = 1,
            name = 'frontend'
        )

        Job.objects.create(
            id = 2,
            name = 'backend'
        )

        google_login.setUp(self)
        account = Account.objects.get(google_id="abcd@abcd.com")

        Resume.objects.create(
            id = 1,
            account_id = account.id,
            title = 'greate resume'  
        )

        Apply.objects.create(
            account_id = account.id,
            job_id = 1,
            resume_id = 1,
            is_apply = True
        )
    
    def tearDown(self): 
        Account.objects.all().delete()
        Job.objects.all().delete()
        Bookmark.objects.all().delete()
    
    def test_apply_get_success(self):
        client = Client()
        access_token = google_login.test_account_google_account(self)
        header = {"HTTP_AUTHORIZATION":access_token}
        response = client.get('/job/apply?job_id=1', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)

    def test_apply_post_success(self):
        client = Client()
        access_token = google_login.test_account_google_account(self)
        header = {"HTTP_AUTHORIZATION":access_token}
        response = client.post('/job/apply?job_id=2&resume_id=1', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)