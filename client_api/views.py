from django.shortcuts import render
from .serializers import AppointmentSerlizer, AvailabilitiesSerializers, BeauticianServicesSerializer, BeauticianServicesSerializerget, RatingSerlizer, BlogSerlizer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import AppointmentModel, BeauticianAvailabilities, BeauticianServices, Ratingmodel, Blogmodel
from api.models import Beautician, User, Beauticianphoto
from api.serializers import BeauticianRegistrationSerializer, BeauticianphotoSerializer, BeauticianSerializer
import json
from rest_framework.generics import ListAPIView
from api.paginations import AppointmentPagePagination
import datetime
from datetime import date
from django.core.paginator import Paginator
from django.conf import settings

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

    def get(self, request, format=None):
        user = BeauticianAvailabilities.objects.filter(user_id=request.user.id)
        serializer = AvailabilitiesSerializers(user, many=True)
        return JsonResponse({
            'status': 200,
            'message': 'Beautician Availabile',
            'data': serializer.data
        })


class BeauticianServicesView(APIView):
    def get(self, request, format=None):
        user = User.objects.get(user_id=request.user.id)
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
        status = request.query_params.get('status')
        if status:
            appt = AppointmentModel.objects.filter(
                user_id=request.user.id, status=status)
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
                services = BeauticianAvailabilities.objects.get(
                    beautician_id=user_id.id)
                appt = AppointmentModel.objects.filter(
                    beautician_id=services.id, status=status)
                data = dict()
                beautician = list()
                for app in appt:
                    ser = app.appointment_service.all().values()
                    data = app.__dict__.copy()
                    data['appointment_service'] = list(ser.values())
                    data.pop('_state')
                    beautician.append(data)
                return JsonResponse({
                    'massage': 'all Beuticians appointment',
                    'data': beautician
                })
        else:
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
                services = BeauticianAvailabilities.objects.get(
                    beautician_id=user_id.id)
                appt = AppointmentModel.objects.filter(
                    beautician_id=services.id)
                data = dict()
                beautician = list()
                for app in appt:
                    ser = app.appointment_service.all().values()
                    data = app.__dict__.copy()
                    data['appointment_service'] = list(ser.values())
                    data.pop('_state')
                    beautician.append(data)
                serializer_class = beautician
                pagination_class = AppointmentPagePagination
                return JsonResponse({
                    'massage': 'all Beuticians appointment',
                    'data': beautician
                })
    def post(self, request, format=None):
        today = date.today()
        serializer = AppointmentSerlizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        valid_ser = serializer.validated_data
        beautician_avlibale = BeauticianAvailabilities.objects.filter(beautician_id=valid_ser.get('beautician_id').beautician_id.id)
        duration_data = list()
        ser_services=list()
        newlist_services=list()
        for curent_s in  valid_ser['appointment_service']:
            ser_services.append(curent_s.duration)
        for time_s in ser_services:
            ts_time = str(time_s)
            (h, m, s) = ts_time.split(':')
            new_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            newlist_services.append(new_time)
        appointment_start = str(valid_ser['appointment_time'])
        (h, m, s) = appointment_start.split(':')
        new_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        appointment_time = new_time+sum(newlist_services, datetime.timedelta(0, 0))
        appointment_end = (datetime.datetime.min + appointment_time).time()
        flag = True
        service_time = list()
        for available in beautician_avlibale:
            ser = BeauticianServices.objects.get(beautician_id=available.beautician_id.beautician_id.id)
            services_id = list()
            for service in ser.services_id.all().values('id'):
                services_id.append(service.get('id'))
            appointment_get =AppointmentModel.objects.filter(beautician_id=available.id, appointment_date=today)
            for appointment in appointment_get:
                duration_data.clear()
                for services_duration in appointment.appointment_service.all().values('duration'):
                    duration_data.append(services_duration.get('duration'))
                for ti_me in duration_data:
                    ttt = str(ti_me)
                    (h, m, s) = ttt.split(':')
                    d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    service_time.append(d)
                appoint_time = str(appointment.appointment_time)
                print('appointment time',appoint_time)
                (h, m, s) = appoint_time.split(':')
                new_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                appointment_time = new_time+sum(service_time, datetime.timedelta(0, 0))
                appointment_endtime = (datetime.datetime.min + appointment_time).time()
                print('total',appointment_endtime)
                service_time.clear()
                if valid_ser['appointment_time'] != appointment.appointment_time and valid_ser['appointment_time'] != appointment_endtime:
                    flag=True
                    if valid_ser['appointment_time'] < appointment.appointment_time and valid_ser['appointment_time'] > appointment_endtime:
                        flag= False
                        for appointment_services in valid_ser['appointment_service']:
                            if appointment_services.id in services_id:
                                    if valid_ser['appointment_date'] == today and available.start_date == today:
                                        if valid_ser['appointment_time']>=available.start_time and valid_ser['appointment_time']<=available.end_time:
                                            location = available.beautician_id.beautician_id.city
                                            if location == valid_ser['location']:
                                                print('valid')
                                                flag = True
                                            else:
                                                flag = False
                                        else:
                                            return JsonResponse({'message': 'Beautician is not avlibale'})
                                    else:
                                        return JsonResponse({'message': 'Beautician is not avlibale'})
                            else:
                                flag = False
                            break
                else:
                    flag = False
        if flag is False:
            return JsonResponse({'message': 'no data available'})
        else:
            # serializer.save(user_id=request.user)
            return JsonResponse({
                'status': 201,
                'message': 'Appointment successfully',
                'data': serializer.data
            })
    def delete(self, request):
        id_li = request.query_params.getlist('id')
        data = AppointmentModel.objects.filter(id__in=id_li).delete()
        return JsonResponse({
            'message': 'Appointment successfully deleted'
        })

    def patch(self, request, format=None):
        id_li = request.query_params.getlist('id')
        data = AppointmentModel.objects.get(id__in=id_li)
        if request.data["status"] == "Approved":
            data.status = request.data["status"]
            data.save()
            ser = AppointmentSerlizer(data)
            return JsonResponse({
                'status': 200,
                'message': 'Appointment Approved',
                'data': ser.data
            })
        elif request.data["status"] == "Rejected":
            data.status = request.data["status"]
            data.save()
            ser = AppointmentSerlizer(data)
            return JsonResponse({
                'status': 200,
                'message': 'Appointment Rejected',
                'data': ser.data
            })
        return JsonResponse({
            'status': 400,
            'message': 'something went wrong',
            'data': []
        })


