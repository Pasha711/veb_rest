from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_confirm = data.get('password_confirmation')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        errors = {}

        if not username:
            errors['username'] = "Поле username є обов'язковим."
        if not email:
            errors['email'] = "Поле email є обов'язковим."
        if not password:
            errors['password'] = "Поле password є обов'язковим."
        if not password_confirm:
            errors['password_confirmation'] = "Повторне введення пароля є обов'язковим."

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        if len(username) > 150:
            errors['username'] = "Максимальна довжина username — 150 символів."
        if User.objects.filter(username=username).exists():
            errors['username'] = "Користувач з таким username вже існує."
        if User.objects.filter(email=email).exists():
            errors['email'] = "Користувач з таким email вже існує."

        try:
            validate_email(email)
        except ValidationError:
            errors['email'] = "Некоректний формат email (приклад: name@example.com)."

        if len(password) < 6:
            errors['password'] = "Мінімальна довжина пароля — 6 символів."
        if password != password_confirm:
            errors['password_confirmation'] = "Паролі не збігаються."

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return Response({
            "message": "Користувача успішно зареєстровано!",
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_201_CREATED)