import streamlit as st
import cv2
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw
import io

st.set_page_config(page_title="笔记矫正 Pro", layout="wide")

# --- 初始化状态 ---
if 'points' not in st.session_state:
    st.session_state.points = []
if 'last_point' not in st.session_state:
    st.session_state.last_point = None

# 定义选点顺序提示
POINT_LABELS = ["左上 (Top-Left)", "右上 (Top-Right)", "右下 (Bottom-Right)", "左下 (Bottom-Left)"]

st.title("📸 智能笔记透视矫正器")

# --- 侧边栏 ---
with st.sidebar:
    st.header("操作步骤")
    uploaded_file = st.file_uploader("1. 上传照片", type=["jpg", "png"])
    
    if st.button("🔄 重置所有选点"):
        st.session_state.points = []
        st.rerun()

    st.divider()
    # 动态显示进度
    for i, label in enumerate(POINT_LABELS):
        if len(st.session_state.points) > i:
            st.write(f"✅ {label}")
        else:
            st.write(f"⭕ {label}")

# --- 主逻辑 ---
if uploaded_file:
    # 1. 加载原图
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, 1)
    orig_h, orig_w = img_bgr.shape[:2]
    
    # 2. 计算显示缩放比例 (规定显示最大宽度为 700)
    DISPLAY_WIDTH = 700
    scale = DISPLAY_WIDTH / orig_w
    display_h = int(orig_h * scale)
    
    # 准备用于显示的 PIL 图片
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    # 实际上 streamlit_image_coordinates 会根据容器自动缩放，
    # 我们最好手动 Resize 以确保坐标计算精确。
    display_img = pil_img.resize((DISPLAY_WIDTH, display_h))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("原图选点")
        # 如果还没选完，提示下一步
        if len(st.session_state.points) < 4:
            st.info(f"👉 请点击：**{POINT_LABELS[len(st.session_state.points)]}**")
        
        # 在图片上画出已选的点，方便用户查看
        draw_img = display_img.copy()
        draw = ImageDraw.Draw(draw_img)
        for i, (px, py) in enumerate(st.session_state.points):
            # 将“原始坐标”映射回“显示坐标”画出来
            dx, dy = px * scale, py * scale
            draw.ellipse([dx-5, dy-5, dx+5, dy+5], fill="red", outline="white")
            draw.text((dx+10, dy+10), str(i+1), fill="red")

        # 获取点击坐标
        value = streamlit_image_coordinates(draw_img, key="coords")

        if value is not None:
            # 关键：将点击的显示坐标 (value['x']) 映射回 原始坐标
            actual_x = value["x"] / scale
            actual_y = value["y"] / scale
            new_point = (actual_x, actual_y)

            if len(st.session_state.points) < 4 and new_point != st.session_state.last_point:
                st.session_state.points.append(new_point)
                st.session_state.last_point = new_point
                st.toast(f"已成功捕获第 {len(st.session_state.points)} 个点！", icon="📍")
                st.rerun()

    with col2:
        st.subheader("矫正效果预览")
        if len(st.session_state.points) == 4:
            # 执行 OpenCV 变换
            src_pts = np.array(st.session_state.points, dtype="float32")
            
            # 计算目标纵横比 (简单处理：取选点范围的最大宽高)
            w1 = np.sqrt(((src_pts[1][0]-src_pts[0][0])**2) + ((src_pts[1][1]-src_pts[0][1])**2))
            w2 = np.sqrt(((src_pts[2][0]-src_pts[3][0])**2) + ((src_pts[2][1]-src_pts[3][1])**2))
            h1 = np.sqrt(((src_pts[1][0]-src_pts[2][0])**2) + ((src_pts[1][1]-src_pts[2][1])**2))
            h2 = np.sqrt(((src_pts[0][0]-src_pts[3][0])**2) + ((src_pts[0][1]-src_pts[3][1])**2))
            
            max_w, max_h = int(max(w1, w2)), int(max(h1, h2))
            dst_pts = np.array([[0, 0], [max_w-1, 0], [max_w-1, max_h-1], [0, max_h-1]], dtype="float32")
            
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(img_rgb, M, (max_w, max_h))
            
            st.image(warped, caption="矫正完成", use_container_width=True)
            
            # 导出按钮
            res_pil = Image.fromarray(warped)
            buf = io.BytesIO()
            res_pil.save(buf, format="JPEG")
            st.download_button("💾 保存笔记图片", buf.getvalue(), "note.jpg", "image/jpeg")
        else:
            st.warning("待选定 4 个顶点后显示结果...")

else:
    st.info("请先上传会议或课件照片。")