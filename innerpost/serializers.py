from rest_framework import serializers 

from .models import Letter, Mail


class LetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Letter
        fields = '__all__'


class MailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mail
        fields = '__all__'