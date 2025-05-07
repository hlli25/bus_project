from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get', methods=['POST'])
def get_bot_response():
    user_input = request.form['msg']
    return jsonify({"reply": f"You said: {user_input}"})

if __name__ == "__main__":
    app.run(debug=True)
