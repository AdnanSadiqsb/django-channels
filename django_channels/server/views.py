from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from .models import Category, Channel, Server
from .schema import server_list_docs
from .serializer import CategorySerializer, ChannelSerializer, ServerSerializer

# Create your views here.


@server_list_docs
class ServerListViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Server.objects.all()
        category = request.query_params.get("category")
        byUser = request.query_params.get("by_user") == "true"
        byId = request.query_params.get("by_id")

        if category:
            queryset = queryset.filter(Category__name=category)
        if byUser:
            if byUser and not request.user.is_authenticated:
                raise AuthenticationFailed("You are not authenticated")
            queryset = queryset.filter(members=request.user)
        if byId:
            queryset = queryset.filter(id=byId)

        serializer = ServerSerializer(queryset, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ["get", "post", "put", "delete"]


class ChannelviewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    http_method_names = ["get", "post", "put", "delete"]
