import pandas as pd
import zipfile
import os
from hume import HumeBatchClient
from hume.models.config import FaceConfig
from hume.models.config import ProsodyConfig

client = HumeBatchClient("UZNPXh6KYRr0GHYpd4IPlOsEWGcBlIvGtYXicgwXiPAmmPGv")
urls = ["https://jbdehsbckejkbdkhwx.s3.amazonaws.com/IMG_4648.mp4"]
configs = [FaceConfig(identify_faces=True), ProsodyConfig()]
job = client.submit_job(urls, configs)

print(job)
print("Running...")

job.await_complete()
job.download_predictions("predictions.json")
print("Predictions downloaded to predictions.json")

job.download_artifacts("artifacts.zip")
print("Artifacts downloaded to artifacts.zip")

zip_file_path = r"C:\Users\sahaj\Desktop\Practice\hack\artifacts.zip"
extract_to_directory = r"C:\Users\sahaj\Desktop\Practice\hack\Output"

os.makedirs(extract_to_directory, exist_ok=True)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Extract all the contents
    zip_ref.extractall(extract_to_directory)

print(f"Contents of {zip_file_path} have been extracted to {extract_to_directory}") 

data = pd.read_csv(r"Output\url-0-IMG_4648.mp4\csv\IMG_4648.mp4\prosody.csv")

text = ""
for i, row in data.iterrows():
    text += row['Text'] + " "
    #print(f"Row {i}: {text}")

print(text)


