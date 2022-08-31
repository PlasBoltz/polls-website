from cProfile import Profile
from .models import Post
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email' , 'first_name', 'last_name']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title, content, meta_tags']

class CommentForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
