from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient 
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry, ImageFileCreateBatch
from msrest.authentication import ApiKeyCredentials
from msrest.exceptions import HttpOperationError

import os, time

endpoint = "https://northeurope.api.cognitive.microsoft.com/"
training_key = "7e166980024f433193e7e27ea6f1baab"
training_images = "FRUIT-16K"

credentials = ApiKeyCredentials(in_headers={"training-key": training_key})
trainer = CustomVisionTrainingClient(endpoint=endpoint, credentials=credentials)

project = trainer.create_project("FreshFoodDetection - v1","c151d5b5-dd07-472a-acc8-15d29dea8518")

list_of_images = []
dir = os.listdir(training_images)
for tagName in dir:
  tag = trainer.create_tag(project.id, tagName)
  images = os.listdir(os.path.join(training_images,tagName))
  for img in images:
   with open(os.path.join(training_images,tagName,img), "rb") as image_contents:
    list_of_images.append(ImageFileCreateEntry(name=img, contents=image_contents.read(), tag_ids=[tag.id]))
    

for i in range(0, len(list_of_images), 64):
    try:
     upload_result = trainer.create_images_from_files(project.id, batch=ImageFileCreateBatch(images = list_of_images[i:i + 64], tag_ids=[tag.id]))
     
    except HttpOperationError as e:
     print(e.response.text)
     exit(-1)
    print("Wait...")
 	
  
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
 	iteration = trainer.get_iteration(project.id, iteration.id)
 	print ("Training status: " + iteration.status)
 	time.sleep(1)


publish_iteration_name = 'FreshFoodDetection'
resource_identifier = 'bd34981d24d540378b74ddab1e87cd33'
trainer.publish_iteration(project.id, iteration.id, publish_iteration_name, resource_identifier)