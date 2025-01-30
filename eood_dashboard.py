import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Giả lập dữ liệu dự đoán OOD
data = pd.DataFrame({
    "Product ID": [f"SP{i}" for i in range(10)],
    "Province": np.random.choice(["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Cần Thơ"], 10),
    "Prediction": np.random.choice(["OOD", "ID"], 10, p=[0.4, 0.6]),
    "Confidence Score": np.round(np.random.uniform(0.7, 1.0, 10), 2)
})

# Giao diện Streamlit
st.title("EOOD Detection Dashboard")
st.subheader("📊 Phát hiện dữ liệu ngoài phân phối (OOD) trong hệ thống LIBERICO")

# Bộ lọc tỉnh thành
province_filter = st.selectbox("Chọn tỉnh thành:", ["Tất cả"] + list(data["Province"].unique()))

# Lọc dữ liệu theo tỉnh
if province_filter != "Tất cả":
    filtered_data = data[data["Province"] == province_filter]
else:
    filtered_data = data

# Hiển thị bảng dữ liệu
st.dataframe(filtered_data)

# Biểu đồ tỷ lệ OOD theo tỉnh
ood_counts = data[data["Prediction"] == "OOD"].groupby("Province").size()
plt.figure(figsize=(6,4))
plt.bar(ood_counts.index, ood_counts.values, color='red')
plt.xlabel("Tỉnh thành")
plt.ylabel("Số lượng OOD")
plt.title("Tỷ lệ phát hiện OOD theo tỉnh")
st.pyplot(plt)

st.success("Dashboard hoạt động! Bạn có thể lọc dữ liệu và kiểm tra kết quả.")