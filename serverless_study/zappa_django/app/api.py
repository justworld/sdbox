from django.http import JsonResponse

def index(request):
    return JsonResponse({'result': False, 'msg': '未通过数据验证'})