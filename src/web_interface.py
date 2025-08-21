from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# TODO: Add HTML template and routes in next commit

if __name__ == '__main__':
    print("🌐 Starting Web Interface...")
    print("Web interface will be available at: http://localhost:8081")
    print("Make sure your ML API is running at: http://localhost:5000")
    app.run(host='0.0.0.0', port=8081, debug=True)
