from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def hello_get(request):
    return JsonResponse({'msg': 'hello, get'})


@require_http_methods(['POST'])
def hello_post(request):
    return JsonResponse({'msg': 'hello, post'})
