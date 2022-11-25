from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import User, Beautician, Service, Beauticianphoto
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer, UserBeauticianSerializer, BeauticianRegistrationSerializer, BeauticianphotoSerializer, ServicesSerializer, ContactusSerializer, AddServiceSerializer, ServicesDetailSerializer, BeauticianService, BeauticianSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from api.helper import modify_input_for_multiple_files
from rest_framework.generics import ListAPIView
from .paginations import CustomPagePagination
from client_api.models import BeauticianServices
from client_api.serializers import BeauticianServicesSerializer, BeauticianServicesSerializerget


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return JsonResponse({
            'status': 201,
            'message': 'Registration successfully',
            'token': token,
            'data': serializer.data
        })

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                beautician = User.objects.get(email=user)
                beautician = beautician.is_beautician
                token = get_tokens_for_user(user)
                return JsonResponse({
                    'status': 200,
                    'access': token['access'],
                    'refresh': token['refresh'],
                    'message': 'Login successfully',
                    'email': serializer.data['email'],
                    'Beautician': beautician
                })
            else:
                return JsonResponse({
                    'status': 400,
                    'message': 'Invalid email or password'
                })
        return JsonResponse({
            'status': 400,
            'message': 'Invalid email or password'
        })

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return JsonResponse({
            'status': 200,
            'data': serializer.data
        })


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return JsonResponse({
                'status': 200,
                'message': 'password changed successfully'
            })
        else:
            return JsonResponse({
                'status': 400,
                'message': 'something went wrong'
            })

class SendPasswordResetEmailView(APIView):
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse({
            'status': 200,
            'message': 'Password reset link sent successfully, check your email'
        })

class UserPasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({
            'status': 200,
            'message': 'Password Reset Successfully'
        })

class UserBeauticianView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        serializer = UserBeauticianSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse({
            'status': 200,
            'message': 'successfully',
            'data': serializer.data
        })

class BeauticianGetView(APIView):
    def get(self, request, format=None):
        serv = request.query_params.getlist('service_id')
        data = BeauticianServices.objects.filter(services_id__in=serv)
        serilizer = BeauticianServicesSerializer(data, many=True)
        return JsonResponse({
            'status': 200,
            'total': len(serilizer.data),
            'data': serilizer.data
        })

class Paginationview(ListAPIView):
    queryset = Beautician.objects.all()
    serializer_class = BeauticianRegistrationSerializer
    pagination_class = CustomPagePagination


class BeauticianRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = BeauticianRegistrationSerializer(data=request.data)
        user = User.objects.get(id=request.user.id)
        serializer.is_valid(raise_exception=True)
        if Beautician.objects.filter(user_id=user).exists():
            return JsonResponse({
                'status': 400,
                'message': 'Already exist'
            })
        else:
            serializer.save(user_id=request.user)
            user.is_beautician = True
            user.save()
            return JsonResponse({
                'status': 201,
                'message': 'Registration successfully',
                'data': serializer.data
            })
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = Beautician.objects.filter(user_id=request.user.id)
        serializer = BeauticianRegistrationSerializer(user, many=True)
        return JsonResponse({
            'status': 200,
            'data': serializer.data
        })

    def put(self, request, format=None):
        beautician = Beautician.objects.get(user_id=request.user)
        serializer = BeauticianRegistrationSerializer(
            data=request.data, instance=beautician, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({
            'status': 201,
            'message': 'Beautician service updated successfully',
            'data': serializer.data
        })


class BeauticianphotoView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,format = None):
        user = request.data['user_id']
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for img_name in images:
            modified_data = modify_input_for_multiple_files(user,
                                                            img_name)
            serializer = BeauticianphotoSerializer(data=modified_data)
            if serializer.is_valid():
                serializer.save()
                arr.append(serializer.data)
            else:
                flag = 0

        if flag == 1:
            return JsonResponse({
            'status': 200,
            'message': 'images uploaded successfully',
            'data':arr,
            })
        else:
            return JsonResponse({
            'status': 400,
            'message': 'something went wrong',
            })

    def get(self, request, format=None):
        user = User.objects.get(pk=request.user.id)
        beautician= Beautician.objects.get(user_id=user.id)
        allimg = Beauticianphoto.objects.filter(user_id=beautician)
        serializer = BeauticianphotoSerializer(allimg, many=True)
        return JsonResponse({
            'status': 200,
            'data': serializer.data
        })

    def delete(self, request):
        id_li = request.query_params.getlist('id')
        data = Beauticianphoto.objects.filter(id__in=id_li).delete()
        return JsonResponse({
            'message': 'Deleted Photo'
        })

class ServicesView(APIView):
    def get(self, request, format=None):
        allservice = Service.objects.all()
        serializer = ServicesSerializer(allservice, many=True)
        data = []
        for service in list(serializer.data):
            for item in list(service.values()):
                data.append(item)

        return JsonResponse({
            'status': 200,
            'service': data
        })

class ServicesDetailView(APIView):
    def get(self, request, format=None):
        allservice = Service.objects.all()
        serializer = ServicesDetailSerializer(allservice, many=True)
        return JsonResponse({
            'status': 200,
            'service': serializer.data
        })

class AddServiceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        beautician = Beautician.objects.get(user_id=request.user.id)
        data = Service.objects.filter(beautician_id=beautician)
        serializer = AddServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(beautician_id=beautician)
        return JsonResponse({
            'status': 201,
            'data': serializer.data
        })

    def get(self, request, format=None):
        beautician = Beautician.objects.get(user_id=request.user.id)
        data = Service.objects.filter(beautician_id=beautician)
        serializer = AddServiceSerializer(data=request.data)
        return JsonResponse({
            'status': 201,
            'data': serializer.data
        })

class ContactusView(APIView):
    def post(self, request, format=None):
        serializer = ContactusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({
            'status': 200,
            'message': 'message send successfully',
            'data': serializer.data
        })

class BeauticianServiceView(APIView):
    def get(self, request, format=None):
        id_li = request.query_params.getlist('id')
        data = BeauticianServices.objects.filter(
            services_id__in=id_li).distinct()
        li = []
        for i in data:
            li.append(i.beautician_id.id)
        pro = Beautician.objects.filter(id__in=li)
        ser = BeauticianRegistrationSerializer(pro, many=True)
        serializer = BeauticianService(data, many=True)
        return JsonResponse({
            'status': 200,
            'message': 'message send successfully',
            'data': serializer.data,
            'profile': ser.data
        })


class BeauticianDetails(APIView):
    def get(self, request, format=None):
        id_list = request.query_params.getlist('beautician_id')
        profile_user = Beautician.objects.filter(id__in=id_list).distinct()
        serializer_profile = BeauticianRegistrationSerializer(
            profile_user, many=True)
        id_li = request.query_params.getlist('beautician_id')
        data = BeauticianServices.objects.filter(
            beautician_id__in=id_li).distinct()
        allimg = Beauticianphoto.objects.filter(user_id__in=id_list)
        serializer = BeauticianServicesSerializerget(data, many=True)
        serializer_photo = BeauticianphotoSerializer(allimg, many=True)
        return JsonResponse({
            'status': 200,
            'profile': serializer_profile.data,
            'service': serializer.data,
            'beautician_photos': serializer_photo.data
        })
