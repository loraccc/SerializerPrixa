from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import item
from rest_framework import status
from .serializers import itemSerializer
from rest_framework.views import APIView
# Create your views here.


class ItemListAPIView(APIView):
    def get(self, request):
        items = item.objects.all()
        serializer = itemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = itemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ItemDetail(APIView):
    def get_object(self, pk):
        
        return get_object_or_404(item, pk=pk)
    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = itemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)