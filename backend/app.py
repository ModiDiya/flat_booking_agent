from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Booking AI Agent API', 
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/api/booking', methods=['GET'])
def get_booking():
    return jsonify({'message': 'Booking endpoint'})

@app.route('/api/booking', methods=['POST'])
def create_booking():
    data = request.get_json()
    return jsonify({'message': 'Booking created', 'data': data})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
