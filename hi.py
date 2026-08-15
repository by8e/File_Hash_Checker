#contains legacy ver too
from flask import Flask, request, jsonify, send_from_directory
import hashlib
hi = Flask(__name__)
algos = {
    'md5(legacy)': hashlib.md5,
    'sha1(legacy)': hashlib.sha1,
    'sha256': hashlib.sha256,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512,
}
@hi.route('/')
def i():
    return send_from_directory('.', 'index.html')
@hi.route('/hash', methods=['POST'])
def hash_file():
    uploaded = request.files.get('file')
    if not uploaded:
        return jsonify(error='no file uploaded'), 400
    algo = request.form.get('algo', 'sha256')
    hash_func = algos.get(algo)
    if not hash_func:
        return jsonify(error='unsupported algorithm'), 400
    h = hash_func()
    chunk = uploaded.read(8192)
    while chunk:
        h.update(chunk)
        chunk = uploaded.read(8192)
    return jsonify(hash=h.hexdigest(), algo=algo, filename=uploaded.filename)
if __name__ == '__main__':
    hi.run(debug=True)