class Paginationview(ListAPIView):
    serializer_class = AppointmentSerlizer
    pagination_class = AppointmentPagePagination

    def get_queryset(self):
        qs = AppointmentModel.objects.all()
        return qs

    def list(self, request):
        status = request.query_params.get('status')
        queryset = self.get_queryset().order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            if status:
                appt = AppointmentModel.objects.filter(
                    user_id=request.user.id, status=status)
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
                    return self.get_paginated_response(beautician)
                else:
                    beauty = Beautician.objects.get(user_id=request.user.id)
                    user_id = BeauticianServices.objects.get(
                        beautician_id=beauty)
                    services = BeauticianAvailabilities.objects.get(
                        beautician_id=user_id.id)
                    appt = AppointmentModel.objects.filter(
                        beautician_id=services.id, status=status)
                    data = dict()
                    beautician = list()
                    for app in appt:
                        ser = app.appointment_service.all().values()
                        data = app.__dict__.copy()
                        data['appointment_service'] = list(ser.values())
                        data.pop('_state')
                        beautician.append(data)
                        return self.get_paginated_response(beautician)
            else:
                appt = AppointmentModel.objects.filter(user_id=request.user.id)
                print(appt)
                print("page", self.pagination_class)
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
                    return self.get_paginated_response(beautician)

                else:
                    beauty = Beautician.objects.get(user_id=request.user.id)
                    user_id = BeauticianServices.objects.get(
                        beautician_id=beauty)
                    services = BeauticianAvailabilities.objects.get(
                        beautician_id=user_id.id)
                    appt = AppointmentModel.objects.filter(
                        beautician_id=services.id)
                    data = dict()
                    beautician = list()
                    for app in appt:
                        ser = app.appointment_service.all().values()
                        data = app.__dict__.copy()
                        data['appointment_service'] = list(ser.values())
                        data.pop('_state')
                        beautician.append(data)
                    return self.get_paginated_response(beautician)
        else:
            return self.get_paginated_response(beautician)


