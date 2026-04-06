from flask import Flask, jsonify

app = Flask(__name__)

# Sample data for oposiciones de Alicante
data = {
    'oposiciones': [
        {'id': 1, 'nombre': 'Oposición Técnico/a de Administración General', 'fecha': '2022-05-15'},
        {'id': 2, 'nombre': 'Oposición Profesor/a de Educación Secundaria', 'fecha': '2022-06-20'},
        {'id': 3, 'nombre': 'Oposición Policía Local', 'fecha': '2022-07-10'}
    ]
}

@app.route('/oposiciones', methods=['GET'])
def get_oposiciones():
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)