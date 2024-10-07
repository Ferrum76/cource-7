from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'city', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}