from django.http import JsonResponse
from .models import Data_FLAP, Data_PAC
from .serializers import DataPACSerializer, DataFLAPSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST', 'DELETE'])
def data_pac(request):
    if request.method == 'GET':
        data_points = Data_PAC.objects.all() # get all data
        serializer = DataPACSerializer(data_points, many=True)
        return JsonResponse({"data": serializer.data})

    if request.method == 'POST':
        serializer = DataPACSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'POST', 'DELETE'])
def data_flap(request):
    if request.method == 'GET':
        data_points = Data_FLAP.objects.all() # get all data
        serializer = DataFLAPSerializer(data_points, many=True)
        return JsonResponse({"data": serializer.data})

    if request.method == 'POST':
        serializer = DataFLAPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def data_change_pac(request, name):
    try:
        data = Data_PAC.objects.get(name=name)
    except Data_PAC.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DataPACSerializer(data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DataPACSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def data_change_flap(request, name):
    try:
        data = Data_FLAP.objects.get(name=name)
    except Data_FLAP.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = DataFLAPSerializer(data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DataFLAPSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

