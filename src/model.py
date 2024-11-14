import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Đọc dữ liệu từ file Excel
data = pd.read_excel('src/driver.xlsx')

print("Các cột trong dữ liệu:", data.columns)

try:
    features = data.drop(columns=['Pts', 'Driver_name', 'Team', 'year'])
    target = data['Pts']
except KeyError:
    print("Lỗi: Không tìm thấy cột mục tiêu trong dữ liệu. Hãy kiểm tra tên cột và sửa lại trong code.")
    exit()

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Khởi tạo mô hình
model = RandomForestRegressor(random_state=42)

# Tối ưu hóa tham số
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']  # 'auto' không còn được hỗ trợ, sử dụng 'sqrt' hoặc 'log2'
}

grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Lấy mô hình tốt nhất
best_model = grid_search.best_estimator_

# Dự đoán trên tập kiểm tra
predictions = best_model.predict(X_test)

# Tính toán MSE và R²
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f'Mean Squared Error (MSE): {mse:.2f}')
print(f'R² Score: {r2:.2f}')

# Kiểm tra độ chính xác
accuracy_percentage = r2 * 100  # Chuyển đổi R² thành phần trăm
if accuracy_percentage >= 90:
    print(f"Mô hình đạt yêu cầu độ chính xác {accuracy_percentage:.2f}%.")
else:
    print(f"Mô hình chưa đạt yêu cầu độ chính xác {accuracy_percentage:.2f}%.")

# Lưu mô hình tốt nhất
joblib.dump(best_model, 'best_random_forest_model.pkl')