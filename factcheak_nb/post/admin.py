from django.contrib import admin #adminをimport
from .models import Category, Article ,Comment,Rating,Request# modelからArticleクラスをimport

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Article) # adminサイトにpostというwebアプリのArticleというモデルを追加
admin.site.register(Category) # asminサイトにcategoryモデルを追加
admin.site.register(Comment) # asminサイトにcommentモデルを追加
admin.site.register(Rating) # asminサイトにratingモデルを追加
admin.site.register(Request) # asminサイトにrequestモデルを追加