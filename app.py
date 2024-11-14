import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

def read_excel_files(folder_path):
    all_data = pd.DataFrame()
    for file in os.listdir(folder_path):
        if file.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file)
            try:
                data = pd.read_excel(file_path, engine='openpyxl')
                print(f"Columns in {file}: {data.columns.tolist()}")
                all_data = pd.concat([all_data, data], ignore_index=True)
            except Exception as e:
                print(f"Error reading {file}: {e}")
    return all_data

@app.route('/', methods=['GET', 'POST'])
def index():
    folder_path = 'data'
    data = read_excel_files(folder_path)
        
    if 'Grand Prix' in data.columns:
        country_names = data['Grand Prix'].unique()
    else:
        country_names = []

    selected_country = None
    prediction_2025 = None
    chart_path = None

    if request.method == 'POST':
        selected_country = request.form.get('country')
        race_results_data = pd.read_excel(os.path.join(folder_path, 'race_results.xlsx'), engine='openpyxl')
        race_results_data.columns = race_results_data.columns.str.strip()
        print("Columns in race_results_data:", race_results_data.columns.tolist())

        if 'Driver Name' in race_results_data.columns and 'Grand Prix' in race_results_data.columns:
            # Lấy số lần thắng của mỗi tay đua cho chặng đua đã chọn
            winners = race_results_data[race_results_data['Grand Prix'] == selected_country]['Driver Name'].value_counts()
            if not winners.empty:
                prediction_2025 = f"Predicted Champion for 2025: {winners.idxmax()}"
                
                # Vẽ biểu đồ
                plt.figure(figsize=(10, 6))
                winners.plot(kind='bar', color='skyblue')
                plt.title(f'Number of Wins in {selected_country}')
                plt.xlabel('Driver Name')
                plt.ylabel('Number of Wins')
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                chart_path = os.path.join('static', 'chart.png')
                plt.savefig(chart_path)
                plt.close()
            else:
                prediction_2025 = "No winners found for the selected Grand Prix."
        else:
            prediction_2025 = "Driver Name or Grand Prix column not found in race results data."

    return render_template('index.html', country_names=country_names, selected_country=selected_country, prediction_2025=prediction_2025, chart_path=chart_path)

if __name__ == '__main__':
    app.run(debug=True)