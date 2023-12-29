from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import item
from .serializers import itemSerializer

# Create your views here.


@api_view(['GET'])
def getData(request):
    Item=item.objects.all()
    serializer=itemSerializer(Item,many=True)
    return Response(serializer.data)