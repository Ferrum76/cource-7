from rest_framework import serializers

from task.models import Task
from task.validators import RewardValidator, RelatedTaskValidator


class TaskSerializer(serializers.ModelSerializer):
    """Сериализотор модели привычки"""

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user']
        validators = [
            RewardValidator(field='reward'),
            RelatedTaskValidator(field='related_task')
        ]
