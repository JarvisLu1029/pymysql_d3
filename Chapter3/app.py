from flask import Flask, render_template, jsonify
from chart_data import get_category_chart_data, \
    get_sub_category_chart_data, get_profit_data

app = Flask(__name__)
# __name__ 用來定位目前載入資料夾的位置


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


@app.route('/api/hierarchical-data')
def hierachical_data():
    profit_data = get_profit_data()
    
    return jsonify(profit_data)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True, # 檔案更新網頁也會跟著更新
        port=5000
    )