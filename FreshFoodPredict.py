from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

endpoint = "https://northeurope.api.cognitive.microsoft.com/"
prediction_key = "bd34981d24d540378b74ddab1e87cd33"

publish_iteration_name = 'FreshFoodDetection'
project_id = "b5716ef9-aeba-4cfa-8d1d-46ae23081e59" 

image_url = "https://image.shutterstock.com/image-photo/banana-bananas-isolated-on-white-260nw-594559439.jpg"

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)
predictor = CustomVisionPredictionClient(prediction_key, endpoint=endpoint)

results = predictor.classify_image_url(project_id,publish_iteration_name,url=image_url)

for prediction in results.predictions:
  print("\t" + prediction.tag_name + ": {0:.2f}%".format(prediction.probability * 100))