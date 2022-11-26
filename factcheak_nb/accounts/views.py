from django.shortcuts import render #　Httpresponseとしてブラウザに返す
from django.contrib.auth.forms import UserCreationForm # 新しいユーザーを作成するためのModelForm
from django.urls import reverse_lazy #　ページ名からURLを取得
from django.views import generic # generic ← リクエスト処理をしレスポンスするviewの定義

from django.contrib.auth import get_user_model # 追加
from django.contrib.auth.mixins import UserPassesTestMixin # 追加
from django.contrib.auth.models import User

from django.shortcuts import render,get_object_or_404
from post.models import Article,Comment # 定義したarticle変数をimport
from django.db.models import Avg

class SignUpView(generic.CreateView): # Signupページを作成
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


def Mypage(request):
    user_info = get_object_or_404(User, id=request.user.id)
    post_info = Article.objects.filter(author_id =request.user.id).all()
    score_info = Comment.objects.filter(target_id_id=2).aaggregate(Avg('score'))
    return render(request, 'accounts/mypage.html', {'user_info': user_info,'post_info':post_info,'score_info':score_info})