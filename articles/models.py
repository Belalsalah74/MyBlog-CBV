from unicodedata import category
from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def articles(self):
        return self.article_set.all()

    def __str__(self):
        return self.name

class ArticleManager(models.Manager):
    def get_queryset(self) :
        return super().get_queryset()

    def published(self):
        return self.get_queryset().filter(publish=True)
    
    def draft(self):
        return self.get_queryset().filter(publish=False)

    def search(self,query):
        if len(str(query)) > 1:
            return self.published().filter(
                Q(title__icontains=query) | Q(category__name__icontains=query) |     Q(user__username=query)
                )
            return None

class Article(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='articles')
    title = models.CharField(max_length=255,unique=True, validators=[MinLengthValidator(1)])
    content = models.TextField(blank=True,null=True)
    slug = models.CharField(max_length=255,null=True,blank=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    likes = models.ManyToManyField(User,blank=True,related_name='likes')
    objects = ArticleManager()

    class Meta:
        ordering = ['-updated','-created','-id']
   
    def __str__(self) -> str:
        return self.title
    
    def is_liked_by_user(self,request):
        user = request.user
        if self.likes.filter(id=user.id):
            return True
        return False

    def like_or_unlike(self,request):
        user = request.user
        if self.is_liked_by_user(request):
            self.likes.remove(user.id)
        else:
            self.likes.add(user.id)




    def get_absolute_url(self):
        return reverse("articles:article-detail", args=[self.slug])
    
    


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    content = models.TextField(validators=[MinLengthValidator(1)])
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created', '-id']

    def __str__(self) -> str:
        return f'comment {self.id}'

    def get_absolute_url(self):
        return reverse("articles:article-detail", args=[self.article.slug])
    


# class Tag(models.Model):
#     pass
