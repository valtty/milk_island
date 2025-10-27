from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Review, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий email.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }
        help_texts = {
            'username': 'Обязательно. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
            'password2': 'Введите тот же пароль, что и выше, для подтверждения.',
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment_text', 'image']
        widgets = {
            'comment_text': forms.Textarea(attrs={'placeholder': 'Оставить комментарий', 'class': 'comment-textarea'}),
            'image': forms.ClearableFileInput(attrs={'class': 'photo-input'}),
        }
        labels = {
            'rating': 'Оценка',
            'comment_text': 'Комментарий',
            'image': 'Изображение',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment_text'].required = False
        self.fields['image'].required = False
        self.fields['rating'].required = True

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {
            'username': 'Имя пользователя',
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['city', 'avatar']
        labels = {
            'city': 'Город',
            'avatar': 'Аватар',
        }
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'profile-avatar-input'}),
        }