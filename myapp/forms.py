from .models import CustomUser,Citizen
from django import forms

class CitizenRegistrationForm(forms.ModelForm):
    email=forms.CharField(widget=forms.TextInput())
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=Citizen
        fields=["email","password","full_name"]

    def clean_email(self):
        email=self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.Proceed to login")
        return email
    
class CitizenLoginForm(forms.ModelForm):
    email=forms.CharField(widget=forms.TextInput())
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=Citizen
        fields=["email","password"]


class ForgetPasswordForm(forms.Form):
    email=forms.CharField(widget=forms.EmailInput)

    def clean_email(self):
        email=self.cleaned_data.get("email")
        
        if CustomUser.objects.filter(email=email).exists():
            pass
        else:
            raise forms.ValidationError("Email entered for non registered customer")
        return email
    

# from django.contrib.auth.forms import PasswordChangeForm
# class ChangePasswordForm(PasswordChangeForm):
#     new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = CustomUser
#         fields = ('old_password', 'new_password1', 'new_password2')

class ResetPasswordForm(forms.Form):
    new_password=forms.CharField(widget=forms.PasswordInput)
    confirm_passwordconfirm=forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        np=self.cleaned_data.get("new_password")
        cp=self.cleaned_data.get("confirm_password")
        if np !=cp :
            raise forms.ValidationError("Pw and conf pw doesnt match")
        return cp
    

    
