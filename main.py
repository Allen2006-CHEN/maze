import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components

from maze_generator import generate_maze
from maze_drawer import plot_maze, plot_path
from maze_solver import a_star

def main():
    st.title("我的 2D 隨機迷宮 (自訂起點版)") 
    
    # ==========================================
    # 1. 迷宮大小設定
    # ==========================================
    st.sidebar.header("迷宮設定")
    width = st.sidebar.slider("迷宮寬度", 5, 30, 20)
    height = st.sidebar.slider("迷宮高度", 5, 30, 15)
    
    # ==========================================
    # 2. 記憶體機制 (Session State)
    # ==========================================
    # 如果記憶體裡還沒有 'maze'，或者使用者按下了重新生成按鈕，才產生新陣列
    if 'maze' not in st.session_state or st.sidebar.button("產生新迷宮"):
        st.session_state.maze = generate_maze(width, height)

    # 從記憶體中把迷宮拿出來用 (這樣調整參數時，地圖就不會變了)
    random_maze = st.session_state.maze

    # ==========================================
    # 3. 新增：起點與終點設定
    # ==========================================
    st.sidebar.header("位置設定")
    # 使用 number_input 讓使用者精確輸入座標
    # 限制最小值為 0，最大值不可超過 迷宮高度/寬度-1
    start_y = st.sidebar.number_input("起點 Y 座標 (上下)", 0, height - 1, 0)
    start_x = st.sidebar.number_input("起點 X 座標 (左右)", 0, width - 1, 0)
    
    end_y = st.sidebar.number_input("終點 Y 座標 (上下)", 0, height - 1, height - 1)
    end_x = st.sidebar.number_input("終點 X 座標 (左右)", 0, width - 1, width - 1)

    start_pos = (start_y, start_x)
    end_pos = (end_y, end_x)

    # ==========================================
    # 4. 動畫速度設定
    # ==========================================
    st.sidebar.header("動畫設定")
    anim_speed = st.sidebar.slider("每步延遲 (毫秒/越小越快)", 10, 500, 100, step=10)
    
    # ==========================================
    # 5. 計算路徑與繪圖
    # ==========================================
    solution_path = a_star(random_maze, start_pos[0], start_pos[1], end_pos[0], end_pos[1])
    
    fig, ax = plot_maze(random_maze, start=start_pos, end=end_pos)
    
    # 防呆機制：因為起點和終點可以亂動，如果遇到死胡同找不到路徑時，要避免動畫報錯
    if solution_path:
        plt.title(f"A* Path Found! ({width}x{height})")
        fig, ax, ani = plot_path(random_maze, solution_path, fig, ax, speed_ms=anim_speed)
        
        with st.spinner("正在生成動畫，請稍候..."):
            components.html(ani.to_jshtml(), height=850, scrolling=True)
    else:
        # 如果找不到路徑 (solution_path 是空的)，就只畫出靜態迷宮並跳出警告
        plt.title(f"No Path Found... ({width}x{height})")
        st.pyplot(fig)
        st.error("糟糕！從這個起點到終點沒有路可以通（被牆壁封死了）。請嘗試移動起點或終點！")

if __name__ == "__main__":
    main()


