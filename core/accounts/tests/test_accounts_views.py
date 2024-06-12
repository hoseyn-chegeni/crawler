# from django.test import TestCase, Client
# from ..views import User
# from django.urls import reverse
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import Permission


# class TestLoginView(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             email="test@example.com", password="password123"
#         )

#     def test_login(self):
#         url = reverse("accounts:login")
#         login_data = {
#             "username": "test@example.com",
#             "password": "password123",
#         }
#         response = self.client.post(url, login_data, follow=True)

#         self.assertTrue(response.context["user"].is_authenticated)
#         self.assertEqual(response.status_code, 200)


# class TestUserListView(TestCase):
#     def setUp(self):
#         self.user_with_perms = User.objects.create_user(
#             email="testuser@example.com", password="12345", is_superuser=True
#         )
#         self.user = User.objects.create_user(
#             email="testuser2@example.com", password="12345"
#         )
#         self.user_with_permission = User.objects.create_user(
#             email="permitteduser@example.com", password="12345"
#         )
#         content_type = ContentType.objects.get_for_model(User)
#         permission = Permission.objects.get(
#             codename="view_user", content_type=content_type
#         )
#         self.user_with_permission.user_permissions.add(permission)
#         for i in range(15):
#             User.objects.create_user(email=f"user{i}@example.com", password="12345")

#     def test_pagination(self):
#         self.client.login(email="testuser@example.com", password="12345")
#         session = self.client.session
#         session["items_per_page"] = 10
#         session.save()
#         response = self.client.get(reverse("accounts:list"))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context["users"]), 10)

#     def test_queryset_ordering(self):
#         self.client.login(email="testuser@example.com", password="12345")
#         response = self.client.get(reverse("accounts:list"))
#         self.assertEqual(response.status_code, 200)
#         users = response.context["users"]
#         self.assertTrue(users.ordered)
#         self.assertEqual(users.query.order_by, ("-created_at",))

#     def test_filtering(self):
#         self.client.login(email="testuser@example.com", password="12345")
#         response = self.client.get(
#             reverse("accounts:list"), {"email": "user1@example.com"}
#         )
#         self.assertEqual(response.status_code, 200)
#         users = response.context["users"]
#         self.assertEqual(len(users), 1)
#         self.assertEqual(users[0].email, "user1@example.com")

#     def test_permission_denied(self):
#         self.client.login(email="testuser2@example.com", password="12345")
#         response = self.client.get(reverse("accounts:list"))
#         self.assertEqual(response.status_code, 403)


# class TestUserDeatilView(TestCase):
#     def setUp(self):
#         self.user_with_perms = User.objects.create_user(
#             email="testuser@example.com", password="12345", is_superuser=True
#         )

#     def test_user_detail_view(self):
#         self.client.login(email="testuser@example.com", password="12345")
#         response = self.client.get(
#             reverse("accounts:detail", kwargs={"pk": self.user_with_perms.pk})
#         )
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.user_with_perms.email)

#     def test_login_required(self):
#         response = self.client.get(
#             reverse("accounts:detail", kwargs={"pk": self.user_with_perms.pk})
#         )
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(response.url.startswith("/accounts/login/"))


# class TestAccountsPermissions(TestCase):
#     def setUp(self):
#         self.user_without_permission = User.objects.create_user(
#             email="testuser@example.com", password="12345"
#         )
#         self.user_with_permission = User.objects.create_user(
#             email="permitteduser@example.com", password="12345"
#         )
#         content_type = ContentType.objects.get_for_model(User)
#         permission = Permission.objects.get(
#             codename="view_user", content_type=content_type
#         )
#         self.user_with_permission.user_permissions.add(permission)

#     def test_permission_required_denied(self):
#         self.client.login(email="testuser@example.com", password="12345")
#         response = self.client.get(
#             reverse("accounts:detail", kwargs={"pk": self.user_without_permission.pk})
#         )
#         self.assertEqual(response.status_code, 403)

#     def test_permission_required_granted(self):
#         self.client.login(email="permitteduser@example.com", password="12345")
#         response = self.client.get(
#             reverse("accounts:detail", kwargs={"pk": self.user_with_permission.pk})
#         )
#         self.assertEqual(response.status_code, 200)


# class UserCreateViewTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             email="testuser@example.com", password="12345"
#         )
#         self.user_with_permission = User.objects.create_user(
#             email="admin@admin.com", password="admin12345"
#         )
#         content_type = ContentType.objects.get_for_model(User)
#         permission = Permission.objects.get(
#             codename="add_user", content_type=content_type
#         )
#         self.user_with_permission.user_permissions.add(permission)

#     def test_form_display(self):
#         self.client.login(email="admin@admin.com", password="admin12345")
#         response = self.client.get(reverse("accounts:create"))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "form")
#         self.assertContains(response, "email")
#         self.assertContains(response, "first_name")
#         self.assertContains(response, "last_name")
#         self.assertContains(response, "password1")

#     def test_form_submission(self):
#         self.client.login(email="admin@admin.com", password="admin12345")
#         data = {
#             "email": "newuser@example.com",
#             "first_name": "New",
#             "last_name": "User",
#             "password1": "D@tateb$^@",
#             "password2": "D@tateb$^@",
#         }
#         response = self.client.post(reverse("accounts:create"), data)

#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
#         new_user = User.objects.get(email="newuser@example.com")
#         self.assertEqual(new_user.first_name, "New")
#         self.assertEqual(new_user.last_name, "User")

#     def test_permission_required_denied(self):
#         self.client.login(email="testuser@example.com", password="12345")
#         response = self.client.get(reverse("accounts:create"))
#         self.assertEqual(response.status_code, 403)

#     def test_permission_required_granted(self):
#         self.client.login(email="admin@admin.com", password="admin12345")
#         response = self.client.get(reverse("accounts:create"))
#         self.assertEqual(response.status_code, 200)
