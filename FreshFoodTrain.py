from azure.cognitiveservices.vision.customvision import training
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient 
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

cv_endpoint = "https://northeurope.api.cognitive.microsoft.com/"
training_key = "7e166980024f433193e7e27ea6f1baab"
training_images = "FRUIT-16K"

credentials = ApiKeyCredentials(in_headers={"training-key": training_key})
trainer = CustomVisionTrainingClient(endpoint=cv_endpoint, credentials=credentials)

#Wyświetlamy listę wszystkich domenów, żeby zdecydować nad tym, jaki będzie pasował do naszych wymagań   
for domain in trainer.get_domains():   
   print(domain.id, "\t", domain.name)

project = trainer.create_project("FreshFoodDetection - v1","c151d5b5-dd07-472a-acc8-15d29dea8518")

list_of_images = []
dir = os.listdir(training_images)
for tagName in dir:
  tag = trainer.create_tag(project.id, tagName)
  images = os.listdir(os.path.join(training_images,tagName))
  for img in images:
   with open(os.path.join(training_images,tagName,img), "rb") as image_contents:
    list_of_images.append(ImageFileCreateEntry(name=img, contents=image_contents.read(), tag_ids=[tag.id]))