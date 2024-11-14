import pandas as pd
from sklearn.model_selection import train_test_split

# Đọc dữ liệu từ các file   
race_results = pd.read_excel('data/race_results.xlsx')
drivers = pd.read_excel('data/driver.xlsx')
circuits = pd.read_excel('data/circuits.xlsx')
fastest_pit_stops = pd.read_excel('data/fastest_pit_stop.xlsx')
fastest_laps = pd.read_excel('data/fastest_lap.xlsx')

# Hàm chuẩn hóa tên
def clean_names(df, name_col):
    df[name_col] = df[name_col].str.strip().str.replace(' ', '').str.upper()
    return df

# Chuẩn hóa tên driver, đội đua và Grand Prix
race_results = clean_names(race_results, 'Driver Name')
race_results = clean_names(race_results, 'Team')
race_results = clean_names(race_results, 'Grand Prix')

drivers = clean_names(drivers, 'Driver Name')
drivers = clean_names(drivers, 'Team')

circuits = clean_names(circuits, 'Grand Prix')

# Kiểm tra dữ liệu trong các DataFrame
print("Race Results DataFrame:")
print(race_results.head())
print("Drivers DataFrame:")
print(drivers.head())
print("Circuits DataFrame:")
print(circuits.head())

# Kết hợp dữ liệu
merged_data = pd.merge(race_results, drivers, on=['Driver Name', 'Team'], suffixes=('_driver', '_race_results'))
print("After merging race_results and drivers:", merged_data.shape)

merged_data = pd.merge(merged_data, circuits, left_on='Grand Prix', right_on='Grand Prix', how='left')
print("After merging with circuits:", merged_data.shape)

merged_data = pd.merge(merged_data, fastest_pit_stops, on=['Grand Prix', 'Driver Name', 'Team'], how='left')
print("After merging with fastest_pit_stops:", merged_data.shape)

merged_data = pd.merge(merged_data, fastest_laps, on=['Grand Prix', 'Driver Name', 'Team'], how='left')
print("After merging with fastest_laps:", merged_data.shape)

# In ra các cột trong merged_data để kiểm tra
print("Columns in merged_data:", merged_data.columns.tolist())
print("Number of rows in merged_data:", merged_data.shape[0])

# Chọn các cột cần thiết cho mô hình
if merged_data.shape[0] > 0:
    features = merged_data[['Driver Name', 'Team', 'Grand Prix']]
    target = merged_data['Driver Name']  # Giả sử chúng ta có cột này trong dữ liệu

    # Chuyển đổi các cột phân loại thành biến số
    features = pd.get_dummies(features, columns=['Driver Name', 'Team', 'Grand Prix'], drop_first=True)

    # Kiểm tra kích thước của features
    print("Features shape:", features.shape)

    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra
    if features.shape[0] > 0:
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        print("Training and testing data split successfully.")
    else:
        print("Features DataFrame is empty. Cannot split data.")
else:
    print("Merged data is empty. Cannot proceed.")