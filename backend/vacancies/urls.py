from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacancyViewSet

router = DefaultRouter()
router.register(r'vacancies', VacancyViewSet, basename='vacancy')

urlpatterns = [
    path('', include(router.urls)),
    path('api/vacancies/top/', VacancyViewSet.as_view({'get': 'top'}), name='vacancy-top'),
]