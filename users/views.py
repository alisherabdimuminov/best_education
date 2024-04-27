from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from users.models import User

# @authentication_classes(IsAuthenticated)
# @permission_classes(TokenAuthentication)
@api_view(['POST'])
def login(request: HttpRequest):
    user = None
    token = None
    username = request.data.get("phone")
    password = request.data.get("password")
    try:
        user = User.objects.filter(username=username).first()
        check_password = user.check_password(password)
        if not check_password:
            return Response({
                "status": "error",
                "message": "Kalit so'z noto'g'ri"
            })
    except Exception as e:
        print(e)
        return Response({
            "status": "error",
            "message": "Telefon raqam topilmadi"
        })
    try:
        token = Token.objects.get_or_create(user=user)
        token[0].delete()
        token = Token.objects.create(user=user)
    except Exception as e:
        print(e)
        return Response({
            "status": "error",
            "message": "Token topilmadi"
        })
    return Response({
        "status": "success",
        "message": "",
        "token": str(token)
    })

# @authentication_classes(IsAuthenticated)
# @permission_classes(TokenAuthentication)
@api_view(['POST'])
def signup(request: HttpRequest):
    username = request.data.get("phone")
    password = request.data.get("password")
    last_name = request.data.get("last_name")
    first_name = request.data.get("first_name")
    try:
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()
        return Response({
            "status": "success",
            "message": "Hisob muvaffaqiyatli yaratildi."
        })
    except Exception as e:
        print(e)
        return Response({
            "status": "error",
            "message": "Telefon raqam allaqachon mavjud."
        })

@api_view(http_method_names=["GET"])
@authentication_classes(authentication_classes=[TokenAuthentication])
@permission_classes(permission_classes=[IsAuthenticated])
def logout(request):
    try:
        token = Token.objects.get_or_create(user=request.user)
        token[0].delete()
        token = Token.objects.create(user=request.user)
        return Response({
            "status": "success",
            "message": "Chiqildi"
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": e
        })

@api_view(http_method_names=["GET"])
@authentication_classes(authentication_classes=[TokenAuthentication])
@permission_classes(permission_classes=[IsAuthenticated])
def change_password(request: HttpRequest):
    try:
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        check_password = user.check_password(old_password)
        if not check_password:
            return Response({
                "status": "error",
                "message": "Eski kalit so'z mos kelmadi"
            })
        user.set_password(raw_password=new_password)
        user.save()
        return Response({
            "status": "success",
            "message": "Kalit so'z muvaffaqiyatli o'zgartirildi"
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": e
        })

@api_view(http_method_names=["GET"])
@authentication_classes(authentication_classes=[TokenAuthentication])
@permission_classes(permission_classes=[IsAuthenticated])
def change_data(request: HttpRequest):
    try:
        user = request.user
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return Response({
            "status": "success",
            "message": "Ma'lumotlar muvaffaqiyatli saqlandi"
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": e
        })

@api_view(http_method_names=["GET"])
@authentication_classes(authentication_classes=[TokenAuthentication])
@permission_classes(permission_classes=[IsAuthenticated])
def students(request):
    try:
        users_obj = User.objects.filter(is_student=True)
        users = []
        for user in users_obj:
            users.append({
                "id": user.pk,
                "phone": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "image": user.image.url,
                "activity": user.activity
            })
        return Response({
            "status": "success",
            "message": "",
            "users": users
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": e
        })
    
@api_view(http_method_names=["GET"])
@authentication_classes(authentication_classes=[TokenAuthentication])
@permission_classes(permission_classes=[IsAuthenticated])
def student(request, phone):
    user = None
    try:
        user = User.objects.filter(username=phone, is_student=True).first()
    except Exception as e:
        print(e)
        return Response({
            "status": "error",
            "message": "Talaba topilmadi."
        })
    if user:
        return Response({
            "id": user.pk,
            "phone": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "image": user.image.url
        })
    else:
        return Response({
            "status": "error",
            "message": "Talaba topilmadi"
        })
    
@api_view(http_method_names=["GET"])
@authentication_classes(authentication_classes=[TokenAuthentication])
@permission_classes(permission_classes=[IsAuthenticated])
def teachers(request):
    try:
        users_obj = User.objects.filter(is_student=False)
        users = []
        for user in users_obj:
            users.append({
                "id": user.pk,
                "phone": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "image": user.image.url,
                "description": user.description
            })
        return Response({
            "status": "success",
            "message": "",
            "users": users
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": e
        })
    
@api_view(http_method_names=["GET"])
@authentication_classes(authentication_classes=[TokenAuthentication])
@permission_classes(permission_classes=[IsAuthenticated])
def teacher(request, phone):
    user = None
    try:
        user = User.objects.filter(username=phone, is_student=False).first()
    except Exception as e:
        print(e)
        return Response({
            "status": "error",
            "message": "O'qituvchi topilmadi."
        })
    if user:
        return Response({
            "id": user.pk,
            "phone": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "image": user.image.url,
            "description": user.description
        })
    else:
        return Response({
            "status": "error",
            "message": "O'qituvchi topilmadi"
        })
