from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import limesurvey
from . import models
# Create your views here.
def index(request):
    return HttpResponse("Hello")


def suggestion(request):
    new_suggestion = str(limesurvey.get_latest_suggestion())
    new_item, created = models.Suggestion.objects.get_or_create(suggestion=new_suggestion)
    item_set = models.Suggestion.objects.all().distinct()
    item_list = [
        item['suggestion'] 
        for item in item_set.values('suggestion') 
        if item['suggestion'] and item['suggestion'] != 'None'
    ]
    context = {'suggestions': item_list}
    return JsonResponse(context)
