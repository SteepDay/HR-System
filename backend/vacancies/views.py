from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Vacancy
from candidates.models import Candidate
from .serializers import VacancySerializer

class VacancyViewSet(viewsets.ModelViewSet):
    serializer_class = VacancySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Vacancy.objects.all()
        
        if self.request.user.role == 'HR':
            return queryset.filter(status='OPEN')
        elif self.request.user.role == 'MANAGER':
            return queryset
        return queryset.none()

    @action(detail=False, methods=['get'])
    def all_stats(self, request):
        from django.db.models import Count, Q
        
        vacancies = Vacancy.objects.annotate(
            total_candidates=Count('candidates'),
            hired_candidates=Count(
                'candidates',
                filter=Q(candidates__status=Candidate.Status.HIRED)
            ),
            in_progress_candidates=Count(
                'candidates',
                filter=Q(
                    Q(candidates__status=Candidate.Status.HR_INTERVIEW) |
                    Q(candidates__status=Candidate.Status.TECH_INTERVIEW) |
                    Q(candidates__status=Candidate.Status.FINAL_REVIEW)
                )
            )
        ).order_by('-total_candidates')

        result = []
        for vacancy in vacancies:
            result.append({
                'id': vacancy.id,
                'title': vacancy.title,
                'count': vacancy.total_candidates,
                'hired': vacancy.hired_candidates,
                'in_progress': vacancy.in_progress_candidates
            })

        return Response(result)

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