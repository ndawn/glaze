from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSerializer, UserCreateSerializer

from rest_framework.generics import CreateAPIView
from rest_framework import viewsets, status


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        fields = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'last_name': request.data.get('last_name'),
            'first_name': request.data.get('first_name'),
        }

        serializer = UserCreateSerializer(data=fields)

        serializer.is_valid(raise_exception=True)

        user = serializer.create(serializer.validated_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
