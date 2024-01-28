from rest_framework import serializers
from .models import Data_PAC, Data_FLAP
class DataPACSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data_PAC
        fields = ['id','name','score']

class DataFLAPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data_FLAP
        fields = ['id','name','score']