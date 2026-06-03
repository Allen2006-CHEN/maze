import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components  # 新增：用來顯示 HTML 動畫

from maze_generator import generate_maze
from maze_drawer import plot_maze, plot_path  # 新增引入 plot_path
from maze_solver import a_star

def main():
    st.title("我的 2D 隨機迷宮 (A* 動畫版)") 
    
    st.sidebar.header("迷宮設定")
    width = st.sidebar.slider("迷宮寬度", 5, 30, 20)
    height = st.sidebar.slider("迷宮高度", 5, 30, 15)
    
    if st.button("重新生成迷宮"):
        pass

    # 1. 產生迷宮
    random_maze = generate_maze(width, height)
    start_pos = (0, 0)
    end_pos = (height - 1, width - 1)
    
    # 2. 計算路徑
    solution_path = a_star(random_maze, start_pos[0], start_pos[1], end_pos[0], end_pos[1])
    
    # 3. 畫出「靜態」的底圖 (這時先不要傳 path 進去，保留空畫布)
    fig, ax = plot_maze(random_maze, start=start_pos, end=end_pos)
    plt.title(f"A* Path Finding... ({width}x{height})")
    
    # 4. 在底圖上加上動畫
    fig, ax, ani = plot_path(random_maze, solution_path, fig, ax)
    
    # 5. 關鍵步驟：把動畫轉成 HTML JavaScript 格式，並用 components 顯示
    with st.spinner("正在生成動畫，請稍候..."):
        # to_jshtml() 會產生一個帶有播放/暫停按鈕的互動式播放器
        components.html(ani.to_jshtml(), height=600)

if __name__ == "__main__":
    main()


