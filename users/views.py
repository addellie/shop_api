from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from users.serializers import UserCreateSerializer, UserAuthoriseSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import UserConfirmation
import random


@api_view(['POST'])
def authorisation_api_view(request):
    serializer = UserAuthoriseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.create_user(username=username, password=password)

    # генерируем случайный код подтверждения
    confirmation_code = ''.join(random.choices(range(0, 10), k=6))

    # возвращаем ответ с данными пользователя и кодом подтверждения
    response_data = {'user_id': user.id, 'confirmation_code': confirmation_code}
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def confirm_api_view(request):
    # получаем данные подтверждения из запроса
    user_id = request.data.get('user_id')
    confirmation_code = request.data.get('confirmation_code')

    if not user_id or not confirmation_code:
        return Response({'error': 'User ID and confirmation code are required'}, status=status.HTTP_400_BAD_REQUEST)

    # ищем запись в модели UserConfirmation
    try:
        confirmation = UserConfirmation.objects.get(user_id=user_id, confirmation_code=confirmation_code)
    except UserConfirmation.DoesNotExist:
        return Response({'error': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)

    # устанавливаем флаг подтверждения в значение True
    confirmation.is_confirmed = True
    confirmation.save()

    return Response({'message': 'User confirmed successfully'}, status=status.HTTP_200_OK)
