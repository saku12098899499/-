from xml.dom.minidom import Document, DocumentFragment
from django.contrib import admin # djangoの標準ライブラリadminをimport
from django.urls import include , path # pathを検索
from django.views.generic import RedirectView # リダイレクトするために使用
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',RedirectView.as_view(url='/post/')),
    path('index.html',RedirectView.as_view(url='/post/')),
    path('post/', include('post.urls')),
    path('admin/', admin.site.urls),  # admin/のパスにアクセスすると管理サイトにアクセスできる
    path('accounts/', include('django.contrib.auth.urls')), # django.contrib.auth.urls ← template機能を使用
    path('accounts/',include('accounts.urls')),
]

if settings.DEBUG: # バグの原因を探して取り除く:debug
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # static(静的ファイルの配信URL、静的ファイルの保存先)を指定、
    # これによりURLと保存先が紐付けられ、URLにアクセスしたとき、静的ファイルの保存先につながる


