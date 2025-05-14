from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateViewSet

router = DefaultRouter()
router.register(r'candidates', CandidateViewSet, basename='candidate')

urlpatterns = [
    
    path('', include(router.urls)),
    path('api/candidates/<int:pk>/update_hr_comment/', 
         CandidateViewSet.as_view({'patch': 'update_hr_comment'}), 
         name='update-hr-comment'),
    path('api/candidates/<int:pk>/update_tech_comment/', 
         CandidateViewSet.as_view({'patch': 'update_tech_comment'}), 
         name='update-tech-comment'),
    path('api/candidates/<int:pk>/move_to_tech/', CandidateViewSet.as_view({'post': 'move_to_tech'}), name='candidate-move-to-tech'),
    path('api/candidates/<int:pk>/change_status/', CandidateViewSet.as_view({'post': 'change_status'})),
    path('api/candidates/<int:pk>/reject/', CandidateViewSet.as_view({'post': 'reject'}), name='candidate-reject'),
]