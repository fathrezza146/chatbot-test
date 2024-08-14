from flask import Flask
from flask_socketio import SocketIO, send
from transformers import pipeline, Conversation
import torch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
pipe_device = 0 if torch.cuda.is_available() else -1

# Load Hugging Face pipeline for text generation
chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill", device=pipe_device)

@app.route('/')
def index():
    return "SocketIO Chatbot Server with Hugging Face"

@socketio.on('message')
def handle_message(msg):
    print('Received message: ' + msg)

    conversation = Conversation(msg)

    # Generate a response using the Hugging Face model
    response = chatbot(conversation)
    print(response)
    reply = response.generated_responses[-1]
    send(reply, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
