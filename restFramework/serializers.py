from rest_framework import serializers
from restFramework.models import item

class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model=item
        fields='__all__'