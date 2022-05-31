from django.db import models
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(blank=True, verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True, verbose_name='Фото')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT,null=True, verbose_name='Категория')
    views = models.IntegerField(default = 0)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

class Meta:
    verbose_name = 'Новость'
    verbose_name_plural = 'Новости'
    ordering = ['-created_at']

class Category (models.Model):
    title = models.TextField(max_length=150, db_index=True, verbose_name='Название категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

class Meta:
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'
    ordering = ['title']

# Create your models here.
