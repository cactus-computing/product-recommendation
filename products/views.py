from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from datetime import timedelta
import json
from celery.result import AsyncResult
from products.tasks import get_products, get_orders, get_customers, get_info

class GetProductsInfo(APIView):
    def get(self, request, format=None):
        stores = json.loads(request.query_params.get("stores"))
        task_ids = []
        for store in stores:
            task = get_products.delay(store)
            task_ids.append({
                'method': "get_products",
                'Start time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Company':store,
                'Task_id': task.id
            })
        return Response(task_ids)

class GetOrdersInfo(APIView):
    def get(self, request, format=None):
        stores = json.loads(request.query_params.get('stores'))
        task_ids = []
        for store in stores:
            task = get_orders.delay(store)
            task_ids.append({
                'method': "get_orders",
                'Start time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Company':store,
                'Task_id': task.id
            })
        return Response(task_ids)

class GetCustomersInfo(APIView):
    def get(self, request, format=None):
        stores = json.loads(request.query_params.get('stores'))
        task_ids = []
        for store in stores:
            task = get_customers.delay(store)
            task_ids.append({
                'method': "get_customers",
                'Start time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Company':store,
                'Task_id': task.id
            })
        return Response(task_ids)

class GetAllInfo(APIView):
    def get(self, request, format=None):
        stores = json.loads(request.query_params.get('stores'))
        task_ids = []
        for store in stores:
            task = get_info.delay(store)
            task_ids.append({
                'method': "get_all_info",
                'Start time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Company':store,
                'Task_id': task.id
            })
        return Response(task_ids)


class CheckTaskStatus(APIView):
    def get(self, request, format=None):
        statuses = json.loads(request.query_params.get('task_id'))
        status_res = []
        for status in statuses:
            resp = AsyncResult(status['Task_id']).status
            status_res.append({
                'method': status['method'],
                'Start time': status['Start time'],
                'Company': status['Company'],
                'Status': resp
            })
        return Response(status_res)
