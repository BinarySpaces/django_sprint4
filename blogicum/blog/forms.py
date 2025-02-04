from django.contrib.auth import get_user_model
from django.utils import timezone
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

    def clean(self):
        cleaned_data = super().clean()
        pub_date = cleaned_data.get('pub_date')

        if pub_date and pub_date > timezone.now():
            cleaned_data['is_published'] = False
        else:
            cleaned_data['is_published'] = cleaned_data.get('is_published')
        return cleaned_data


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
