from cgitb import text
from email import contentmanager, message
from email.mime import base
import imp
from multiprocessing import context
from re import search
from tabnanny import verbose
from turtle import title
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category, Reviews 
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm, CommentForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация!!')
            return redirect('home')
        else:
            messages.error (request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form" : form})





def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form" : form})

def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    if request.method == "POST":
        form = ContactForm(data = request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'goloveikozhenya@mail.ru', ['goloveikozhenya77@gmail.com'] , fail_silently=False)
            if mail:
                messages.success(request, "Письмо отправлено!")  
            else:
                messages.error(request, 'Ощибка отправки письма!')
        else:
            messages.error(request, 'Ошибка валидации!')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {"form" : form})
    
    


class MyBlog(ListView):
    model = News
    template_name = 'news/BLOG.html'
    context_object_name = 'BLOG'


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    paginate_by = 4

    # def search(request):
    #     if 'q' in request.GET:
    #         q = request.GET['q']
    #         data = News.objects.filter(title__icontains = q)
    #     else:
    #         data = News.objects.all()
    #     context = {
    #         'data' : News
    #     }
    #     return render(request, 'news/home_news_list.html', context)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] ='Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')



class Price(ListView):
    model = News
    template_name = 'news/price.html'
    context_object_name = 'price'

class Faq(ListView):
    model = News
    template_name = 'news/faq.html'
    context_object_name = 'faq'

class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id = self.kwargs['category_id'], is_published = True).select_related('category')


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False
    
    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    
    def get_success_url(self):
        return '%s?id=%s'%(self.success_url, self.object.id)




class ViewNews(CustomSuccessMessageMixin ,FormMixin, DetailView):
    model = News
    context_object_name = 'news_item'
    form_class = CommentForm
    success_msg = "Комментарий создан!"

    def get_success_url(self, **kwargs):
        return reverse_lazy('view_news', kwargs={'pk' : self.get_object().id})
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return HttpResponse("Вы не авторизованы! Пожалуйста пройдите регистрацию!")
    
    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.product = self.get_object()
        #self.object.product = self.request.user
        self.object.save()
        return super().form_valid(form)





class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'


class Search(ListView):
    paginate_by = 2
    template_name = 'news/home_news_list2.html'
    context_object_name = 'news'


    def get_queryset(self):
        return News.objects.filter(title__icontains = self.request.GET.get("q"))

    def get_context_data(self, *args, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q")
        return context
