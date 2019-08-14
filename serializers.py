from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Feedback, Stuff, StuffType


class StuffTypeSerializer(ModelSerializer):

    class Meta:
        model = StuffType
        fields = '__all__'


class StuffSerializer(ModelSerializer):
    type = StuffTypeSerializer(read_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        kwargs_voucher = {
            'type_id': 1,  # Standard Type
            'amount': validated_data['points_amount'],
            'account': user,
        }

        voucher = Stuff(**kwargs_voucher)
        voucher.save()
        return voucher

    class Meta:
        model = Stuff
        fields = '__all__'
        read_only_fields = ('date_in', 'date_out')


class FeedbackSerializer(serializers.Serializer):
    rating = serializers.ChoiceField(choices=[1, 2, 3, 4, 5])
    comment = serializers.CharField(max_length=2048)

    def create(self, validated_data):
        obj = Feedback(**validated_data)
        obj.save()
        return obj
