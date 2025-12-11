from rest_framework import routers
from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [path('articles/tags/', views.TagListAPIView.as_view(), name='tags'),
               path('articles/categories/', views.CategoryListAPIView.as_view(), name='categories')]

router = routers.DefaultRouter()
router.register('articles', views.ArticleViewSet, basename='article')
urlpatterns += router.urls
