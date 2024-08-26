from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import limesurvey
# Create your views here.
def index(request):
    return HttpResponse("Hello")


def suggestion(request):
    new_suggestion = str(limesurvey.get_latest_suggestion())
    print(new_suggestion)
    context = {'suggestions': new_suggestion}
    return JsonResponse(context)