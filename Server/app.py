from flask import Flask, request, jsonify
from flask_cors import CORS
from data import DataHandler


app = Flask(__name__)
CORS(app)

@app.route('/results', methods=['POST'])
def results():
    data = request.json
    ticker = data.get('ticker')
    start_date = data.get('startDate')
    end_date = data.get('endDate')
    
    DH = DataHandler(ticker, start_date, end_date)
    summary = DH.data_characteristics()
    plot_path = DH.performance_analysis()
    
    
    response = {
        
        'data': {
            'data_statistics' : summary,
     
            'plot_path' : plot_path
        }
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
