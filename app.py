import json
import os
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Cấu hình giao diện trang web Streamlit
st.set_page_config(
    page_title="NASA NEO Tracker Dashboard",
    page_icon="☄️",
    layout="wide",
)

st.title("☄️ NASA Space Apps Challenge - NEO Tracker Dashboard")
st.markdown(
    "Dashboard tương tác theo dõi các Tiểu hành tinh gần Trái Đất (Near Earth Objects) dựa trên dữ liệu thời gian thực từ NASA API."
)


# 2. Hàm đọc dữ liệu từ file JSON bạn đã xuất ra
@st.cache_data
@st.cache_data
def load_data():
  json_file = 'nasa_neo_data.json'
  if not os.path.exists(json_file):
    return None

  with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

  rows = []
  # Kiểm tra nếu dữ liệu là danh sách (list)
  if isinstance(data, list):
    for item in data:
      rows.append({
          'Ngày tiếp cận': item.get('Ngày tiếp cận'),
          'Tên tiêu hành tinh': item.get('Tên tiêu hành tinh'),
          'Đường kính tối đa (m)': item.get('Đường kính tối đa (m)'),
          'Vận tốc (km/h)': item.get('Vận tốc (km/h)'),
          'Khoảng cách tới Trái đất (km)': item.get(
              'Khoảng cách tới Trái đất (km)'
          ),
          'Cảnh báo nguy hiểm': item.get('Cảnh báo nguy hiểm'),
      })
  # Kiểm tra nếu dữ liệu là từ điển (dict)
  elif isinstance(data, dict):
    for date_str, items in data.items():
      for item in items:
        rows.append({
            'Ngày tiếp cận': item.get('Ngày tiếp cận'),
            'Tên tiêu hành tinh': item.get('Tên tiêu hành tinh'),
            'Đường kính tối đa (m)': item.get('Đường kính tối đa (m)'),
            'Vận tốc (km/h)': item.get('Vận tốc (km/h)'),
            'Khoảng cách tới Trái đất (km)': item.get(
                'Khoảng cách tới Trái đất (km)'
            ),
            'Cảnh báo nguy hiểm': item.get('Cảnh báo nguy hiểm'),
        })

  return pd.DataFrame(rows)


df = load_data()

if df is None or df.empty:
  st.error(
      "Không tìm thấy file `nasa_neo_data.json`. Hãy chạy file code lấy dữ liệu"
      " NASA trước!"
  )
else:
  # 3. Hiển thị các chỉ số tổng quan (Metrics) ở đầu trang
  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric(
        label="Tổng số tiểu hành tinh quét được", value=len(df)
    )
  with col2:
    hazardous_count = df[
        df["Cảnh báo nguy hiểm"].str.contains("có|Nguy hiểm", case=False, na=False)
    ].shape[0]
    st.metric(
        label="Số lượng cảnh báo nguy hiểm",
        value=hazardous_count,
        delta=f"{hazardous_count} cần chú ý",
    )
  with col3:
    max_speed = (
        f"{df['Vận tốc (km/h)'].max():,.0f} km/h"
        if not df.empty
        else "0 km/h"
    )
    st.metric(label="Vận tốc tối đa ghi nhận", value=max_speed)

  st.divider()

  # 4. Khu vực vẽ biểu đồ 2D và 3D tương tác
  tab1, tab2, tab3 = st.tabs([
      "📊 Biểu đồ Phân tích 2D",
      "🌐 Mô phỏng Không gian 3D",
      "📋 Dữ liệu chi tiết",
  ])

  with tab1:
    st.subheader("Tương quan giữa Khoảng cách và Vận tốc bay")
    fig_2d = px.scatter(
        df,
        x="Khoảng cách tới Trái đất (km)",
        y="Vận tốc (km/h)",
        size="Đường kính tối đa (m)",
        color="Cảnh báo nguy hiểm",
        hover_name="Tên tiêu hành tinh",
        title=(
            "Biểu đồ phân tán: Khoảng cách, Vận tốc và Kích thước tiểu hành tinh"
        ),
        template="plotly_dark",
    )
    st.plotly_chart(fig_2d, use_container_width=True)

  with tab2:
    st.subheader(
        "Mô hình không gian 3D (Khoảng cách - Vận tốc - Đường kính tối đa)"
    )
    fig_3d = px.scatter_3d(
        df,
        x="Khoảng cách tới Trái đất (km)",
        y="Vận tốc (km/h)",
        z="Đường kính tối đa (m)",
        color="Cảnh báo nguy hiểm",
        hover_name="Tên tiêu hành tinh",
        title="Không gian 3D Quỹ đạo tiếp cận Tiểu hành tinh",
        template="plotly_dark",
    )
    st.plotly_chart(fig_3d, use_container_width=True)

  with tab3:
    st.subheader("Bảng dữ liệu chi tiết thô")
    st.dataframe(df, use_container_width=True)
