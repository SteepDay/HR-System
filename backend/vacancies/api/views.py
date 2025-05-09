from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Vacancy
from ..serializers import VacancySerializer
from rest_framework.exceptions import PermissionDenied

class VacancyViewSet(viewsets.ModelViewSet):
    serializer_class = VacancySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Vacancy.objects.all()
    
        # Для HR - только открытые вакансии
        if self.request.user.role == 'HR':
            return queryset.filter(status='OPEN')
    
        # Для руководителей - все вакансии
        elif self.request.user.role == 'MANAGER':
            return queryset
        
        return queryset.none()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['put'])
    def publish(self, request, pk=None):
        vacancy = self.get_object()
        vacancy.status = 'OPEN'
        vacancy.save()
        return Response({'status': 'published'})

    @action(detail=True, methods=['put'])
    def close(self, request, pk=None):
        vacancy = self.get_object()
        vacancy.status = 'CLOSED'
        vacancy.save()
        return Response({'status': 'closed'})
    
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
    
        # HR может только просматривать открытые вакансии
        if request.user.role == 'HR' and obj.status != 'OPEN':
            raise PermissionDenied("HR can only view OPEN vacancies")
        
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)