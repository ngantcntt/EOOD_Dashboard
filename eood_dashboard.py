import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Giả lập dữ liệu dự đoán OOD
data = pd.DataFrame({
    "Product ID": [f"SP{i}" for i in range(20)],
    "Province": np.random.choice(["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Cần Thơ"], 20),
    "Prediction": np.random.choice(["OOD", "ID"], 20, p=[0.4, 0.6]),
    "Confidence Score": np.round(np.random.uniform(0.7, 1.0, 20), 2),
    "Revenue": np.round(np.random.uniform(500000, 5000000, 20), -3)
})

# Tạo giao diện Streamlit
st.set_page_config(page_title="EOOD Detection Dashboard", layout="wide")
st.title("📊 EOOD Detection Dashboard - LIBERICO")
st.markdown("### Hệ thống phát hiện dữ liệu ngoài phân phối (OOD)")

# Bộ lọc dữ liệu
col1, col2 = st.columns(2)
province_filter = col1.selectbox("🔍 Chọn tỉnh thành:", ["Tất cả"] + list(data["Province"].unique()))
confidence_threshold = col2.slider("🎯 Ngưỡng độ tin cậy (Confidence Score)", 0.7, 1.0, 0.8)

# Lọc dữ liệu
filtered_data = data.copy()
if province_filter != "Tất cả":
    filtered_data = filtered_data[filtered_data["Province"] == province_filter]
filtered_data = filtered_data[filtered_data["Confidence Score"] >= confidence_threshold]

# Hiển thị bảng dữ liệu có màu sắc OOD
def highlight_ood(s):
    return ['background-color: #FFDDC1' if v == "OOD" else '' for v in s]

st.markdown("### 📋 Danh sách sản phẩm được phát hiện OOD")
st.dataframe(filtered_data.style.apply(highlight_ood, subset=["Prediction"]))

# Biểu đồ tỷ lệ OOD theo tỉnh
ood_counts = data[data["Prediction"] == "OOD"].groupby("Province").size().reset_index(name="Count")
fig_ood = px.bar(ood_counts, x="Province", y="Count", title="📌 Tỷ lệ OOD theo tỉnh", color="Province")
st.plotly_chart(fig_ood, use_container_width=True)

# Biểu đồ xu hướng doanh thu
time_series_data = data.groupby("Province")["Revenue"].sum().reset_index()
fig_revenue = px.line(time_series_data, x="Province", y="Revenue", markers=True, title="📈 Xu hướng doanh thu theo tỉnh")
st.plotly_chart(fig_revenue, use_container_width=True)

# Biểu đồ Pie Chart tổng quan tỷ lệ OOD
ood_pie_data = data["Prediction"].value_counts().reset_index()
fig_pie = px.pie(ood_pie_data, names="index", values="Prediction", title="🎯 Tỷ lệ OOD vs ID trên toàn bộ dữ liệu")
st.plotly_chart(fig_pie, use_container_width=True)

# Xu hướng phát hiện OOD theo thời gian
data["Date"] = np.random.choice(pd.date_range(start="2024-01-01", periods=30, freq="D"), len(data))
ood_trend = data[data["Prediction"] == "OOD"].groupby("Date").size().reset_index(name="Count")
fig_trend = px.line(ood_trend, x="Date", y="Count", markers=True, title="📉 Xu hướng phát hiện OOD theo thời gian")
st.plotly_chart(fig_trend, use_container_width=True)

# Hiển thị cảnh báo nếu số lượng OOD tăng mạnh
total_ood = len(data[data["Prediction"] == "OOD"])
if total_ood > 10:
    st.warning(f"🚨 Cảnh báo: Có {total_ood} sản phẩm được xác định là OOD! Kiểm tra ngay.")
if ood_trend["Count"].tail(3).mean() > 8:
    st.error("🚨 Cảnh báo: Số lượng OOD đang tăng nhanh trong 3 ngày qua! Kiểm tra hệ thống ngay.")

st.success("🎉 Dashboard hoạt động tốt! Hãy sử dụng bộ lọc để xem thông tin chi tiết.")
