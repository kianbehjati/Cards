from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Factor,Card
from .models import Card

class factor_serializer(ModelSerializer):
    card_number = SerializerMethodField()
    class Meta:
        model = Factor
        fields = [
            'card_number',
            'description',
            'amount',
            'status'
        ]

    def get_card_number(self,obj):
        return Card.objects.get(factor=obj.id).card_number

class card_serializer(ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'owner',
            'secret_key',
            'balance'
        ]
