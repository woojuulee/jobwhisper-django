from django.db import models
from django.utils import timezone

from django.core import validators


class Board(models.Model):
    name = models.CharField(max_length=255, validators=[
        validators.MinLengthValidator(2, "최소 세 글자 이상은 입력해주셔야 합니다.")
    ])
    category = models.CharField(max_length=255,)
    description = models.TextField(validators=[
        validators.MinLengthValidator(10, "최소 10글자 이상은 입력해주셔야 합니다."),
    ])  # Text
    link = models.CharField(max_length=255,)
    salary = models.CharField(max_length=255,)
    logo = models.CharField(max_length=255,)
    location = models.CharField(max_length=255,)
    ceo = models.CharField(max_length=255,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    board = models.ForeignKey(
        Board, on_delete=models.SET_NULL, null=True, to_field='id')
    job_category = models.CharField(max_length=255,)
    location = models.CharField(max_length=255,)
    status = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField(validators=[
        validators.MinLengthValidator(10, "최소 10 글자 이상은 입력해주셔야 합니다."),
    ])
    content_pros = models.TextField(validators=[
        validators.MinLengthValidator(30, "최소 30 글자 이상은 입력해주셔야 합니다."),
    ])
    content_cons = models.TextField(validators=[
        validators.MinLengthValidator(30, "최소 30 글자 이상은 입력해주셔야 합니다."),
    ])
    content_hope = models.TextField(validators=[
        validators.MinLengthValidator(30, "최소 30 글자 이상은 입력해주셔야 합니다."),
    ])
    star = models.IntegerField()
    star_1 = models.IntegerField()
    star_2 = models.IntegerField()
    star_3 = models.IntegerField()
    star_4 = models.IntegerField()
    star_5 = models.IntegerField()