class RatingView(APIView):
    def post(self, request, format=None):
        serializer = RatingSerlizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        return JsonResponse({
            'status': 200,
            'data': serializer.data
        })

    def get(self, request, format=None):
        rating = Ratingmodel.objects.all()
        da = list()
        for rate in rating:
            data = int(rate.rating)
            da.append(data)
        print(da)
        max_rate = Ratingmodel.objects.filter(rating=str(max(da)))
        Beautician = []
        for i in max_rate:
            dictionaty = {
                'first_name': i.beautician_id.first_name,
                'last_name': i.beautician_id.last_name,
                'phone_number': i.beautician_id.phone_number,
                'address': i.beautician_id.address,
                'city': i.beautician_id.city,
                'state': i.beautician_id.state,
                'zip_code': i.beautician_id.zip_code,
                'id_proof': i.beautician_id.id_proof,
                'shop_name': i.beautician_id.shop_name,
                'profile_image': i.beautician_id.profile_image,
                'about_us': i.beautician_id.about_us
            }
            Beautician.append(dictionaty)
        ser = BeauticianRegistrationSerializer(Beautician, many=True)
        serializer = RatingSerlizer(max_rate, many=True)
        photo = Beauticianphoto.objects.filter(user_id_id=i.beautician_id)
        photo_ser = BeauticianphotoSerializer(photo, many=True)
        return JsonResponse({
            'satus': 200,
            'data': serializer.data,
            'profile': ser.data,
            'shop_photos': photo_ser.data
        })


class BlogView(APIView):
    def post(self, request, format=None):
        serializer = BlogSerlizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        return JsonResponse({
            'status': 200,
            'data': serializer.data
        })

    def get(self, request, format=None):
        data = Blogmodel.objects.all()
        serializer = BlogSerlizer(data, many=True)
        return JsonResponse({
            'status': 200,
            'data': serializer.data
        })

    def put(self, request, format=None):
        data_blog = Blogmodel.objects.get(user_id=request.user)
        serializer = BlogSerlizer(
            data=request.data, instance=data_blog, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({
            'status': 201,
            'message': 'Blog updated successfully',
            'data': serializer.data
        })


class AppointmentConfirmation(APIView):
    def get(self, request, format=None):
        id = request.query_params.get('id')
        user = AppointmentModel.objects.filter(id=id)
        services_price = list()
        for app in user:
            beauty = app.beautician_id.beautician_id
            rating = Ratingmodel.objects.filter(
                beautician_id=beauty.beautician_id.id)
            rateing = list()
            for rate in rating:
                rateing.append(rate.review)
            shop_image = beauty.beautician_id.shop_image
            service = list()
            shop = {
                'shop_image': '/media/'+str(shop_image),
                'shop_name': beauty.beautician_id.shop_name,
                'location': beauty.beautician_id.city,
                'rating': rate.rating,
                'review': len(rateing),
                'service': service
            }
            services_price.append(shop)
            appo_s = app.appointment_service.all()
            for services in appo_s:
                data = {'service': services.service_name,
                        'price': services.price,
                        }
                service.append(data)
        return JsonResponse({
            'status': 200,
            'message': 'Thank You',
            'data': list(services_price)
        })
