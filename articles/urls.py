from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('',views.ArticleList.as_view(),name='article-list'),
    path('create/',views.ArticleCreate.as_view(),name='article-create'),
    path('search/',views.article_search,name='article-search'),
    path('<slug:slug>/', views.ArticleDetail.as_view(), name='article-detail'),
    path('<slug:slug>/update/',views.ArticleUpdate.as_view(),name='article-update'),
    path('<slug:slug>/delete/', views.ArticleDelete.as_view(), name='article-delete'),

    path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='delete_comment'),


    path('category/create/',views.CategoryCreate.as_view(),name='category-create'),
]
