# Ten dokument opisuje poszczeglne kroki do realizacji projektu "Fresh Food Detection" za pomocą serwisów Microsoft Azure 

Cała implementacja jest napisana w języku Python (ver. 3.8.8) 

Welcome to this first article in the AI for Developer series, in this series of articles I will share tips and tricks around Azure AI with you. My name is Henk Boelman, a Cloud Advocate at Microsoft based in the Netherlands, focusing on AI for developers.

In this first article I want to share with you how you can create a classification model using the Custom Vision service with the Python SDK.

### Configuracja serwisu Custom Vision AI za pomocą Azure-CLI (polecenia są wpisywane w terminalu)
1. Na początku instalujemy Azure Client poleceniem: 
```
pip install azure-cli
```
2. Tworzymy grupę zasobów:
```
az group create --name FreshFoodDetection --location northeurope
```
3. Tworzymy model testowy oraz prognozowy:
```
az cognitiveservices account create --name FreshFoodDetection-Prediction --resource-group FreshFoodDetection --kind CustomVision.Prediction --sku S0 --location northeurope

az cognitiveservices account create --name FreshFoodDetection-Prediction --resource-group FreshFoodDetection --kind CustomVision.Prediction --sku S0 --location northeurope
```

### Trening modelu
1. Na początku mamy zainstalować (w linii poleceń) Custom Vision Service Python SDK, żeby móc konfigurować modeli bez dostępu do interfejsu graficznego
```
pip install azure-cognitiveservices-vision-customvision
```
2. Dodajemy niezbędne pakiety, czyli CustomVisionTrainingClient, ImageFileCreateEntry, ImageFileCreateEntry, ApiKeyCredentials oraz HttpOperationError:
```
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient 
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, ImageFileCreateBatch
from msrest.authentication import ApiKeyCredentials
from msrest.exceptions import HttpOperationError
```
3. Pobiramy dane odnośnie zbioru zasobów treningowych:
```
az cognitiveservices account show --name FreshFoodDetection-Training --resource-group FreshFoodDetection
```
3. Tworzymy zmienne, do których zapisujemy dane o punkcie docelowym, kluczu modelu treningowego oraz dataset ze zdjęciami produktów: 
```
endpoint = "https://northeurope.api.cognitive.microsoft.com/"
training_key = "7e166980024f433193e7e27ea6f1baab"
training_images = "FRUIT-16K"
```
4. Tworzymy Training Client:
```
credentials = ApiKeyCredentials(in_headers={"training-key": training_key})
trainer = CustomVisionTrainingClient(endpoint=endpoint, credentials=credentials)
```
5. Wyświetlamy listę wszystkich domenów, żeby zdecydować nad tym, jaki będzie pasował do naszych wymagań:
```
for domain in trainer.get_domains():   
   print(domain.id, "\t", domain.name)
```
6. Na podstawie uzyskanych wyników tworzymy projekt:
```
project = trainer.create_project("FreshFoodDetection - v1","c151d5b5-dd07-472a-acc8-15d29dea8518")
```
7. Tagujemy wszystkie obrazki według kategorii(nazw folderów, w których są zdjęcia przydzielone):
```
list_of_images = []
dir = os.listdir(training_images)
for tagName in dir:
  tag = trainer.create_tag(project.id, tagName)
  images = os.listdir(os.path.join(training_images,tagName))
  for img in images:
   with open(os.path.join(training_images,tagName,img), "rb") as image_contents:
    list_of_images.append(ImageFileCreateEntry(name=img, contents=image_contents.read(), tag_ids=[tag.id]))
```
8. Wysyłamy zdjęca do Azure Custom Vision Service grupowo (po 64 zdjęcia na zbiór):
```
for i in range(0, len(list_of_images), 64):
    try:
     upload_result = trainer.create_images_from_files(project.id, batch=ImageFileCreateBatch(images = list_of_images[i:i + 64], tag_ids=[tag.id]))
     
    except HttpOperationError as e:
     print(e.response.text)
     exit(-1)
    print("Wait...")
```
