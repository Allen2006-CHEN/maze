import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import random  # 用於隨機生成陷阱位置

from maze_generator import generate_maze
from maze_drawer import plot_maze, plot_path
from maze_solver import a_star

def main():
    st.title("我的 2D 隨機迷宮 (黃金路徑保護版)") 
    
    # ==========================================
    # 1. 側邊欄設定區
    # ==========================================
    st.sidebar.header("迷宮設定")
    width = st.sidebar.slider("迷宮寬度", 5, 30, 20)
    height = st.sidebar.slider("迷宮高度", 5, 30, 15)
    
    # 陷阱密度設定 (0% - 30%)
    trap_percent = st.sidebar.slider("尖刺陷阱密度 (%)", 0, 30, 10)
    
    regen_button = st.sidebar.button("產生新地圖 (迷宮+陷阱)")

    # ==========================================
    # 2. 記憶體機制 (Session State)
    # ==========================================
    if 'maze' not in st.session_state or 'traps' not in st.session_state or regen_button:
        # 2a. 生成迷宮
        st.session_state.maze = generate_maze(width, height)
        
        # ==================================================================
        # 2b. 【核心修改】生成隨機陷阱（導入黃金路徑保護機制）
        # ==================================================================
        # 計算需要多少陷阱格
        num_cells = width * height
        num_traps = int(num_cells * (trap_percent / 100))
        
        # 找出所有可能的格子座標
        all_cells = [(r, c) for r in range(height) for c in range(width)]
        
        # 💡 先在完全沒有陷阱的狀態下，算出一條從 (0,0) 到 (H-1, W-1) 的保底黃金路徑
        golden_path = a_star(st.session_state.maze, 0, 0, height - 1, width - 1, traps=set())
        
        # 篩選安全格子：必須不是預設起終點，且【絕對不能】落在剛剛算出來的黃金路徑上
        # 這樣就能確保這一條活路不會被尖刺截斷
        safe_cells = [cell for cell in all_cells if cell not in golden_path]
        
        # 從剩餘的安全區域中隨機抽取陷阱位置
        if len(safe_cells) >= num_traps:
            selected_traps = random.sample(safe_cells, num_traps)
        else:
            selected_traps = safe_cells # 萬一安全格子不夠，就放滿安全區
            
        # 將陷阱儲存為集合(Set)
        st.session_state.traps = set(selected_traps)

    # 從記憶體中拿出鎖定的迷宮和陷阱
    random_maze = st.session_state.maze
    spike_traps = st.session_state.traps

    # ==========================================
    # 3. 位置設定 (起點/終點)
    # ==========================================
    st.sidebar.header("位置設定")
    start_y = st.sidebar.number_input("起點 Y (上下)", 0, height - 1, 0)
    start_x = st.sidebar.number_input("起點 X (左右)", 0, width - 1, 0)
    
    end_y = st.sidebar.number_input("終點 Y (上下)", 0, height - 1, height - 1)
    end_x = st.sidebar.number_input("終點 X (左右)", 0, width - 1, width - 1)

    start_pos = (start_y, start_x)
    end_pos = (end_y, end_x)

    # 關鍵防守邏輯：如果使用者手動將起終點移到原有的陷阱上，動態將其移除，確保起終點可通行
    valid_traps = spike_traps.copy()
    if start_pos in valid_traps: valid_traps.remove(start_pos)
    if end_pos in valid_traps: valid_traps.remove(end_pos)

    # ==========================================
    # 4. 動畫速度設定
    # ==========================================
    st.sidebar.header("動畫設定")
    anim_speed = st.sidebar.slider("每步延遲 (毫秒)", 10, 500, 100, step=10)
    
    # ==========================================
    # 5. 計算路徑與繪圖
    # ==========================================
    solution_path = a_star(random_maze, start_pos[0], start_pos[1], end_pos[0], end_pos[1], traps=valid_traps)
    fig, ax = plot_maze(random_maze, start=start_pos, end=end_pos, traps=valid_traps)
    
    if solution_path:
        plt.title(f"A* Path Found! ({width}x{height})")
        fig, ax, ani = plot_path(random_maze, solution_path, fig, ax, speed_ms=anim_speed)
        
        with st.spinner("正在生成尋路動畫..."):
            components.html(ani.to_jshtml(), height=850, scrolling=True)
    else:
        plt.title(f"No Path Found... Spiked Blocked ({width}x{height})")
        st.pyplot(fig)
        st.error("糟糕！路徑被牆壁或尖刺陷阱完全封死了。請嘗試移動起終點，或按按鈕產生新地圖！")

if __name__ == "__main__":
    main()


