
# app.py
from flask import Flask, jsonify, render_template
from scraper import fetch_trending_data
from bson.json_util import dumps

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_trends')
def fetch_trends():
    data = fetch_trending_data()
    return jsonify({
        "trends": data["trends"],
        "timestamp": data["timestamp"],
        "proxy": data["proxy"],
        "mongodb_data": dumps(data)
    })

if __name__ == '__main__':
    app.run(debug=True)



# # app.py
# from flask import Flask, jsonify, render_template
# from scraper import scrape_with_proxy, store_data

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/fetch_trends')
# def fetch_trends():
#     trends = scrape_with_proxy()
#     store_data(trends)
#     return jsonify({"trends": trends})

# if __name__ == '__main__':
#     app.run(debug=True)
