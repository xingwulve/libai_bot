# app.py
from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Coze API 配置
COZE_API_URL = 'https://api.coze.cn/open_api/v2/chat'
COZE_HEADERS = {
    'Authorization': 'Bearer pat_6g9Xfd0T7oddD5yDazzZkhTu8eqMLvyDGRZS6Neu2iIIjc5THG5FhxUpSJsnrpv7',
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
    'Accept': '*/*'
}
BOT_ID = '7482561611249877028'
USER_ID = 'web_user'  # 网页用户唯一标识


def get_coze_response(query):
    data = {
        'bot_id': BOT_ID,
        'user': USER_ID,
        'query': query,
        'stream': False
    }

    try:
        response = requests.post(
            COZE_API_URL,
            headers=COZE_HEADERS,
            json=data,
            timeout=10
        )

        if response.status_code == 200:
            return response.json().get('result', '')
        else:
            return f"Coze API Error: {response.status_code}"
    except Exception as e:
        return f"Request Error: {str(e)}"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({'error': 'Empty message'}), 400

    bot_response = get_coze_response(user_input)
    return jsonify({'message': bot_response})


if __name__ == '__main__':
    app.run(debug=True)