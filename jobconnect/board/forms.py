from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Board, Comment


class CommentForm(forms.ModelForm):
    STATUS_CHOICES = [
        (True, '현직원'),
        (False, '전직원'),
    ]

    star = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])
    star_1 = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])
    star_2 = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])
    star_3 = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])
    star_4 = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])
    star_5 = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])
    status = forms.ChoiceField(
        choices=STATUS_CHOICES, widget=forms.Select, label='직원 상태')

    class Meta:
        model = Comment
        fields = ['job_category', 'location', 'status', 'title', 'content_pros', 'content_cons',
                  'content_hope', 'star', 'star_1', 'star_2', 'star_3', 'star_4', 'star_5']
        widgets = {
            'job_category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '직무를 입력해주세요.'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '지역을 입력해주세요.'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 10글자 이상 입력해주세요.'}),
            'content_pros': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '장점을 30글자 이상 입력해주세요.'}),
            'content_cons': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '단점을 30글자 이상 입력해주세요.'}),
            'content_hope': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회사에 바라는 점을 30글자 이상 입력해주세요.'}),
        }


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='닉네임', min_length=4, max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='이메일', required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control'}),)
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}),)
    password2 = forms.CharField(
        label='비밀번호 확인', widget=forms.PasswordInput(attrs={'class': 'form-control'}),)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('이 사용자 이름은 이미 사용중입니다.')
        return username


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='닉네임 또는 이메일', widget=forms.TextInput(
        attrs={'class': 'form-control'}),)
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}),)
