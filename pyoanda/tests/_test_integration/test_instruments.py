from .integration_test_case import IntegrationTestCase


class TestInstrumentsAPI(IntegrationTestCase):
    def test_get_instruments_pass(self):
        assert self.client.get_instruments()

    def test_get_prices_unstreamed(self):
        assert self.client.get_prices(instruments="EUR_GBP", stream=False)

    def test_get_prices_streamed(self):
        resp = self.client.get_prices(instruments="EUR_GBP", stream=True)
        prices = resp.iter_lines()
        assert next(prices)

    def test_get_instrument_history(self):
        assert self.client.get_instrument_history('EUR_GBP')
