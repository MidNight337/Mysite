from itertools import product
from tabnanny import verbose
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class News(models.Model):
    author =models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Автор статьи', blank=True, null=True)
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

class Reviews(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    name = models.CharField("Имя", max_length= 150)
    text = models.TextField("Текст", max_length= 400)
    product = models.ForeignKey(News, verbose_name='Статья', on_delete=models.CASCADE, null = True, blank = True, related_name = 'comments_articles')
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария', blank = True, null = True)
    status = models.BooleanField(verbose_name="Видимость статьи", default = True)
    
    def __str__(self):
        return f'{self.name} - {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
# Create your models here.
