from django.shortcuts import render, resolve_url, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView
from .models import Post, Like, Category
from django.urls import reverse_lazy
from .forms import PostForm, LoginForm, SignUpForm, SearchForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

class OnlyMyPostMixin(UserPassesTestMixin):
    raise_exception = True
    def test_func(self):
        post = Post.objects.get(id = self.kwargs['pk'])
        return post.author == self.request.user

class Index(LoginRequiredMixin, TemplateView):
    login_url = '/loginuser'
    template_name = 'myapp/index.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.all().order_by('-created_at')
        context = {
            'post_list': post_list,
        }
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    login_url = '/loginuser'
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('myapp:index')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, '投稿しました。')
        return resolve_url('myapp:index')


class PostDetail(LoginRequiredMixin, DetailView):
    login_url = '/loginuser'
    model = Post

    def get_context_data(self, *args, **kwargs):
        detail_data = Post.objects.get(id=self.kwargs['pk'])
        category_posts = Post.objects.filter(category=detail_data.category).order_by('-created_at')[:5]

        params = {
            'object': detail_data,
            'category_posts': category_posts,
        }
        return params

class PostUpdate(OnlyMyPostMixin, UpdateView):
    login_url = '/loginuser'
    model = Post
    form_class = PostForm

    def get_success_url(self):
        messages.info(self.request, '記事をを更新しました')
        return resolve_url('myapp:post_detail', pk=self.kwargs['pk'])

class PostDelete(OnlyMyPostMixin, DeleteView):
    login_url = '/loginuser'
    model = Post

    def get_success_url(self):
        messages.info(self.request, '記事を削除しました')
        return resolve_url('myapp:index')


class PostList(LoginRequiredMixin, ListView):
    login_url = '/loginuser'
    paginate_by = 5
    model = Post

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    login_url = '/loginuser'
    template_name = 'myapp/logout.html'


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'myapp/signup.html'
    success_url = reverse_lazy('myapp:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.info(self.request, 'ユーザー登録をしました')
        return HttpResponseRedirect(self.get_success_url())


@login_required
def Like_add(request, post_id):
    post = Post.objects.get(id=post_id)
    is_liked = Like.objects.filter(user = request.user, post = post_id).count()
    if is_liked > 0:
        messages.info(request, 'すでにお気に入りに追加済みです')
        return redirect('myapp:post_detail', post_id)
    like = Like()
    like.user = request.user
    like.post = post
    like.save()

    messages.success(request, 'お気に入りに追加しました')
    return redirect('myapp:post_detail', post.id)


class CategoryList(LoginRequiredMixin, ListView):
    login_url = '/loginuser'
    model = Category

    def get_queryset(self):
        return Category.objects.all().order_by('-name')


class CategoryDetail(LoginRequiredMixin, DetailView):
    login_url = '/loginuser'
    model = Category
    slug_field = 'name_en'
    slug_url_kwarg = 'name_en'

    def get_context_data(self, *args, **kwargs):
        detail_data = Category.objects.get(name_en=self.kwargs['name_en'])
        category_posts = Post.objects.filter(category=detail_data.id).order_by('-created_at')

        params = {
            'object': detail_data,
            'category_posts': category_posts,
        }

        return params


def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)

        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword']
            searchlist = Post.objects.filter(Q(title__icontains = freeword) | Q(content__icontains = freeword))
        
        params = {
            'freeword': freeword,
            'search_list': searchlist
        }

        return render(request, 'myapp/search.html', params)