from hume import HumeBatchClient
from hume.models.config import FaceConfig
from hume.models.config import ProsodyConfig

client = HumeBatchClient("Hume_API")
urls=['https://jbdehsbckejkbdkhwx.s3.amazonaws.com/IMG_4647.mp4']
configs = [FaceConfig(identify_faces=True), ProsodyConfig()]
job = client.submit_job(urls, configs)

print(job)
print("Running...")

job.await_complete()
job.download_predictions("predictions.json")
print("Predictions downloaded to predictions.json")

job.download_artifacts("artifacts.zip")
print("Artifacts downloaded to artifacts.zip")