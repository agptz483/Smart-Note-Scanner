# 📸 智能笔记透视矫正器 (Smart Note Scanner)  
这是一个基于 **Streamlit** 和 **OpenCV** 开发的轻量级 Web 工具。它可以帮助你将会议、课堂上侧拍的、存在透视畸形的笔记或屏幕照片，矫正为正视角的、工整的电子笔记。  
## ✨ 功能特点  
* **🖱️ 交互式选点**：通过鼠标点击图片上的四个顶点（左上、右上、右下、左下），直观地确定矫正区域。  
* **📐 自动透视变换**：基于 OpenCV 的 `getPerspectiveTransform` 算法，实现高质量的图像拉伸与矫正。  
* **📏 智能尺寸计算**：自动计算目标区域的最佳纵横比，确保矫正后的文字不拉伸、不变形。  
* **💾 一键导出**：处理完成后，可直接下载高质量的 JPEG 图片进行保存。  
## 🚀 快速开始  
### 本地运行  
1. **克隆项目**  
   ```bash  
   git clone [https://github.com/agptz483/Smart-Note-Scanner.git](https://github.com/agptz483/Smart-Note-Scanner.git)  
   cd 你的仓库名  
   ```
2. **安装依赖**  
```Bash  
pip install -r requirements.txt  
```
3. **启动应用**  
```Bash  
streamlit run app.py  
```  
## 🛠️ 技术栈    
UI 框架: Streamlit  
图像处理: OpenCV (Open Source Computer Vision Library)  
矩阵运算: Numpy  
交互组件: streamlit-image-coordinates  

## 📝 使用提示  
为了获得最佳效果，请按照以下顺序点击原图：  
左上角 -> 2. 右上角 -> 3. 右下角 -> 4. 左下角  

如果你觉得这个小工具对你有帮助，欢迎给个 ⭐ Star！  