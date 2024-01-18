from rest_framework.serializers import ModelSerializer

from domain.apps.honeypot.models import LoginAttempt
class LoginAttemptModelSerializer(ModelSerializer):
    class Meta:
        model = LoginAttempt
        fields = ['id', 'username', 'password', 'ip', 'session_key', 'user_agent', 'path', 'created_date']
        read_only_fields = ['id', 'created_date']