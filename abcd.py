import os
from flask import Flask, request, jsonify
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

import pandas as pd
import zipfile
import json
from hume import HumeBatchClient
from hume.models.config import FaceConfig, ProsodyConfig

# Initialize Hume client
client = HumeBatchClient("hume_api")
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

# Extract artifacts.zip
zip_file_path = "artifacts.zip"
extract_to_directory = "Output"

os.makedirs(extract_to_directory, exist_ok=True)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to_directory)

print(f"Contents of {zip_file_path} have been extracted to {extract_to_directory}") 

# Load the prosody.csv file
csv_path = os.path.join(extract_to_directory, "url-0-IMG_4648.mp4", "csv", "IMG_4648.mp4", "prosody.csv")
data = pd.read_csv(csv_path)

# Process the data to get top 3 labels for each row
filtered = data.drop(columns=['Id', 'Text', 'SpeakerConfidence'])
print(filtered.head())

def get_top_3_labels(row):
    top_3_labels = row[2:].nlargest(3).index.tolist()
    return top_3_labels

filtered['Top_3_Labels'] = filtered.apply(get_top_3_labels, axis=1)
print("\nDataFrame with top 3 labels of highest values in each row:")
print(filtered)

json_output = []
for index, row in filtered.iterrows():
    row_dict = {
        'BeginTime': row['BeginTime'],
        'EndTime': row['EndTime'],
        'Top_3_Labels': row['Top_3_Labels']
    }
    json_output.append(row_dict)

json_str = json.dumps(json_output, indent=4)
print("\nJSON output:")
print(json_str)

@app.route('/api/emotions', methods=['GET'])
def get_emotions():
    return jsonify(json_str)
# Build the question from the prosody.csv data
answer = " ".join(data['Text'])

print(answer)

app = Flask(__name__)

# Get Groq API key from environment variable
groq_api_key = os.environ.get('GROQ_API_KEY')
model = 'llama3-8b-8192'
groq_chat = ChatGroq(
    groq_api_key=groq_api_key,
    model_name=model
)
question = "Tell me about a time when you had to deal with a difficult customer. How did you handle the situation and what was the outcome?"
system_prompt = f"""
As an interviewer for a software developer position, your task is to evaluate the candidate's response to the following question: 
“{question}” 

Provide a detailed assessment of the candidate's response focusing on their knowledge, articulation, and understanding of Amazon's leadership principles. 
Your feedback should include:
1. **Rating:** A score on a scale of 1-100 based on the quality of the response.
2. **Strengths:** Highlight the strong points of the candidate's answer.
3. **Weaknesses:** Point out any areas where the response was lacking or incorrect.
4. **Suggestions for Improvement:** Offer constructive advice on how the candidate can improve their knowledge or delivery.
5. **Stronger Response Example:** Provide an example of a more comprehensive and accurate response.

Ensure the feedback is structured in a JSON format with the following fields: rating, strengths, weaknesses, suggestions_for_improvement, stronger_response. Do not include any additional text or context, only return the JSON response.
"""

@app.route('/api/chat', methods=['POST'])
def chat():
    user_question = request.json.get('message')
    if not user_question:
        return jsonify({'error': 'No message provided'}), 400

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            HumanMessagePromptTemplate.from_template(f"Candidate response: {user_question}"),
        ]
    )

    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=False,
    )

    response = conversation.predict(human_input=user_question)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
