from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': '请输入网址'}), 400

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        return jsonify({'error': f'请求失败: {e}'}), 500

    soup = BeautifulSoup(r.text, 'html.parser')

    # 提取文本
    texts = ' '.join(soup.stripped_strings)

    # 提取图片
    images = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and src.startswith(('http', 'https')):
            images.append(src)

    return jsonify({'text': texts, 'images': images})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
