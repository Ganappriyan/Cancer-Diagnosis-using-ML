import requests

def download_file_from_google_drive(url, destination):
    # URL = "https://docs.google.com/uc?export=download"
    URL = url

    session = requests.Session()

    # response = session.get(URL, params = { 'id' : id }, stream = True)
    response = session.get(URL, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


# file_id = '1L-5EPgPTJzq73jEe5L28JAl_1SUioYjJ'
url1 = "https://www.googleapis.com/drive/v3/files/1L-5EPgPTJzq73jEe5L28JAl_1SUioYjJ?alt=media&key=AIzaSyCusL2jXa17co43qqGhQdlZie_XmRFe-SQ"
url2 = "https://www.googleapis.com/drive/v3/files/1I1smsK2SyjNIgKOgLvijCuZDOzILCD7U?alt=media&key=AIzaSyCusL2jXa17co43qqGhQdlZie_XmRFe-SQ"
destination1 = 'model/classification/simple_noarg.h5'
destination2 = 'model/grade/simple_noarg.h5'
# download_file_from_google_drive(url1, destination1)
download_file_from_google_drive(url2, destination2)