# backend.py
import asyncio
import base64
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from hume import HumeStreamClient
from hume.models.config import FaceConfig, ProsodyConfig

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

hume_client = HumeStreamClient("Hume_API")
configs = [FaceConfig(), ProsodyConfig()]

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    file.save(file.filename)
    return jsonify({'success': 'File uploaded successfully', 'filename': file.filename})

@socketio.on('stream_video')
def handle_stream_video(data):
    print('Streaming video')
    filename = data['filename']
    async def process_video():
        async with hume_client.connect(configs) as socket:
            async with open(filename, 'rb') as f:
                while chunk := f.read(1024 * 1024):  # Read video in chunks
                    result = await socket.send_bytes(base64.b64encode(chunk))
                    await socketio.emit('response', result)
    asyncio.run(process_video())

@socketio.on('stream_frame')
def handle_stream_frame(data):
    print('Received a frame')
    frame_data = data['frame']
    frame_bytes = base64.b64decode(frame_data.split(",")[1])
    encoded_frame = base64.b64encode(frame_bytes).decode('utf-8')
    async def process_frame():
        async with hume_client.connect(configs) as socket:
            result = await socket.send_bytes(encoded_frame.encode('utf-8'))
            await socketio.emit('response', result)
    asyncio.run(process_frame())

if __name__ == '__main__':
    socketio.run(app, debug=True)
