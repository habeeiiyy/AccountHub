from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AdminDashboardTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            is_staff=True,
            is_superuser=True,
        )
        self.user1 = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="pass123",
            is_active=True,
        )
        self.user2 = User.objects.create_user(
            username="bob",
            email="bob@example.com",
            password="pass123",
            is_active=True,
        )

    def test_admin_dashboard_search_filters_users(self):
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get(reverse("Accounts:admin_dashboard"), {"q": "ali"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alice")
        self.assertNotContains(response, "bob")

    def test_regular_user_is_redirected_from_admin_dashboard(self):
        self.client.login(username="alice", password="pass123")

        response = self.client.get(reverse("Accounts:admin_dashboard"))

        self.assertRedirects(
            response,
            f'{reverse("Accounts:admin_login")}?next=%2Fadmin-dashboard%2F',
        )

    def test_editing_unknown_user_returns_not_found(self):
        self.client.login(username="admin", password="adminpass123")

        response = self.client.get(reverse("Accounts:edit_user", args=[99999]))

        self.assertEqual(response.status_code, 404)

    def test_admin_can_block_and_unblock_user(self):
        self.client.login(username="admin", password="adminpass123")
        response = self.client.post(
            reverse("Accounts:toggle_user_status", args=[self.user1.id]),
            {"next": reverse("Accounts:admin_dashboard")},
        )

        self.user1.refresh_from_db()
        self.assertFalse(self.user1.is_active)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            reverse("Accounts:toggle_user_status", args=[self.user1.id]),
            {"next": reverse("Accounts:admin_dashboard")},
        )

        self.user1.refresh_from_db()
        self.assertTrue(self.user1.is_active)
        self.assertEqual(response.status_code, 302)

    def test_status_change_rejects_external_return_url(self):
        self.client.login(username="admin", password="adminpass123")

        response = self.client.post(
            reverse("Accounts:toggle_user_status", args=[self.user1.id]),
            {"next": "https://example.com/"},
        )

        self.assertRedirects(response, reverse("Accounts:admin_dashboard"))

    def test_admin_can_delete_user(self):
        self.client.login(username="admin", password="adminpass123")
        response = self.client.post(
            reverse("Accounts:delete_user", args=[self.user2.id]),
            {"next": reverse("Accounts:admin_dashboard")},
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user2.id).exists())
