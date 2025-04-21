from flask import Blueprint, request, jsonify
from .services.faceVerify import compare_faces

main = Blueprint('main', __name__)

@main.route('/verify', methods=['POST'])
def verify_route():
    if 'img1' not in request.files or 'img2' not in request.files:
        return jsonify({'error': 'Missing img1 or img2 in form data'}), 400

    img1 = request.files['img1']
    img2 = request.files['img2']

    if img1.filename == '' or img2.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        result = compare_faces(img1, img2)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500