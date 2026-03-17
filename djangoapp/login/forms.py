# from django import forms
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User, Group
# from django.contrib.auth.forms import AuthenticationForm


# class CustomUserForm(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'email', 'password')

from django                                     import forms
from django.contrib.auth.forms                  import UserCreationForm
from django.contrib.auth.models                 import Group, User

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', )      
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class':'form-control form-control-sm'})      
            
            

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "group")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            group = self.cleaned_data["group"]
            user.groups.add(group)
        return user
    

class UserGroupForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Usuário", widget=forms.Select(attrs={'class': 'form-control'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label="Grupo", widget=forms.Select(attrs={'class': 'form-control'}))
    


