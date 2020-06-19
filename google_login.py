import json
import bcrypt

from django.test    import TransactionTestCase, Client
from unittest.mock  import patch, MagicMock

from account.models        import Account

from account.views         import SocialLoginView

class GoogleLoginTest(TransactionTestCase):

    def setUp(self):
        bytes_pw    = bytes('123456', 'utf-8')

        Account.objects.create(
            email               = "abcd@abcd.com",
            password            = "123456",
            username            = "abcd",
            google_id           = "abcd@abcd.com"
        )

    def tearDown(self):
        Account.objects.filter(email = "abcd@abcd.com").delete()
          
    @patch('account.views.requests')
    def test_account_google_account(self, mocked_requests):
        c = Client()

        class MockedResponse:
            def json(self):
                return {
                    "user_id"    : "1234567",
                    "email" : "abcd@abcd.com"
                }
        
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        response = c.post("/account/sociallogin", **{"HTTP_Authorization":"1234567", "content_type":"application/json"})
        
        return response.json()['access_token']