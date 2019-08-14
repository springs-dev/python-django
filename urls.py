from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'v1/stuff', views.StuffViewSet, base_name='stuff')

urlpatterns = router.urls
