import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import random

from maze_generator import generate_maze
from maze_drawer import plot_maze, plot_path
from maze_solver import a_star

def main():
    st.title("我的 2D 隨機迷宮 (動態洗牌 + 絕對防堵版)") 
    
    # ==========================================
    # 1. 側邊欄：地圖與位置參數輸入
    # ==========================================
    st.sidebar.header("迷宮設定")
    width = st.sidebar.slider("迷宮寬度", 5, 30, 20)
    height = st.sidebar.slider("迷宮高度", 5, 30, 15)
    trap_percent = st.sidebar.slider("陷阱密度 (%)", 0, 30, 10)
    regen_button = st.sidebar.button("產生新地圖 (迷宮+陷阱)")
    
    st.sidebar.header("位置設定")
    start_y = st.sidebar.number_input("起點 Y (上下)", 0, height - 1, 0)
    start_x = st.sidebar.number_input("起點 X (左右)", 0, width - 1, 0)
    end_y = st.sidebar.number_input("終點 Y (上下)", 0, height - 1, height - 1)
    end_x = st.sidebar.number_input("終點 X (左右)", 0, width - 1, width - 1)

    start_pos = (start_y, start_x)
    end_pos = (end_y, end_x)

    st.sidebar.header("動畫設定")
    anim_speed = st.sidebar.slider("每步延遲 (毫秒)", 10, 500, 100, step=10)

    # ==========================================
    # 2. 狀態偵測 (判斷使用者動了什麼)
    # ==========================================
    if 'prev_start' not in st.session_state: st.session_state.prev_start = start_pos
    if 'prev_end' not in st.session_state: st.session_state.prev_end = end_pos
    if 'prev_trap_pct' not in st.session_state: st.session_state.prev_trap_pct = trap_percent

    positions_changed = (start_pos != st.session_state.prev_start) or (end_pos != st.session_state.prev_end)
    pct_changed = (trap_percent != st.session_state.prev_trap_pct)

    # ==========================================
    # 3. 生成邏輯 (導入黃金路徑保護)
    # ==========================================
    if 'maze' not in st.session_state or regen_button:
        st.session_state.maze = generate_maze(width, height)
        st.session_state.need_new_traps = True 

    if 'traps' not in st.session_state or positions_changed or pct_changed or st.session_state.get('need_new_traps', False):
        num_cells = width * height
        num_traps = int(num_cells * (trap_percent / 100))
        all_cells = [(r, c) for r in range(height) for c in range(width)]
        
        # 💡【關鍵修復】先算出新起點到新終點的黃金路徑 (假裝沒有陷阱 traps=set())
        golden_path = a_star(st.session_state.maze, start_pos[0], start_pos[1], end_pos[0], end_pos[1], traps=set())
        
        # 防呆：如果迷宮本身真的連一條路都沒有，就只保護起終點
        if not golden_path:
            protected_cells = [start_pos, end_pos]
        else:
            protected_cells = golden_path

        # 從所有格子中，把「黃金路徑」上的格子剔除，剩下的才是可以撒陷阱的區域
        safe_cells = [cell for cell in all_cells if cell not in protected_cells]
        
        if len(safe_cells) >= num_traps:
            selected_traps = random.sample(safe_cells, num_traps)
        else:
            selected_traps = safe_cells
            
        st.session_state.traps = set(selected_traps)
        
        st.session_state.need_new_traps = False
        st.session_state.prev_start = start_pos
        st.session_state.prev_end = end_pos
        st.session_state.prev_trap_pct = trap_percent

    random_maze = st.session_state.maze
    valid_traps = st.session_state.traps

    # ==========================================
    # 4. 計算路徑與繪圖
    # ==========================================
    solution_path = a_star(random_maze, start_pos[0], start_pos[1], end_pos[0], end_pos[1], traps=valid_traps)
    fig, ax = plot_maze(random_maze, start=start_pos, end=end_pos, traps=valid_traps)
    
    if solution_path:
        plt.title(f"A* Path Found! ({width}x{height})")
        fig, ax, ani = plot_path(random_maze, solution_path, fig, ax, speed_ms=anim_speed)
        
        with st.spinner("正在生成尋路動畫..."):
            components.html(ani.to_jshtml(), height=850, scrolling=True)
    else:
        # 理論上有了黃金路徑保護，這裡永遠不該被觸發，除非你把迷宮調成死胡同地圖
        plt.title(f"No Path Found... ({width}x{height})")
        st.pyplot(fig)
        st.error("糟糕！路徑完全被牆壁封死了。請產生新地圖！")

if __name__ == "__main__":
    main()



