import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import limesurvey
from . import models
from django.contrib.auth.models import User
import random
import string
# Create your views here.
def index(request):
    return HttpResponse("Hello")


def suggestion(request):
    # Get the latest suggestion from limesurvey (simulated)
    new_suggestion = str(limesurvey.get_latest_suggestion())

    # Save the suggestion with a 'pending' status for admin review
    new_item, created = models.Suggestion.objects.get_or_create(
        suggestion=new_suggestion,
        defaults={'status': 'pending'}
    )

    # Fetch all distinct suggestions from the database
    item_set = models.Suggestion.objects.all().distinct()

    # Create a list of all suggestion texts
    item_list = [
        item['suggestion'] 
        for item in item_set.values('suggestion') 
        if item['suggestion'] and item['suggestion'] != 'None'
    ]

    # Return all suggestions as JSON response
    context = {'suggestions': item_list}
    return JsonResponse(context)

@csrf_exempt
def save_rating(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            suggestion_text = data.get("solution")
            rating_value = data.get("rating")
            print(f"{suggestion_text} : {rating_value}")
            # Validate the rating value
            if rating_value is None or not (1 <= int(rating_value) <= 5):
                return JsonResponse({"error": "Invalid rating value. Must be between 1 and 5."}, status=400)

            # Get the participant (current user or a placeholder for testing)
            username = 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            participant = User.objects.create(username=username)

            # Check if the suggestion exists in the database
            try:
                suggestion = models.Suggestion.objects.get(suggestion=suggestion_text)
            except models.Suggestion.DoesNotExist:
                return JsonResponse({"error": "Suggestion not found."}, status=404)

            # Create or update the rating for this participant and suggestion
            rating, created = models.Rating.objects.update_or_create(
                participant=participant,
                suggestion=suggestion,
                defaults={'rating': rating_value}
            )
            print(created)
            response_data = {
                "message": "Rating saved successfully!",
                "created": created  # True if a new rating, False if updated
            }
            return JsonResponse(response_data, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
