from ast import arg
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from articles.forms import ArticleForm, CategoryForm,CommentForm
from .models import Article, Category, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,View

class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 2


def article_search(request):
    query = request.GET.get('q')
    qs = Article.objects.search(query)
    context = {'qs':qs}
    return render(request,'articles/search.html',context)


class ArticleDetail(DetailView):
    model = Article
    extra_context = {'form': CommentForm()}


    def get(self, request,*args, **kwargs):
        article = self.get_object()
        if article.publish or request.user.is_staff or request.user == article.user:
            self.extra_context['like_button'] = 'like'
            if article.is_liked_by_user(request):
                self.extra_context['like_button'] = 'unlike'
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden()

    def post(self,request, *args, **kwargs):
        form = CommentForm(request.POST)
        article = self.get_object()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()

        if 'like' in request.POST:
            article.like_or_unlike(request)

        return redirect(article)


class ArticleCreate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        article_form = ArticleForm()
        category_form = CategoryForm()
        ctx = {'form': article_form, 'category_form': category_form}
        return render(request, 'articles/article_form.html', ctx)

    def post(self, request, *args, **kwargs):
        article_form = ArticleForm(request.POST)
        category_form = CategoryForm(request.POST)
        ctx = {'article_form': article_form, 'category_form': category_form}
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            if category_form.is_valid():
                cat = category_form.cleaned_data.get('name')
                if cat is not None and cat != '':
                    cat = category_form.save()
                    article.category = cat
            article.save()
            return redirect(article)
        return render(request, 'articles/article_form.html', ctx)


class ArticleUpdate(LoginRequiredMixin,UserPassesTestMixin, UpdateView):

    def test_func(self):
        user = self.request.user
        article = self.get_object()
        if user == article.user or user.is_staff:
                return True
        return False

    model = Article
    form_class = ArticleForm


class ArticleDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        user = self.request.user
        article = self.get_object()
        if user == article.user or user.is_staff:
            return True
        return False
    
    model = Article
    success_url = '/'

class CommentDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    def test_func(self):
        user = self.request.user
        comment = self.get_object()
        if user == comment.user or user.is_staff:
            print(self.request.path)
            return True
        return False

    def get_success_url(self) :
        comment = self.get_object()
        return reverse('articles:article-detail',args=[comment.article.slug])


    model = Comment
    # comment = ''
    # success_url = '/'



class CategoryCreate(CreateView):
    model = Category
    form_class = CategoryForm
    # print('re')

