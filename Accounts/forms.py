from django import forms

class Loginform(forms.Form):
    username=forms.CharField(
        label="username",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password=forms.CharField(
        label="password:",
        widget=forms.PasswordInput(attrs={"class":"form-control"})
    )