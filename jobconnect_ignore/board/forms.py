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
