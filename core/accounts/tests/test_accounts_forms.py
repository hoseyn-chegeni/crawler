from django.test import TestCase
from ..forms import CustomUserUpdateForm, UserCreationForm

class TestUserForms(TestCase):
    def test_update_user_form_with_valid_data(self):
        form = CustomUserUpdateForm(data ={ 
            "email":'test@test.com',
            "first_name":"test",
            "last_name":"test",
        })
        self.assertTrue(form.is_valid())

    def test_create_user_form_with_valid_data(self):
        form = CustomUserUpdateForm(data ={ 
            "email":'test@test.com',
            "first_name":"test",
            "last_name":"test",
            "password1":"Test@123",
        })
        self.assertTrue(form.is_valid())

    def test_user_form_with_no_data(self):
        form = CustomUserUpdateForm(data ={})
        self.assertFalse(form.is_valid())

    def test_user_form_with_invalid_data(self):
        form = CustomUserUpdateForm(data ={    
            "email":'test.com',
            "first_name":"test",
            "last_name":"test",
            "password1":"Test@123",})
        self.assertFalse(form.is_valid())