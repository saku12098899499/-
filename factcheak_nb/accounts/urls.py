from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(),name = 'signup'),
    path('mypage/', views.Mypage, name='mypage'), # 追加
]