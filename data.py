import pandas as pd
import json

data = pd.read_csv(r"Output\url-0-IMG_4648.mp4\csv\IMG_4648.mp4\prosody.csv")

text = ""
for i, row in data.iterrows():
    text += row['Text'] + " "
    #print(f"Row {i}: {text}")

print(text)

filtered = data.drop(columns=['Id', 'Text', 'SpeakerConfidence'])
print(filtered.head())

# Function to find the top 3 labels with the highest values in each row
def get_top_3_labels(row):
    # Exclude 'Start Time' columns and find the top 3 columns with the highest values
    top_3_labels = row[2:].nlargest(3).index.tolist()
    return top_3_labels

# Apply the function to each row
filtered['Top_3_Labels'] = filtered.apply(get_top_3_labels, axis=1)
print("\nDataFrame with top 3 labels of highest values in each row:")
print(filtered)

# Create a list of dictionaries for the JSON output
json_output = []
for index, row in filtered.iterrows():
    row_dict = {
        'BeginTime': row['BeginTime'],
        'EndTime': row['EndTime']
        ,
        'Top_3_Labels': row['Top_3_Labels']
    }
    json_output.append(row_dict)

# Convert the list of dictionaries to a JSON string
json_str = json.dumps(json_output, indent=4)
print("\nJSON output:")
print(json_str)

