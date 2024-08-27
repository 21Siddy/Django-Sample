import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
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

suggestion_rating_dict = {} #to store the solution and rating as key value pairs
@csrf_exempt
def post_suggestion_ratings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_value = data.get("solution")
            selected_rating = data.get("rating")
            suggestion_rating_dict[f"{selected_value}"] = selected_rating
            response_data = {
                "message": "Rating received successfully!",
            }
            print(suggestion_rating_dict) #temporarily stored in a dictionary - should be saved to Db
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
    return JsonResponse({"error": "Invalid request method"}, status=405)
