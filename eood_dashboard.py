import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Danh sách sản phẩm mẫu
product_list = [
    "Khăn mặt bông Deary 28*46 (10 cái/Túi)",
    "Dao cạo râu lưỡi kép có đệm bôi trơn LUS-3P; 3 Cái/Gói; 10 Gói/Hộp",
    "Dung dịch sát khuẩn On1 hương Bamboo Charcoal 500ml/CH20",
    "Nước rửa tay Aroma 500 g (12 chai/thùng)",
    "Sữa tắm không chất phụ gia Pharmaact 600ml (16 Chai/ Thùng)",
    "Dầu gội FARA cho tóc nhuộm 250ml (12 chai/thùng)",
    "Bột giặt Polar Bear đỏ 2,25kg ( 8 túi/Bao )",
    "Nước giặt cao cấp Caremore hương nước hoa 3,8 kg",
    "Nước xả vải đậm đặc FUWA 500ml (20 Túi/ Thùng)",
    "Nước lau sàn Izana hương quế 2.1 kg (6 chai/ thùng)",
    "Nước tẩy toilet Kliin 500g",
    "Nước uống tăng lực Rồng Đỏ hương dâu 330ml (6 chai*4 lốc/thùng)",
    "Rượu Vodka Cọ chai thủy tinh 600ml - 6 chai/thùng",
    "Cà phê VCF 3in1 Gold 18 gói*17g",
    "Bột ngũ cốc 5 thứ đậu 400g (28 Gói/ Thùng)",
    "Trà Akbar mixed fruit 24x20x2g"
]

# Giả lập dữ liệu dự đoán OOD
data = pd.DataFrame({
    "Product ID": [f"SP{i}" for i in range(len(product_list))],
    "Product Name": product_list,
    "Province": np.random.choice(["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Cần Thơ"], len(product_list)),
    "Prediction": np.random.choice(["OOD", "ID"], len(product_list), p=[0.4, 0.6]),
    "Confidence Score": np.round(np.random.uniform(0.7, 1.0, len(product_list)), 2),
    "Revenue": np.round(np.random.uniform(500000, 5000000, len(product_list)), -3)
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
ood_pie_data.columns = ["Prediction", "Count"]
fig_pie = px.pie(ood_pie_data, names="Prediction", values="Count", title="🎯 Tỷ lệ OOD vs ID trên toàn bộ dữ liệu")
st.plotly_chart(fig_pie, use_container_width=True)

# Giả lập dữ liệu xu hướng phát hiện OOD theo thời gian
data["Date"] = np.random.choice(pd.date_range(start="2024-01-01", periods=30, freq="D"), len(data))
ood_trend = data[data["Prediction"] == "OOD"].groupby("Date").size().reset_index(name="Count")

# Đảm bảo có dữ liệu trên toàn bộ 30 ngày
date_range = pd.DataFrame({"Date": pd.date_range(start="2024-01-01", periods=30, freq="D")})
ood_trend = date_range.merge(ood_trend, on="Date", how="left").fillna(0)

# Vẽ biểu đồ xu hướng OOD
fig_trend = px.line(ood_trend, x="Date", y="Count", markers=True, title="📉 Xu hướng phát hiện OOD theo thời gian")
st.plotly_chart(fig_trend, use_container_width=True)

# Hiển thị cảnh báo nếu số lượng OOD tăng mạnh
total_ood = len(data[data["Prediction"] == "OOD"])
if total_ood > 3:
    st.warning(f"🚨 Cảnh báo: Có {total_ood} sản phẩm được xác định là OOD! Kiểm tra ngay.")
if ood_trend["Count"].tail(3).mean() > 8:
    st.error("🚨 Cảnh báo: Số lượng OOD đang tăng nhanh trong 3 ngày qua! Kiểm tra hệ thống ngay.")

st.success("🎉 Dashboard hoạt động tốt! Hãy sử dụng bộ lọc để xem thông tin chi tiết.")
