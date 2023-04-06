from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_image_file_extension
from django.core.exceptions import ValidationError
from image_processor.models import JsonResponse
import json

@login_required
def process_image(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return render(request, 'image_processor/process_image.html', {'error_message': 'No file was uploaded'})
        files = {'file': request.FILES['file']}
        try:
            validate_image_file_extension(files['file'])
        except ValidationError:
            return render(request, 'image_processor/process_image.html', {'error_message': 'The uploaded file is not an image.'})
        files = {'file': request.FILES['file']}
        try:
            url = 'http://127.0.0.1:8001/process/'
            response = requests.post(url, files=files, timeout=5)
        except (requests.exceptions.ConnectionError):
            return render(request, 'image_processor/process_image.html', {'error_message': 'No Response Received from Image Processor'})
        
        dict_obj = json.loads(response.json())
        print(type(dict_obj), dict_obj)
        classification = dict_obj['classification']
        print(type(classification), classification)
        grading = dict_obj['grading']
        
        response_text = {'grading': grading['maxlabel']}
        if response_text['grading'] != 'normal':
            response_text['classification'] = classification['maxlabel']
        JsonResponse.objects.create(user=request.user, response_text=response_text)
        return render(request, 'image_processor/process_image.html', response_text)
    else:
        return render(request, 'image_processor/process_image.html')

@login_required
def history(request):
    json_responses = JsonResponse.objects.filter(user=request.user).order_by('-created_at')
    response_as_array = []
    for json_response in json_responses:
        dict_obj = json.loads(json_response.response_text.replace("'", '"'))
        dict_obj['created_at'] = json_response.created_at
        print(type(dict_obj), dict_obj)
        response_as_array.append(dict_obj)
    print(type(response_as_array), response_as_array)
    return render(request, 'image_processor/history.html', {'json_responses': response_as_array})

@login_required
def clear_history(request):
    JsonResponse.objects.filter(user=request.user).delete()
    return redirect('history')
