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
        return JsonResponse({"data":serializer.data})

    if request.method == 'POST':
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
