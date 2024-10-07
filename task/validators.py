from rest_framework import serializers


class RewardValidator:
    """
    Валидатор поля reward.
    Проверяет условия:
    - У приятной привычки не может быть вознаграждения.
    - В модели не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки.
    Можно заполнить только одно из двух полей.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reward = value.get(self.field)
        related_task = value.get('related_task')
        is_nice = value.get('is_nice')
        if reward and is_nice:
            raise serializers.ValidationError('У приятной привычки не может быть вознаграждения')
        elif reward and related_task:
            raise serializers.ValidationError(
                'В модели не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки.')


class RelatedTaskValidator:
    """
    Валидатор поля related_task.
    Проверяет условия:
    - В связанные привычки могут попадать только привычки с признаком приятной привычки.
    - У приятной привычки не может быть связанной привычки.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        related_task = value.get(self.field)
        pleasant_task = value.get('pleasant_task')
        if related_task and not related_task.pleasant_task:
            raise serializers.ValidationError(
                'В связанные привычки могут попадать только привычки с признаком приятной привычки.')
        if related_task and pleasant_task:
            raise serializers.ValidationError('У приятной привычки не может быть связанной привычки.')
