from importlib.resources import contents
from turtle import title
from django.shortcuts import render,redirect,get_object_or_404 # オブジェクトを返す
from .models import Article,Comment,Request # 定義したarticle変数をimport
from .forms import ArticleForm,RequestForm
from django.views import generic #　汎用ビュー(反復動作を防ぐ)
from django.urls import reverse_lazy # ページ名からURLを取得するためのメソッド
from django.contrib.auth.mixins import LoginRequiredMixin # ユーザがログインしている場合だけページ表示
from django.core.exceptions import PermissionDenied # 特定ユーザからのアクセス制限をかける  django.core.exceptions ← 例外クラス
from django.db.models import Q,Count,Avg,F  # or検索や否定条件を指定可
from django.views.generic import TemplateView
from django import forms
from django.http import HttpResponse

from django.db.models.functions import Coalesce

import post.post_factcheak as fk


""" 投稿一覧ページ """
class List_article(generic.ListView): # ListViewで一覧ページを作成
    model = Article  # リスト作成するモデル
    paginate_by = 5

    def get_queryset(self):  # モデルインスタンスの一覧を返すメソッド
        q_word = self.request.GET.get('query') # requestからgetメソッドを使ってデータを取得

        #　以下、チェックボックスにチェックが入っている項目 
        selected_title = self.request.GET.get('title')
        selected_article = self.request.GET.get('article')

        if q_word:
            if selected_title and selected_article:
                object_list = Article.objects.filter(Q(title__icontains=q_word) | Q(content__icontains=q_word))
                # icontainsで大文字,小文字区別無し  |でor文
            elif selected_title:
                object_list = Article.objects.filter(Q(title__icontains=q_word))    
            else:
                object_list = Article.objects.filter(Q(content__icontains=q_word))
        else: # 投稿内容のみ、または両方ともチェックされていないときは投稿内容のみを検索する
            object_list = Article.objects.all()

        return object_list           


""" ファクトチェック依頼一覧ページ """
class List_request(generic.ListView): # ListViewで一覧ページを作成
    model = Request  # リスト作成するモデル
    paginate_by = 5

    def get_queryset(self):  # モデルインスタンスの一覧を返すメソッド
        q_word = self.request.GET.get('query') # requestからgetメソッドを使ってデータを取得

        #　以下、チェックボックスにチェックが入っている項目 
        selected_title = self.request.GET.get('title')
        selected_article = self.request.GET.get('article')

        if q_word:
            if selected_title and selected_article:
                object_list = Request.objects.filter(Q(title__icontains=q_word) | Q(content__icontains=q_word))
                # icontainsで大文字,小文字区別無し  |でor文
            elif selected_title:
                object_list = Request.objects.filter(Q(title__icontains=q_word))    
            else:
                object_list = Request.objects.filter(Q(content__icontains=q_word))
        else: # 投稿内容のみ、または両方ともチェックされていないときは投稿内容のみを検索する
            object_list = Request.objects.all()

        return object_list           



""" 新規投稿記事　詳細ページ """
def Detail_aritcle(request,pk):
    object= get_object_or_404(Article, id=pk)   # id(記事作成時につけられるid)とpk(urlの上数字)が一致したときreturn
    comment = Comment.objects.filter(target_id_id = pk).all()
    average = comment.aggregate(Avg("score"))
    if average["score__avg"] == None:
            average = 0
    else:
        print(average["score__avg"])
        average = round(average["score__avg"],1)
    
    return render(request, 'post/detail_article.html', {'object': object,'comment':comment,'average':average}) # DetailViewで個別の詳細ページをDBテーブルからレコード一列ずつデータを取得


""" ファクトチェック依頼　詳細ページ """
# def Detail_request(request,pk):
#     object=get_object_or_404(Request, id=pk)
#     context = {'object':object}
#     return render(request,'post/detail_request.html', context)


""" 新規投稿ページ """
def Create_article(request, *args, **kwargs):
    if request.method == 'GET':
        
        content={"form":ArticleForm}
        return render(request, 'post/article_form.html',context=content) # DetailViewで個別の詳細ページをDBテーブルからレコード一列ずつデータを取得

    if request.method == 'POST':
        print('////////////////////////////////////////////')
        textdata = str([request.POST["title"],request.POST["category"],request.POST["content"],request.POST["rating"]])
        print(textdata)
        fk.post(textdata)
        print('/////////////////////////////////////////////////////')
        params = {'message': '', 'form': None}
        form = ArticleForm(request.POST)
        if form.is_valid():
            image=None
            try:
                image=request.FILES["image"]
            except:
                pass
            form.save(user_id=request.user.id,image=image)
            return redirect("/post")
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form


