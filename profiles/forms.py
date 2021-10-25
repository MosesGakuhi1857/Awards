from django import forms
from django.forms import widgets
from .models import Profile



class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'profile_pic', 'bio','gender','location', 'mobile', 'website', 'github']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class':'form-control'}),
            'bio':forms.Textarea(attrs={'class': 'form-control'}),
            'gender':forms.Select(attrs={'class': 'form-control'}),
            'location':forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class':'form-control'}),
            'website': forms.TextInput(attrs={'class':'form-control'}),
            'github':forms.TextInput(attrs={'class': 'form-control'}),

        }