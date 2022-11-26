from distutils.command.upload import upload
from email.mime import image
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models # djangoのデータベースからdbコードをimport
from django.urls import reverse # djangoのurlに設定されたパラメータとして渡すと,URLを返す
from django.core import validators # validatorのインポート

""" スコアの選択 """
SCORE_CHOICES = [
    (1, '★'),
    (2, '★★'),
    (3, '★★★'),
    (4, '★★★★'),
    (5, '★★★★★'),
]


""" カテゴリーモデル """
class Category(models.Model):
    name = models.CharField('カテゴリー', max_length=50)

    def __str__(self):
        return self.name


""" レーティングモデル """
class Rating(models.Model):
    name = models.CharField('レーティング', max_length=50)

    def __str__(self):
        return self.name


""" メインモデル """
class Article(models.Model): # 以下テーブル作成
    ### メインモデル ###
    title = models.CharField(max_length = 200) # 投稿記事のタイトル(文字サイズの編集,文字の挿入が可能)
    content = models.TextField(max_length = 1000) # 記事本文(文字サイズの変更,文章の挿入が可能)
    

    author = models.ForeignKey( # on_deleteを入れることが必須、参照先が削除された場合に紐付いているテーブルを削除
        'auth.User', 
        on_delete = models.CASCADE, # 該当のArticleテーブルが一緒に削除される
    )
    
    category = models.ForeignKey(
                    Category, verbose_name='カテゴリー',
                    on_delete=models.PROTECT
               )
    
    rating = models.ForeignKey(
                    Rating, verbose_name='レーティング',
                    on_delete=models.PROTECT
               )
    
    image = models.ImageField(
                upload_to='img/',
                blank=True,      # フィールド値の設定は必須でない
                null=True   )    # データベースにnullが保存されることを許容

    created_at = models.DateTimeField(verbose_name='開始時刻',auto_now_add=True) # 投稿日の日時を表示
    updated_at = models.DateTimeField(verbose_name='終了時刻',auto_now=True) # 記事のタイトル、本文の更新日時を表示



    def __str__(self):
        return self.content 

    def get_absolute_url(self):
        return reverse('post:detail',kwargs={'pk':self.pk}) # /detail/数字　を返す



""" コメントモデル """
class Comment(models.Model):
    user = models.CharField('名前', max_length=255, default='')
    comment = models.TextField(verbose_name='レビューコメント', blank=False)
    score = models.PositiveSmallIntegerField(verbose_name='レビュースコア', choices=SCORE_CHOICES, default='3') # SCORE_CHOICESの中から選んで保存
    target_id = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField(auto_now_add=True)
    #　追加
    #eval_number = models.IntegerField(verbose_name='トータル数',blank=True,null=True,default=1)
    #eval_score = models.IntegerField(verbose_name='トータルスコア',blank=True,null=True,default=1)

    def get_percent(self):
        percent = round(self.score / 5 * 100)
        return percent

    def __str__(self):
        return self.comment[:20]


""" リクエストモデル """
class Request(models.Model):
    title = models.CharField(max_length = 200)
    post_user = models.ForeignKey( # on_deleteを入れることが必須、参照先が削除された場合に紐付いているテーブルを削除
        'auth.User', 
        on_delete = models.CASCADE, # 該当のArticleテーブルが一緒に削除される
    )
    category = models.ForeignKey(
                    Category, verbose_name='カテゴリー',
                    blank = True,
                    null = True,
                    on_delete=models.PROTECT
               )
    content = models.TextField(max_length = 1000)
    reward = models.DecimalField(
        verbose_name='報酬',
        max_digits=5,
        decimal_places=3,
        default = 0.001,
        validators=[validators.MinValueValidator(0.001),
                    validators.MaxValueValidator(10)]
    )
    wallet = models.CharField(max_length = 1000)
    starttime = models.DateTimeField(auto_now_add=True)
    endtime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content 