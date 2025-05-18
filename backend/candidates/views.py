from rest_framework import viewsets, permissions, status
from .models import Candidate
from .serializers import CandidateSerializer
from users.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Candidate.objects.all()
        
        # Фильтр по вакансии
        vacancy_id = self.request.query_params.get('vacancy_id')
        if vacancy_id:
            queryset = queryset.filter(vacancy_id=vacancy_id)
            
        # Для HR - все кандидаты
        if self.request.user.role == 'HR':
            return queryset
            
        # Для менеджеров - только финальные статусы
        elif self.request.user.role == 'MANAGER':
            return queryset.filter(status__in=['FINAL', 'HIRED', 'REJECTED'])
            
        return queryset.none()

    # Создание кандидата (только для HR)
    def create(self, request, *args, **kwargs):
        if request.user.role != 'HR':
            raise PermissionDenied("Только HR может создавать кандидатов")
        return super().create(request, *args, **kwargs)

    # Обновление кандидата (только для HR)
    def update(self, request, *args, **kwargs):
        if request.user.role != 'HR':
            raise PermissionDenied("Только HR может редактировать кандидатов")
        return super().update(request, *args, **kwargs)

    # Частичное обновление (только для HR)
    def partial_update(self, request, *args, **kwargs):
        if request.user.role != 'HR':
            raise PermissionDenied("Только HR может редактировать кандидатов")
        
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)

    # Удаление кандидата (только для HR)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if request.user.role != 'HR':
            raise PermissionDenied("Только HR может удалять кандидатов")
        
        instance.delete()
        return Response(
            {"message": "Кандидат успешно удален"},
            status=status.HTTP_204_NO_CONTENT
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def move_to_tech(self, request, pk=None):
        candidate = self.get_object()
        
        if request.user.role != 'HR':
            raise PermissionDenied("Только HR может переводить на тех.собес")
            
        if candidate.status != Candidate.Status.HR_INTERVIEW:
            raise PermissionDenied("Кандидат должен быть на этапе HR собеседования")

        candidate.status = Candidate.Status.TECH_INTERVIEW
        candidate.save()
        return Response({'status': 'moved_to_tech'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        candidate = self.get_object()
        candidate._pre_save_status = candidate.status
        comment = request.data.get('comment', '')

        if request.user.role == 'HR':
            if candidate.status != Candidate.Status.HR_INTERVIEW:
                raise PermissionDenied("HR может отклонять только на своем этапе")
            candidate.status = Candidate.Status.HR_REJECTED
            candidate.hr_comment = comment
        elif request.user.role == 'MANAGER':
            candidate.status = Candidate.Status.REJECTED
            candidate.tech_comment = comment
        else:
            raise PermissionDenied("Недостаточно прав")

        candidate.save()
        return Response({'status': 'rejected'})
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        candidate = self.get_object()
        candidate._pre_save_status = candidate.status
        new_status = request.data.get('status')
        comment = request.data.get('comment', '')

        if not new_status:
            raise ValidationError("Статус обязателен")

        # Логика для HR
        if request.user.role == 'HR':
            # HR может переводить на любые статусы кроме финальных решений
            if new_status in [Candidate.Status.HIRED, Candidate.Status.REJECTED]:
                raise PermissionDenied("HR не может принимать финальные решения")
                
            # Обновляем соответствующие комментарии
            if new_status == Candidate.Status.TECH_INTERVIEW:
                candidate.hr_comment = comment
            elif new_status == Candidate.Status.TECH_REJECTED:
                candidate.tech_comment = comment
            elif new_status == Candidate.Status.FINAL_REVIEW:
                candidate.tech_comment = comment

        # Логика для менеджеров
        elif request.user.role == 'MANAGER':
            if new_status not in [Candidate.Status.HIRED, Candidate.Status.REJECTED]:
                raise PermissionDenied("Менеджер может только принимать или отклонять")
            
            if candidate.status != Candidate.Status.FINAL_REVIEW:
                raise PermissionDenied("Можно работать только с кандидатами на финальном рассмотрении")

            candidate.tech_comment = comment
        else:
            raise PermissionDenied("Недостаточно прав")

        candidate.status = new_status
        candidate.save()
        
        return Response({
            'status': 'updated',
            'new_status': candidate.get_status_display(),
            'comment': comment
        })
    
    @action(detail=True, methods=['patch'])
    def update_hr_comment(self, request, pk=None):
        candidate = self.get_object()
        
        if request.user.role != 'HR':
            raise PermissionDenied("Только HR может обновлять HR комментарии")
            
        candidate.hr_comment = request.data.get('hr_comment', '')
        candidate.save()
        return Response({'status': 'hr_comment_updated'})

    @action(detail=True, methods=['patch'])
    def update_tech_comment(self, request, pk=None):
        candidate = self.get_object()
        
        if request.user.role != 'MANAGER':
            raise PermissionDenied("Только менеджер может обновлять технические комментарии")
            
        candidate.tech_comment = request.data.get('tech_comment', '')
        candidate.save()
        return Response({'status': 'tech_comment_updated'})