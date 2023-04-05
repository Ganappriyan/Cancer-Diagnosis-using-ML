from django.shortcuts import render
import requests

def process_image(request): # TODO: Make this function accessible only when user is logged in
    if request.method == 'POST':
        url = 'http://127.0.0.1:8001/process/'
        files = {'file': request.FILES['file']}
        try:
            response = requests.post(url, files=files, timeout=5)
        except (requests.exceptions.ConnectionError):
            print("Connection Error: Image Processor is not running")
            return render(request, 'process_image.html', {'error_message': 'No Response Received from Image Processor'})
        print("Actual Timeout Error")
        return render(request, 'process_image.html', {'response_text': response.text})
    else:
        return render(request, 'process_image.html')
    