from django import forms
#fail - was not able to create a custom form, will ty to do that in future.
class NameForm(forms.Form):
    username = forms.CharField(label='User Name')
    password = forms.CharField(label ='Password' , widget=forms.PasswordInput())