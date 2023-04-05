from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required
from image_processor.models import JsonResponse

@login_required
def process_image(request): # TODO: Make this function accessible only when user is logged in
    if request.method == 'POST':
        url = 'http://127.0.0.1:8001/process/'
        files = {'file': request.FILES['file']}
        try:
            response = requests.post(url, files=files, timeout=5)
        except (requests.exceptions.ConnectionError):
            print("Connection Error: Image Processor is not running")
            return render(request, 'image_processor/process_image.html', {'error_message': 'No Response Received from Image Processor'})
        # create a new JsonResponse object and save it to the database
        JsonResponse.objects.create(user=request.user, response_text=response.text)
        
        return render(request, 'image_processor/process_image.html', {'response_text': response.text})
    else:
        return render(request, 'image_processor/process_image.html')

@login_required
def history(request):
    # retrieve the user's previous JSON responses from the database
    json_responses = JsonResponse.objects.filter(user=request.user).order_by('-created_at')
    
    # render the history template with the JSON responses
    return render(request, 'image_processor/history.html', {'json_responses': json_responses})

    