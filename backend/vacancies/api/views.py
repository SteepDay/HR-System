from rest_framework import viewsets, permissions
from rest_framework.response import Response
from ..models import Vacancy
from ..serializers import VacancySerializer

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)