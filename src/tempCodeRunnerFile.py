accuracy_percentage = r2 * 100  # Chuyển đổi R² thành phần trăm
if accuracy_percentage >= 90:
    print(f"Mô hình đạt yêu cầu độ chính xác {accuracy_percentage:.2f}%.")
else:
    print(f"Mô hình chưa đạt yêu cầu độ chính xác {accuracy_percentage:.2f}%.")
