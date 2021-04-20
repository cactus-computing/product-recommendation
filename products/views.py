from rest_framework.views import APIView
from rest_framework.response import Response
import json
from celery.result import AsyncResult
from products.tasks import get_products, get_orders

class GetProductsInfo(APIView):
    def get(self, request, format=None):
        stores = json.loads(request.query_params.get("stores"))
        task_ids = []
        for store in stores:
            task = get_products.delay(store)
            task_ids.append(task.id)
        return Response(task_ids)

class GetOrdersInfo(APIView):
    def get(self, request, format=None):
        stores = json.loads(request.query_params.get('stores'))
        task_ids = []
        for store in stores:
            task = get_orders.delay(store)
            task_ids.append(task.id)
        return Response(task_ids)

class CheckTaskStatus(APIView):
    def get(self, request, format=None):
        statuses = json.loads(request.query_params.get('task_id'))
        status_res = []
        for status in statuses:
            resp = AsyncResult(status).status
            status_res.append(resp)
        return Response(status_res)
