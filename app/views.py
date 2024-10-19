import json
from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from . import limesurvey
from . import models
from django.contrib.auth.models import User

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
    item_set_approved = models.Suggestion.objects.filter(status='approved')
    item_set_all = models.Suggestion.objects.all()

    # Create a list of all suggestion texts
    item_list = [
        item['suggestion'] 
        for item in item_set_approved.values('suggestion')
    ]
    
    item_list_all = [
        item['suggestion'] 
        for item in item_set_all.values('suggestion')
    ]

    # Use atomic transaction to ensure unique username generation
    with transaction.atomic():
        # Fetch the latest user with a username starting with 'lsuser$'
        last_user = User.objects.filter(username__startswith='lsuser$').order_by('-username').first()

        if last_user:
            # Extract the number from the username and increment
            last_number = int(last_user.username.split('$')[-1])
            new_number = last_number + 1
        else:
            # Start from lsuser$1 if no such users exist
            new_number = 1

        # Generate a new username
        new_username = f'lsuser${new_number}'

    # Return all suggestions as JSON response along with the new username
    context = {
        'suggestions': item_list, 
        'suggestions_all': item_list_all,
        'username': new_username  # Send this username to the front end
    }
    print(item_list_all)
    return JsonResponse(context)


@csrf_exempt
@transaction.atomic  # Ensures atomicity to prevent race conditions
def save_rating(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)
            suggestion_text = data.get("solution")
            rating_value = data.get("rating")
            username = data.get("username")  # Get the username from the frontend

            # Validate the rating value
            if rating_value is None or not (1 <= int(rating_value) <= 5):
                return JsonResponse({"error": "Invalid rating value. Must be between 1 and 5."}, status=400)

            # Ensure the username is provided
            if not username:
                return JsonResponse({"error": "Username is required."}, status=400)

            # Get or create the participant (user) with the provided username
            participant, created = User.objects.get_or_create(username=username)
            if created:
                # Set a random password if this is a new user
                random_password = get_random_string(length=8)
                participant.set_password(random_password)
                participant.save()

            # Check if the suggestion exists
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

            response_data = {
                "message": "Rating saved successfully!",
                "created": created  # True if a new rating, False if updated
            }
            return JsonResponse(response_data, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
