from django import forms
from .models import News, Reviews, UserProfile
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django.forms import ModelForm
from django.forms import Textarea
from django.core.files.images import get_image_dimensions


# class NewContactForm(forms.Form):
#     subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     content = forms.CharField(label='Текст', widget=forms.TextInput(attrs={'class': 'form-control', "rows": 4}))
#     captcha = CaptchaField()

class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.TextInput(attrs={'class': 'form-control', "rows": 4}))
    captcha = CaptchaField()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username =forms.CharField(label='Имя пользователя', help_text = 'Имя пользователя не более 150 символов', widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', help_text = "Например : yanafiery@mail.ru", widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus')

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content','is_published','category']
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control'}),
            'content': forms.Textarea(attrs={'class' : 'form-control', 'rows' : 5}),
            'category': forms.Select(attrs={'class' : 'form-control'}),
        }

def clean_title(self):
    title = self.cleaned_data['title']
    if re.match (r'\d', title):
        raise ValidationError('НАЗВАНИЕ НЕ С ЦИФРЫ!')
    return title

# class ReviewForm(forms.ModelForm):
#     """Форма отзыва"""
#     class Meta:
#         model = Reviews
#         fields =['name', 'email', 'text']
#         widgets = {
#             'text' : Textarea(
#                 attrs = {
#                     'placeholder' : 'Напиште свое сообщение'
#                 }
#             )
            
#         }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('text',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        #self.fields['text'].widget = Textarea(attrs={'rows' : 5})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
         
        def clean_avatar(self):
            avatar = self.cleaned_data['avatar']

            try:
                w, h =get_image_dimensions(avatar)

                max_width = max_height = 100
                if w > max_width or h > max_height:
                    raise forms.ValidationError(
                        u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
                main, sub = avatar.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                    raise forms.ValidationError(u'Please use a JPEG, '
                        'GIF or PNG image.')

            #validate file size
                if len(avatar) > (20 * 1024):
                    raise forms.ValidationError(
                        u'Avatar file size may not exceed 20k.')

            except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new avatar
                """
            pass

            return avatar