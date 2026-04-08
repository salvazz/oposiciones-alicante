from flask import Flask, render_template, jsonify
from oposiciones_scraper import get_oposiciones_data
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """Home page with oposiciones list"""
    data = get_oposiciones_data()
    return render_template('index.html', oposiciones=data['oposiciones'], total=data['total'])

@app.route('/api/oposiciones')
def get_oposiciones_api():
    """API endpoint for oposiciones data"""
    data = get_oposiciones_data()
    return jsonify(data)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)