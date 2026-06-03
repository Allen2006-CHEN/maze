import matplotlib.pyplot as plt
import streamlit as st  # 必須引入 streamlit

from maze_generator import generate_maze
from maze_drawer import plot_maze

def main():
    # 1. 網頁標題
    st.title("我的 2D 隨機迷宮網站") 
    
    # 2. 網頁側邊欄設定
    st.sidebar.header("迷宮設定")
    width = st.sidebar.slider("迷宮寬度", 5, 30, 20)
    height = st.sidebar.slider("迷宮高度", 5, 30, 15)
    
    if st.button("重新生成迷宮"):
        pass # 按下按鈕時，Streamlit 會自動重新整理網頁

    # 3. 生成迷宮與畫圖
    random_maze = generate_maze(width, height)
    start_pos = (0, 0)
    end_pos = (height - 1, width - 1)
    
    fig, ax = plot_maze(random_maze, start=start_pos, end=end_pos)
    plt.title(f"Random Maze ({width}x{height})")
    
    # 4. 關鍵指令：把圖表畫在網頁上！
    st.pyplot(fig)

if __name__ == "__main__":
    main()
