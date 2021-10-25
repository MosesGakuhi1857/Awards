
from awardsApp.models import Project, Rating, Review
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        # fields="__all__"
        help_texts = {
            "password2":None,
            "username":None,
        }
        def __init__(self, *args, **kwargs):
            super(UserRegistrationForm, self).__init__(*args, **kwargs)

            for fieldname in ['username', 'password1', 'password2']:
                self.fields[fieldname].help_text = None

        fields = ('first_name', 'last_name', 'email','username',  'password1', 'password2')
        widgets = {
            'first_name':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"First Name", 'label': 'First Name'}),
            'last_name':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Second Name", 'label': 'Second Name'}),
            'email':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Email Address", 'label': 'Email Address'}),
            'username':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Username", 'label': 'Username'}),
            'password1':forms.PasswordInput(attrs = {'class':'form-control ', 'placeholder':"Password", 'label': 'Password'}),
            'password2':forms.PasswordInput(attrs = {'class':'form-control', 'type':'password', 'placeholder':"Confirm Password", 'label': 'Confirm Password'}),
        }

# class LoginForm(forms.Mod):


class PublishProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description', 'project_link', 'project_image','technologies',)


class RatingsForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('design', 'usability', 'content')
        widgets = {
            'design':forms.TextInput(attrs = {'class':'form-control', 'type':'number', 'min':1 ,'max':10, 'required': "True", 'placeholder':"Design", 'label': 'Design'}),
            'usability':forms.TextInput(attrs = {'class':'form-control','type':'number','min':1 ,'max':10,'required': "True", 'placeholder':"Usability", 'label': 'Usability'}),
            'content':forms.TextInput(attrs = {'class':'form-control', 'type':'number','min':1 ,'max':10,'required': "True", 'placeholder':"Content", 'label': 'Content'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('review',)


class UpdateUserProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [  'project_image', 'title','description','technologies', 'project_link']
        widgets = {
            'project_image':forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.Textarea(attrs={'class':'form-control'}), 
            'description':forms.TextInput(attrs={'class': 'form-control'}),
            'technologies':forms.TextInput(attrs={'class': 'form-control'}),
            'project_link': forms.TextInput(attrs={'class':'form-control'}),
            
        
        }