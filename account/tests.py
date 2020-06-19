import json, bcrypt, jwt

from django.test             import TestCase, Client
from unittest.mock           import patch, MagicMock
from job.models              import MainCategory, SubCategory
from .models                 import Account, Profile, Career
from .views                  import SocialLoginView
from wepick_backend.settings import SECRET_KEY, ACCESS_TOKEN


class EmailCheckTest(TestCase):
    def setUp(self):
        Account.objects.create(email = 'qwer@qwer.com')
    
    def tearDown(self):
        Account.objects.all().delete()
    
    def test_emailcheck_exists(self):
        client = Client()
        account  = {'email' : 'qwer@qwer.com'}
        response = client.post('/account/emailcheck',json.dumps(account), content_type='applications/json')
        self.assertEqual(response.status_code, 200)
    
    def test_emailcheck_create(self):
        client = Client()
        account  = {'email' : 'aaa@aar.com'}
        response = client.post('/account/emailcheck',json.dumps(account), content_type='applications/json')
        self.assertEqual(response.status_code, 200)

    def test_emailcheck_validation_error(self):
        client = Client()
        account  = {'email' : 'aaaaarcom'}
        response = client.post('/account/emailcheck',json.dumps(account), content_type='applications/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'INVALID_FORMAT'})

class SignUpTest(TestCase):
    def setUp(self):
        Account.objects.create(
                email    = 'qwer1234@qwer.com',
                password = '123456',
                username = 'NHK'
                )
    
    def tearDown(self):
        Account.objects.all().delete()

    def test_sign_up_exists(self):
        client = Client()
        account = {
                'email'    : 'qwer1234@qwer.com',
                'password' : '123456',
                'username' : 'NHK'
                }
        response = client.post('/account/signup',json.dumps(account), content_type='applications/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message':'ALREADY_EXIST'})

    def test_sign_up(self):
        client = Client()
        account = {
                'email'    : 'asdf@asfg.com',
                'password' : '123456',
                'username' : 'NHK'
                }
        response = client.post('/account/signup',json.dumps(account), content_type='applications/json')
        self.assertEqual(response.status_code, 200)

class SignInTest(TestCase):
    def setUp(self):
        Account.objects.create(
                email    = 'qwer@qwer.com',
                password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                username = 'NHK'
                )
    
    def tearDown(self):
        Account.objects.all().delete()

    def test_sign_in(self):
        client = Client()
        account = {
                'email'    : 'qwer@qwer.com',
                'password' : '123456'
                }
        response = client.post('/account/signin',json.dumps(account), content_type='applications/json')
        self.assertEqual(response.status_code, 200)
    
    def test_sign_in_password_error(self):
        client = Client()
        account = {
                'email'    : 'qwer@qwer.com',
                'password' : '111111'
                }
        response = client.post('/account/signin',json.dumps(account), content_type='applications/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{'message':'INVALID_PASSWORD'})          

    def test_sign_in_invalid_user(self):
        client = Client()
        account   = {
            'email'    : 'qwefrgh@qwerfg.com',
            'password' : '123456',
        }
        response = client.post('/account/signin', json.dumps(account), content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'INVALID_USER'})

class SocialLoginTest(TestCase):
    def setUp(self):
        Account.objects.create(google_id = 'qwer@qwer.com')
    
    def tearDown(self):
        Account.objects.all().delete()

    @patch('account.views.requests')
    def test_google_login(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return{'google_id' : 'qwer@qwer.com'}

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        header = {'HTTP_Authorization' : 'google_token'}
        response = client.post('/account/sociallogin', content_type = 'applications/json', **header)
        self.assertEqual(response.status_code, 200)

class JobCategoryTest(TestCase):
    def setUp(self):
        MainCategory.objects.create(
            id = 1,
            name = 'it')
        SubCategory.objects.create(
            main_category_id = 1,
            id = 1,
            name = 'server')
    
    def tearDown(self):
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
    
    def test_jobcategory_get_success(self):
        client = Client()
        response = client.get('/account/jobcategory')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json(), 
            {
                'profiles' : [{
                    'id' : 1,
                    'name' : 'it',
                    'sub_category' : [{
                        'id' : 1,
                        'name' : 'server'
                        }]
                    }]
                }
            )

class CareerTest(TestCase):
    def setUp(self):
        Career.objects.create(
            id = 1,
            name = 'new')
    
    def tearDown(self):
        Career.objects.all().delete()
    
    def test_career_get_sucess(self):
        client = Client()
        response = client.get('/account/career')
        self.assertEqual(response.status_code, 200)        
        self.assertEqual(response.json(), 
            {
                'career' : [{
                    'id' : 1,
                    'name' : 'new'}]
                }
            )

class ProfileTest(TestCase):
    def setUp(self):
        Account.objects.create(
                email    = 'qwer1234@qwer.com',
                password =  123456,
                username = 'NHK'
                )
        MainCategory.objects.create(
            id = 1,
            name = 'it')
        SubCategory.objects.create(
            main_category_id = 1,
            id = 1,
            name = 'server')
        Career.objects.create(
            id = 1,
            name = 'new')
    
    def tearDown(self):
        Account.objects.all().delete()
        MainCategory.objects.all().delete()
        SubCategory.objects.all().delete()
        Career.objects.all().delete()

    def test_profile_post_success(self):
        client = Client()
        profile = {
                'sub_category_id' : 1,
                'main_category_id' : 1,
                'career_id' : 1
        }
        header = {"HTTP_AUTHORIZATION":ACCESS_TOKEN}
        access_token = self.client.post('/account/sociallogin', content_type="application/json", **header ).json()['access_token']
        header = {"HTTP_AUTHORIZATION":access_token}
        response = self.client.post('/account/profile', json.dumps(profile), content_type="application/json", **header)
        self.assertEqual(response.status_code, 200)
