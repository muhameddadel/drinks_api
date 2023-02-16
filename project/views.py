from django.http import JsonResponse
from .models import Drink
from .serializers import DrinkSerializer
from rest_framework import status
from rest_framework.decorators import api_view 
from rest_framework.response import Response

# without rest
# def drink_list(request):
#     """
#     -get all the drinks
#     -serialize them 
#     -return json
#     """
#     drinks = Drink.objects.all()
#     serializer = DrinkSerializer(drinks, many = True)

#     return JsonResponse({'drinks': serializer.data})


# with rest
@api_view(['GET', 'POST'])
def drink_list(request, format=None):
    """
    -get all the drinks
    -serialize them 
    -return json
    """
    if request.method == "GET":
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many = True)
        return Response({'drinks': serializer.data})
    
    elif request.method == 'POST':
        serializer = DrinkSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED )
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, pk, format=None):
    try:
        drinks = Drink.objects.get(pk = pk)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # GET
    if request.method == 'GET':
        serializer = DrinkSerializer(drinks)
        return Response(serializer.data)
    
    # PUT
    elif request.method == 'PUT':
        serializer = DrinkSerializer(drinks, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED )
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    elif request.method == 'DELETE':
        drinks.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)