from django.contrib.auth import get_user_model
# from django.utils import timezone
from django import forms

from . models import Comment, Post


User = get_user_model()


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateInput(attrs={
                'type': 'date', 'placeholder': 'DD.MM.YYYY'
            })
        }


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
