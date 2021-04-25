from rest_framework.views import APIView
from rest_framework.response import Response
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
                'method': status['methos'],
                'Company': status['Company'],
                'Status': resp
            })
        return Response(status_res)
