from django.shortcuts import render
from articles.models import Article
from django.utils import timezone

def index(request):
    articles = Article.objects.published()[:5]
    return render(request,'index.html',{'articles':articles})