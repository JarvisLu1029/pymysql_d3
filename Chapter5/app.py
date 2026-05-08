from flask import Flask, render_template, jsonify, request
from sql_utils import WebScrapingDB

app = Flask(__name__)

# --- Flask 路由 ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data/store_ratio')
def store_ratio_api():
    keyword = request.args.get('keyword', None)
    data = WebScrapingDB().get_store_products_count(keyword)
    return jsonify(data)

@app.route('/api/data/price_range')
def price_range_api():
    keyword = request.args.get('keyword', None)
    data = WebScrapingDB().get_price_range_products_count(keyword)
    return jsonify(data)

@app.route('/api/data/scatter')
def scatter_api():
    keyword = request.args.get('keyword', None)
    data = WebScrapingDB().get_price_store_scatter_data(keyword)
    return jsonify(data)

if __name__ == '__main__':
    # 運行前請先安裝 Flask: pip install Flask
    app.run(debug=True)