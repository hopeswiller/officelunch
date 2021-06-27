
from django import forms
from .models import Employs,Order,Product,Feedback
from django.contrib.auth.models import User

#blueprint for making a form
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Employs
        fields = ['firstname','lastname', 'department', 'email', 'password'] 


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Employs
        fields = ['email', 'password'] 


class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password'] 



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['email','meal', 'quantity','comments']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['meal', 'price']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['EmployeeFirstname','EmployeeDepartment','Product','Content']