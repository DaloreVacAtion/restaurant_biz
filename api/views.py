import datetime

from django.db.models import Count, Q, Sum, Avg
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, views, status
from rest_framework import mixins, generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from api.exceptions import BadRequest
from api.serializers import RestaurantListSerializer, AddBookingSerializer
from booking.models import Restaurant, Table


def get_allowed_time(time):
    """
    Получает на вход строку времени в виде "%H,%m", возвращает два объекта datetime.time:
    время брони, время окончания брони.
    :param time:
    :return:
    """
    visit_time = []
    for time in time.split(','):
        visit_time.append(int(time))

    allowed_time = datetime.time(visit_time[0], visit_time[1])
    expired_time = datetime.time(visit_time[0] + 2, visit_time[1])
    return allowed_time, expired_time


class RestaurantViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = RestaurantListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['avg_time', 'avg_cost']

    def get_queryset(self):
        allowed_peoples = self.request.query_params.get('peoples_count', None)  # кол-во гостей
        time = self.request.query_params.get('time', None)  # время брони

        if time is None or allowed_peoples is None:
            raise BadRequest(detail="missing required param ('peoples_count' or 'time')")

        allowed_time, _ = get_allowed_time(time)

        if allowed_time < datetime.time(9, 00) or allowed_time > datetime.time(21, 00):
            raise BadRequest(detail="The allowed booking time between 9 and 21")

        if int(allowed_peoples) > 20 or int(allowed_peoples) < 1:
            raise BadRequest(detail="Visitors amount must be less or equal 20 (1 minimum)")
        # получаем список столиков, у которых нет брони на полученный промежуток времени
        # чтобы потом по ним "вытащить" доступные рестораны
        tables = Table.objects.exclude(Q(booking__visit_time__lt=allowed_time) &
                                       Q(booking__expired_time__gt=allowed_time))
        # получаем список ресторанов с доступными столиками, а также получаем количество свободных мест, среднюю
        # стоимость заказа и количество свободных столиков через annotate, отфильтруем по количеству посетителей
        return Restaurant.objects.filter(tables__in=tables).annotate(free_tables_count=Count('tables'),
                                                                     seats=Sum('tables__capacity'),
                                                                     avg_cost=Avg('receipts__amount')).filter(
            Q(seats__gte=self.request.query_params['peoples_count'])
        )


class AddBookingView(views.APIView):

    def get_tables_for_booking(self, visitors, tables, tables_ids):
        """
        На вход подается количество посетителей, вместимость столиков и id столиков. Цикл работает до тех пор,
        пока не подберет столики пользователю. Для начала он пытается найти столик абсолютно подходящий по
        размерам, если такового нет, он находит максимально близкое значение к кол-ву посетителей, затем
        отнимает это значение от кол-ва посетителей, если разница отрицательная или равна 0 (пр. посетителей 7,
        а столик на 8 человек), заканчивает цикл и выводит ID столиков, отобранных для брони.
        :param visitors:
        :param tables:
        :param tables_ids:
        :return:
        """
        _break = False
        tables_id = []
        while visitors > 0:
            for table_count in tables:
                if table_count == visitors:
                    tables_id.append(tables_ids[tables.index(table_count)])
                    _break = True
                    break
            if _break:
                break
            min_l = min(tables, key=lambda x: abs(x - visitors))  # получаем число с минимальной разницей с искомым
            index_min_l = tables.index(min_l)  # Индекс найденного значения
            visitors -= min_l
            tables_id.append(tables_ids[index_min_l])
            tables.remove(min_l)
            del tables_ids[index_min_l]
        return tables_id

    def post(self, request):
        restaurant_id = self.request.data.get('restaurant_id', None)
        allowed_peoples = self.request.data.get('peoples_count', None)
        time = self.request.data.get('visit_time', None)
        user_phone = self.request.data.get('user', None)

        if restaurant_id is None or allowed_peoples is None or time is None or user_phone is None:
            raise BadRequest(detail='missing one or more required field (restaurant_id, peoples_count, time, phone)')

        allowed_time, expired_time = get_allowed_time(time)

        tables = Table.objects.filter(restaurant_id=restaurant_id). \
            exclude(Q(booking__visit_time__lt=allowed_time) &
                    Q(booking__expired_time__gt=allowed_time)).values_list('id', 'capacity')

        ids = []
        counts = []

        for table in tables:
            ids.append(table[0])
            counts.append(table[1])

        t = self.get_tables_for_booking(allowed_peoples, counts, ids)
        data = {
            'tables': t,
            'visit_time': allowed_time,
            'expired_time': expired_time,
            'user': user_phone
        }
        serializer = AddBookingSerializer(data=data, context={'expired_time': expired_time})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
