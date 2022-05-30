from django import forms

from .models import Article, Category,Comment


class ArticleForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = ['title','content','category','publish']



class CategoryForm(forms.ModelForm):
    name = forms.CharField(required=False,min_length=1,max_length=255)
    class Meta:
        model = Category
        fields = ['name']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content':''}