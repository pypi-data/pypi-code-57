from rest_framework import serializers
from .HMACToken import HmacToken, TokenPeriod
from .models import Token

class TokenSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=255)
    ctimes = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=256)

    def create(self, validated_data):
        user = validated_data['user']
        tokens = Token.objects.get(user=user).all()
        token = '' 
        if len(tokens) == 0:
            obj = Token.objects.create(user=user)
            obj.save()
            token = obj.token
        else:
            token = tokens[0].token
        login = user.login
        crypt = HmacToken(token, TokenPeriod.day)
        times, temp_token = crypt.getToken(login)
        self.login = login
        self.times = times
        self.token = temp_token
        return self