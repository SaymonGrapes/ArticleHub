from rest_framework import routers

from . import views

urlpatterns = []

router = routers.DefaultRouter()
router.register('articles', views.ArticleViewSet)
urlpatterns += router.urls
