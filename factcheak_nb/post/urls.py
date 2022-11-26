from .models import Article #　同ディレクリ内のArticleをimport
from django.views import generic # 汎用ビュー(何度も同じコードを書くという反復動作を防ぐ)
from django.urls import path # Httpresponseから送られてきたurlにマッチするpathをurls.pyから探す
from . import views # postと同ディレクトリ(カレントパス(相対パス) from . import (ディレクトリ名))のviewsをimport


app_name = 'post' #以下ルーティング設定

urlpatterns = [
    path('', views.List_article.as_view(), name='index'),
    path('request_list/' , views.List_request.as_view() , name='request_list'),
    path('<int:pk>/', views.Detail_aritcle, name='detail'), # 主キーでDBのレコードを識別
    path('article_create/', views.Create_article, name='article_create'), # /create で新規書き込み用ページを表示
    path('<int:pk>/comment_create/', views.CommentView.as_view(), name='comment_create'), # /comment/がname='comment_create'で置き換えられている
    path('request/',views.Create_request, name='request')
]