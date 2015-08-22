from .integration_test_case import IntegrationTestCase


class TestTransactionAPI(IntegrationTestCase):
    def test_get_transactions(self):
        assert self.client.get_transactions()

    def test_get_transaction(self):
        order = self.build_order(immediate=True)
        self.client.create_order(order)
        transactions = self.client.get_transactions()
        transaction = transactions['transactions'][0]
        assert self.client.get_transaction(transaction['id'])

    def test_request_transaction_history(self):
        assert self.client.request_transaction_history()
