from rest_framework import serializers
from .models import Vacancy

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id', 'title', 'description', 'status', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']