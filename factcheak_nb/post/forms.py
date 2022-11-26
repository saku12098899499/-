from django import forms
from .models import Article,Request
from django.contrib.auth.models import User


""" 新規投稿フォーム """
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title","category","content","rating","image")
        labels = {
            "title":"タイトル",
            "category":"カテゴリー",
            "content":"内容",
            "rating":"レーティング",
            "image":"画像"
        }

    def save(self,user_id,image=None): # image=None で画像ファイルのアリナシ
        # save data using the self.cleaned_data dictionary
        data = self.cleaned_data
        user=User.objects.get(id=user_id)
        post = Article(title=data['title'], author=user,category=data['category'],content=data['content'],
        rating=data['rating'],image=image)
        post.save()


""" ファクトチェック依頼フォーム """
class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ("title","category","content","reward","wallet")
        labels = {
            "title":"タイトル",
            "category":"カテゴリ",
            "content":"内容",
            "reward":"報酬",
            "wallet":"ウォレットアドレス"
        }

    def save(self,user_id):
        # save data using the self.cleaned_data dictionary
        data = self.cleaned_data
        user=User.objects.get(id=user_id)
        post = Request(title=data['title'], post_user=user,category=data['category'],content=data['content'],
        reward=data['reward'],wallet=data['wallet'])
        post.save()



    #     title = models.CharField(max_length = 200) # 投稿記事のタイトル(文字サイズの編集,文字の挿入が可能)
    # content = models.TextField(max_length = 1000) # 記事本文(文字サイズの変更,文章の挿入が可能)
    

    # author = models.ForeignKey( # on_deleteを入れることが必須、参照先が削除された場合に紐付いているテーブルを削除
    #     'auth.User', 
    #     on_delete = models.CASCADE, # 該当のArticleテーブルが一緒に削除される
    # )
    
    # category = models.ForeignKey(
    #                 Category, verbose_name='カテゴリー',
    #                 on_delete=models.PROTECT
    #            )
    
    # rating = models.ForeignKey(
    #                 Rating, verbose_name='レーティング',
    #                 on_delete=models.PROTECT
    #            )
    
    # image = models.ImageField(
    #             upload_to='img/',
    #             blank=True,      # フィールド値の設定は必須でない
    #             null=True   )    # データベースにnullが保存されることを許容
