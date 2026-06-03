import matplotlib.pyplot as plt
import streamlit as st

from maze_generator import generate_maze
from maze_drawer import plot_maze
from maze_solver import a_star  # 引入你寫好的 A* 演算法

def main():
    st.title("我的 2D 隨機迷宮網站 (含 A*search 尋路)") 
    
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
    # 傳入：迷宮陣列, 起點Y, 起點X, 終點Y, 終點X
    solution_path = a_star(random_maze, start_pos[0], start_pos[1], end_pos[0], end_pos[1])
    
    # 3. 畫圖 (把算出來的路徑丟給 plot_maze)
    fig, ax = plot_maze(random_maze, start=start_pos, end=end_pos, path=solution_path)
    plt.title(f"A* Path Found! ({width}x{height})")
    
    # 4. 顯示在網站上
    st.pyplot(fig)

if __name__ == "__main__":
    main()


