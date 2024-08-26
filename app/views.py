from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import limesurvey
from . import models
# Create your views here.
def index(request):
    return HttpResponse("Hello")


def suggestion(request):
    new_suggestion = str(limesurvey.get_latest_suggestion())
    new_item, created = models.Item.objects.get_or_create(item_name=new_suggestion)
    item_set = models.Item.objects.all().distinct()
    item_list = [
        item['item_name'] 
        for item in item_set.values('item_name') 
        if item['item_name'] and item['item_name'] != 'None'
    ]
    context = {'suggestions': item_list}
    return JsonResponse(context)