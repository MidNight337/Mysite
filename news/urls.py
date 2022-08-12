from django.urls import path
from django.views.decorators.cache import cache_page
# from .views import AddReview, success

from .views import *

urlpatterns = (
    #path('submit/', newcontact, name = 'contacter'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('', HomeNews.as_view(), name='home'),
    #path('',cache_page(60) (HomeNews.as_view()), name='home'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    #path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('BLOG/', MyBlog.as_view(), name = 'BLOG'),
    # path('submit/', AddReview.as_view(), name = 'submit'),
    # path('success/', success, name = 'success_page'),
    # path('submit/', newcontact, name = 'contacter'),
    path('price/', Price.as_view(), name ='price'),
)