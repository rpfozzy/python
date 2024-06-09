from flask import Flask, request, jsonify
from threading import Thread
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data['code']
    
    def run_in_background(code):
        process = subprocess.Popen(['python3', '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode() + stderr.decode()

    thread = Thread(target=run_in_background, args=(code,))
    thread.start()
    thread.join()
    output = run_in_background(code)

    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(debug=True)
