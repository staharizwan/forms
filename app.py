from flask import *
import pandas as pd
import openpyxl
import os

app = Flask(__name__)
EXCEL_FILE = 'user_data.xlsx'

@app.route('/', methods=['GET'])
def index():
    return render_template('dataCollector.html')

@app.route('/submit_data', methods=['POST'])
def submit_data():
    try:
        name  = request.form.get('name')
        email = request.form.get('email')
        age   = request.form.get('age')
        city  = request.form.get('city')
        
        data = {'Name': [name], 'Email':[email], 'Age': [age], 'City':[city]}
        df   = pd.DataFrame(data)    
        print(f'the dataframe is {df}')
        
        try:
            existing_pd = pd.read_excel(EXCEL_FILE, sheet_name='Sheet1')
            
            if list(df.columns) == list(existing_pd.columns):
                updated_df = pd.concat([existing_pd, df], ignore_index=True)
                updated_df.to_excel(EXCEL_FILE, index = False)
            else: 
                return jsonify({'error': 'Data columns do not match Excel file columns.'}), 400
        except FileNotFoundError:
            df.to_excel(EXCEL_FILE, index=False)

        return jsonify({'message': 'Data submission was successful !'})    
    
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug = True)