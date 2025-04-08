from flask import Flask, request, jsonify, render_template
# Import your PetAdoptionAssistant class
from main import PetAdoptionAssistant

app = Flask(__name__)
assistant = PetAdoptionAssistant()
assistant.initialize_conversation()

@app.route('/')
def index():
    return render_template('index.html')  # Serve your HTML

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = assistant.generate_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)