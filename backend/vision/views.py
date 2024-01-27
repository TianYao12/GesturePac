from django.http import JsonResponse
from .models import Data
from .serializers import DataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def data_points_list(request):
    if request.method == 'GET':
        data_points = Data.objects.all() # get all data
        serializer = DataSerializer(data_points, many=True)
        return JsonResponse({"data": serializer.data})

    if request.method == 'POST':
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def data_detail(request, id):
    try:
        data = Data.objects.get(pk=id)
    except Data.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DataSerializer(data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DataSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def latest_data_detail(request):
    try:
        latest_data = Data.objects.latest('id')
    except Data.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = DataSerializer(latest_data)
    return Response(serializer.data)