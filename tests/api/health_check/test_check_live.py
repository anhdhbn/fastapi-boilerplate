from app.i18n.errors import ErrorCode
from tests.conftest import APITestCase


class TestGetHealthCheckLive(APITestCase):
    API_ENDPOINT = "/api/healthcheck/live"

    def test_200_check_live(self):
        r = self.client.get(self.API_ENDPOINT)
        response: dict = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(response.get("code"), ErrorCode.SUCCESS_0000)
