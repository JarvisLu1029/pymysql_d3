from flask import Flask, render_template, jsonify
from chart_data import get_category_chart_data, \
    get_sub_category_chart_data, get_quantity_data, \
    get_products_and_order_details

# __name__ 用來定位目前載入資料夾的位置
app = Flask(__name__)


@app.route('/say_hello')  # Python 內建的裝飾詞，讓Flask監聽此URL 並return 返還結果
def hello_world():
    return 'Hello, World!'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/category_pie')
def category_pie():
    category_pie_data = get_category_chart_data()

    return jsonify(category_pie_data)


@app.route('/api/sub_category_pie/<string:category>')
def sub_category_pie(category):
    sub_category_pie_data = get_sub_category_chart_data(category)

    return jsonify(sub_category_pie_data)


@app.route('/api/hierarchical_data')
def hierachical_data():
    quantity_data = get_quantity_data()
    
    return jsonify(quantity_data)


@app.route('/api/products_and_order_details')
def products_and_order_details():
    products_and_order_details_data = get_products_and_order_details()

    return jsonify(products_and_order_details_data)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True, # 檔案更新網頁也會跟著更新
        port=5000
    )