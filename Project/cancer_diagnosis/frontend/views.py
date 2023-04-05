from django.shortcuts import render
import requests

def home(request):
    return render(request, 'home.html')

def process_image(request):
    if request.method == 'POST':
        url = 'http://127.0.0.1:8001/process/'
        files = {'file': request.FILES['file']}
        try:
            response = requests.post(url, files=files, timeout=5)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return render(request, 'process_image.html', {'error_message': 'No Response Received from Image Processor'})
        return render(request, 'process_image.html', {'response_text': response.text})
    else:
        return render(request, 'process_image.html')
