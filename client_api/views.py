from django.shortcuts import render
from .serializers import AppointmentSerlizer, AvailabilitiesSerializers, BeauticianServicesSerializer, BeauticianServicesSerializerget
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework import status
from .models import AppointmentModel, BeauticianAvailabilities, BeauticianServices
from api.models import Beautician, User
from api.serializers import BeauticianRegistrationSerializer, ServicesSerializer
import json


class AvailabilitiesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = AvailabilitiesSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        return JsonResponse({
            'status': 201,
            'message': 'Beautician Availabilities set successfully',
            'data': serializer.data
        })


class BeauticianServicesView(APIView):
    def get(self, request, format=None):
        user = User.objects.get(pk=request.user.id)
        if user.is_beautician:
            id_li = request.query_params.getlist('beautician_id')
            data = BeauticianServices.objects.filter(
                beautician_id__in=id_li).distinct()
            li = []
            for i in data:
                li.append(i.beautician_id.id)
            serializer = BeauticianServicesSerializerget(data, many=True)
            return JsonResponse({
                'status': 200,
                'data': serializer.data
            })
        else:
            data = BeauticianServices.objects.all()
            serializer = BeauticianServicesSerializer(data, many=True)
            return json.dumps(serializer.data)

    def post(self, request, format=None):
        serializer = BeauticianServicesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({
            'status': 201,
            'message': 'Beautician service add successfully',
            'data': serializer.data
        })

    def put(self, request, format=None):
        beautician = Beautician.objects.get(user_id=request.user)
        service = BeauticianServices.objects.get(beautician_id=beautician)
        serializer = BeauticianServicesSerializerget(
            data=request.data, instance=service, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({
            'status': 201,
            'message': 'Beautician service updated successfully',
            'data': serializer.data
        })


class AppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        appt = AppointmentModel.objects.filter(user_id=request.user.id)
        user = User.objects.get(pk=request.user.id)
        beautician = list()
        data = dict()
        for app in appt:
            ser = app.appointment_service.all().values()
            data = app.__dict__.copy()
            data['appointment_service'] = list(ser.values())
            data.pop('_state')
            beautician.append(data)
        if not user.is_beautician:
            return JsonResponse({
                'status': 200,
                'data': beautician
            })
        else:
            beauty = Beautician.objects.get(user_id=request.user.id)
            user_id = BeauticianServices.objects.get(beautician_id=beauty)
            appt = AppointmentModel.objects.filter(beautician_id=user_id.id)
            data = dict()
            beautician = list()
            for app in appt:
                ser = app.appointment_service.all().values()
                data = app.__dict__.copy()
                data['appointment_service'] = list(ser.values())
                data.pop('_state')
                beautician.append(data)
            return JsonResponse({
                'massage':'all Beuticians appointment',
                'data': beautician
            })

    def post(self, request, format=None):
        serializer = AppointmentSerlizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        beautician = json.loads(BeauticianServicesView().get(request))[0]
        flag = True
        for service in data.get("appointment_service"):
            if service.id in beautician['services_id']:
                serializer.save(user_id=request.user)
                flag = True
                return JsonResponse({
                    'status': 201,
                    'message': 'Appointment successfully',
                    'data': serializer.data
                })
            else:
                flag = False
        if flag is False:
            return JsonResponse({'message': 'no data available'})

    def delete(self, request):
        id_li = request.query_params.getlist('id')
        data = AppointmentModel.objects.filter(id__in=id_li).delete()
        return JsonResponse({
            'message': 'Appointment successfully deleted'
        })

    def patch(self, request, format=None):
        id_li = request.query_params.getlist('id')
        data = AppointmentModel.objects.get(id__in=id_li)
        data.status = request.data["status"]
        data.save()
        ser = AppointmentSerlizer(data)
        return JsonResponse({
            'status': 201,
            'message': 'Appointment successfully patched',
            'data': ser.data
        })
