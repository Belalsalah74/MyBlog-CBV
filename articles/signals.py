from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
from django.utils.text import slugify

@receiver(post_save, sender=Article)
def unique_slug(sender, instance, *args, **kwargs):

    if instance.slug is None or instance.slug == '':
        instance.slug = slugify(instance.title)
        qs = Article.objects.filter(slug=instance.slug).exclude(id=instance.id)
        if qs.exists():
            instance.slug = f'{instance.slug}-{instance.id}'
        instance.save()
