from django.test import Client, TestCase

from YSE_App.models import Host, ObservationGroup, Transient, TransientStatus


class LoginSmokeTests(TestCase):
    def test_login_page_returns_200(self):
        response = Client().get("/login/")
        self.assertEqual(response.status_code, 200)


class TransientModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.status, _ = TransientStatus.objects.get_or_create(name="New")
        cls.obs_group, _ = ObservationGroup.objects.get_or_create(name="test-group")

    def test_separation_without_host_returns_none(self):
        transient = Transient(ra=10.0, dec=20.0, host_id=None)
        self.assertIsNone(transient.Separation())

    def test_separation_with_host_returns_formatted_arcsec(self):
        host = Host.objects.create(ra=10.0, dec=20.0, name="test-host")
        transient = Transient.objects.create(
            name="test-transient",
            ra=10.0,
            dec=20.0,
            host=host,
            status=self.status,
            obs_group=self.obs_group,
        )
        self.assertEqual(transient.Separation(), "0.00")
