from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PlayerSerializer
from .models import Player

@api_view(['GET'])
def player_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 20  # Anzahl der Objekte pro Seite
    players = Player.objects.all()
    result_page = paginator.paginate_queryset(players, request)
    serializer = PlayerSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
