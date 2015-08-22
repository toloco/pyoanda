from .integration_test_case import IntegrationTestCase


class TestAccountAPI(IntegrationTestCase):
    def test_create_account(self):
        assert self.client.create_account()

    def test_create_account_with_currency(self):
        assert self.client.create_account('GBP')
        assert self.client.create_account(currency='GBP')

    def test_get_accounts(self):
        assert self.client.get_accounts(username=self.user['username'])
