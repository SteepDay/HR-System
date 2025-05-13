from rest_framework import serializers
from .models import Candidate
from vacancies.serializers import VacancySerializer  

class CandidateSerializer(serializers.ModelSerializer):
    vacancy = VacancySerializer(read_only=True)
    vacancy_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Candidate
        fields = [
            'id',
            'full_name',
            'email',
            'phone',
            'status',
            'hr_comment',
            'tech_comment',
            'vacancy',
            'vacancy_id',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_by', 'status', 'created_at', 'updated_at']