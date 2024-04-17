from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
app_name = "board"

urlpatterns = [
    path('', views.board_index, name="index"),
    path('<int:board_id>/', views.board_detail, name="detail"),
    path('register/', views.board_register, name='register'),
    path('<int:board_id>/comment/', views.board_comment, name='comment'),
    # path('write/', views.board_write, name="write"),
    path('<int:board_id>/edit/', views.board_edit, name="edit"),
    path('<int:board_id>/del/', views.board_delete, name='delete'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
    #     path('', views.board_list, name='index'),
    #     path('<int:board_id>/',
    #          views.board_detail,
    #          name="board_detail"),
    #     path('comments/',
    #          views.comment_list,
    #          name="comment_list"),
]

# if settings.DEBUG:
#     urlpatterns += + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
