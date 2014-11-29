from django import forms
from rango.models import Page, Category, UserProfile
from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet

class CategoryForm(forms.ModelForm):
    
    name = forms.CharField(max_length = 128, help_text = "Please enter the category name")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    
    class Meta:
        
        model = Category

class EditCategoryForm(forms.ModelForm):
    
    name = forms.CharField()
    views = forms.IntegerField()
    likes = forms.IntegerField()
    
    class Meta:
        
        model = Category
    
class PageForm(forms.ModelForm,):
    
    title = forms.CharField(max_length = 128, help_text = "Please enter the title page")
    url = forms.URLField(max_length = 200, help_text = "Please enter the url of the page")
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    
    def clean(self):
        
        cleaned_data = self.cleaned_data
        
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            
            url = 'http://' + url
            cleaned_data['url'] = url
            
        return cleaned_data
    
    class Meta:
        
        model = Page
        
        fields =  ('title','url','views')

class PageEditForm(forms.Form):
    
   
    
    title = forms.CharField()
    url = forms.URLField()
    
    
    def clean(self):
        
        cleaned_data = self.cleaned_data
        
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            
            url = 'http://' + url
            cleaned_data['url'] = url
            
        return cleaned_data
    
    class Meta:
        
        model = Page
        
        fields =  ('title','url')
        
class UserForm(forms.ModelForm):
    
    password = forms.CharField(widget = forms.PasswordInput())
    
    class Meta:
        model = User
        fields =  ('username', 'email', 'password')
        
        
class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')