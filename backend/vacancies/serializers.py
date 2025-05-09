from rest_framework import serializers
from .models import Vacancy

class VacancySerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = Vacancy
        fields = ['id', 'title', 'description', 'status', 'created_by', 'created_at', 'can_edit']
        read_only_fields = ['created_by', 'created_at', 'can_edit']

    def get_can_edit(self, obj):
        request = self.context.get('request')
        return request and request.user.role == 'MANAGER'