# """ 新規投稿ページ """
# def Create_article(request, *args, **kwargs):
#     if request.method == 'GET':
#         print('GETリクエスト')
#         content={"form":ArticleForm}
#         return render(request, 'post/article_form.html',context=content) # DetailViewで個別の詳細ページをDBテーブルからレコード一列ずつデータを取得

#     if request.method == 'POST':
#         print('POSTリクエスト')
#         params = {'message': '', 'form': None}
#         form = ArticleForm(request.POST)
#         if form.is_valid():
#             print(request.FILES["image"])
#             form.save(user_id=1,image=request.FILES["image"])
#             return redirect("/post")
#         else:
#             params['message'] = '再入力して下さい'
#             params['form'] = form



# class CreateView(LoginRequiredMixin, generic.edit.CreateView, forms.ModelForm): # CreateViewでDBに新規レコードを追加,フォーム作成が主
#     model = Article
#     fields = ['content', 'title','category', 'image','rating'] # fileds変数を定義し、定義したデータフィールド('contest' , 'title' ,...)以外を無視


#     def form_valid(self , form): # フォームフィールドが有効かどうか確認(フォーム登録時の処理)
#         form.instance.author = self.request.user # ログイン中のユーザを取得
#         print("------------------")
#         new_post = self.request.POST["title"]+self.request.POST["category"]+self.request.POST["content"]+self.request.POST["rating"]
#         print(new_post)
#         print("--------------------")
#         return super(CreateView, self).form_valid(form) # 有効であればsuperを呼び出してユーザーIDをフォームに挿入
    


# """ 投稿記事編集ページ """
# def Edit_article(request, pk):
#     object_edit = Article.objects.get(id=pk)
#     context = {'object_edit': object_edit}
#     if request.method == 'POST':
#         object.title = request.POST['title']
#         object.category = request.POST['category']
#         object.content = request.POST['content']
#         object.image = request.POST['image']
#         object.save()
#     else:
#         return render(request, 'post/edit_article.html', context)
        


# class UpdateView(LoginRequiredMixin,generic.edit.UpdateView, forms.ModelForm): # CreateViewと同様,　投稿内容の変更処理
#     model = Article
#     fields = ['content', 'title','category', 'image','rating']

#     def dispatch(self , request , *args , **kwargs): # *argsで複数の引数をリストとして受け取る　、　**kwargsで複数のキーワード引数を辞書として受け取る
#         obj = self.get_object() # 単一のオブジェクトを取得

#         if obj.author != self.request.user: # modelsで定義したauthorとuserが同一かどうかの確認
#             raise PermissionDenied('You do not have permission to edit.') # エラーメッセージ表示
        
#         return super(UpdateView,self).dispatch(request, *args, **kwargs) # スーパークラスからdispatchを受取り辞書型変数kwargs変数を返す



class CommentView(generic.CreateView):  #　記事のレビュー
    """コメント投稿ページ"""
    template_name = 'post/comment_form.html' # post/から指定したいhtmlを入れる
    model = Comment
    fields = ['user','comment','score',]
    

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Article, pk=post_pk)
        comment = form.save(commit=False)
        comment.target_id = post
        comment.save()
        return redirect('post:detail', pk=post_pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Article, pk=self.kwargs['pk'])
        return context




""" ファクトチェック依頼ページ """
def Create_request(request, *args, **kwargs):
    if request.method == 'GET':
        print('GETリクエスト')
        content={"form":RequestForm}
        return render(request, 'post/request.html',context=content) # DetailViewで個別の詳細ページをDBテーブルからレコード一列ずつデータを取得

    if request.method == 'POST':
        print('POSTリクエスト')
        params = {'message': '', 'form': None}
        form = RequestForm(request.POST)
        if form.is_valid():
           
            form.save(user_id=request.user.id)
            return redirect("/post")
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form



#class detail_Request(generic.CreateView, forms.ModelForm):
    #template_name = 'post/request.html'
    #model = Request
    #fields = ['title','category','content','reward','wallet']
    #def form_valid(self , form): # フォームフィールドが有効かどうか確認(フォーム登録時の処理)
        #orm.instance.author = self.request.user # ログイン中のユーザを取得
        #print("------------------")
        
        #print("--------------------")
        #return super(detail_Request, self).form_valid(form) # 有効であればsuperを呼び出してユーザーIDをフォームに挿入
    # def post(self , form): # フォームフィールドが有効かどうか確認(フォーム登録時の処理)
    #     print("aaaaa")
    #     return super(CreateView, self).form_valid(form) # 有効であればsuperを呼び出してユーザーIDをフォームに挿入
    
    
    #     return redirect("/")
    

    