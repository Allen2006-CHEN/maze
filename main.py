import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
import random  # 新增：用於隨機生成陷阱位置

from maze_generator import generate_maze
from maze_drawer import plot_maze, plot_path
from maze_solver import a_star

def main():
    st.title("我的 2D 隨機迷宮 (尖刺陷阱版)") 
    
    # ==========================================
    # 1. 側邊欄設定區 (新增陷阱密度 Slider)
    # ==========================================
    st.sidebar.header("迷宮設定")
    width = st.sidebar.slider("迷宮寬度", 5, 30, 20)
    height = st.sidebar.slider("迷宮高度", 5, 30, 15)
    
    # 新增：陷阱密度設定 (0% - 30%)
    trap_percent = st.sidebar.slider("尖刺陷阱密度 (%)", 0, 30, 10)
    
    regen_button = st.sidebar.button("產生新地圖 (迷宮+陷阱)")

    # ==========================================
    # 2. 記憶體機制 (Session State) - 升級版
    # ==========================================
    # 如果記憶體裡沒有地圖，或者按下重新生成按鈕
    if 'maze' not in st.session_state or 'traps' not in st.session_state or regen_button:
        # 2a. 生成迷宮
        st.session_state.maze = generate_maze(width, height)
        
        # 2b. 新增：生成隨機陷阱
        # 計算需要多少陷阱格
        num_cells = width * height
        num_traps = int(num_cells * (trap_percent / 100))
        
        # 找出所有可能的格子座標
        all_cells = [(r, c) for r in range(height) for c in range(width)]
        
        # 我們必須確保預設的起點 (0,0) 和終點 (H-1, W-1) 不會有陷阱
        # 免得地圖一生成就死局
        safe_cells = [cell for cell in all_cells if cell != (0, 0) and cell != (height-1, width-1)]
        
        # 從安全區域中隨機抽取陷阱位置
        if len(safe_cells) >= num_traps:
            selected_traps = random.sample(safe_cells, num_traps)
        else:
            selected_traps = safe_cells # 萬一格子不夠，就全放(雖然不太可能)
            
        # 將陷阱儲存為集合(Set)，優化 A* 的查找速度
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

    # ⚠️ 關鍵防守邏輯：如果使用者把起終點手動移到陷阱上，我們在畫圖和算路徑時要「移除」該處陷阱
    # 否則 A* 會報錯說找不到起點或終點
    valid_traps = spike_traps.copy()
    if start_pos in valid_traps: valid_traps.remove(start_pos)
    if end_pos in valid_traps: valid_traps.remove(end_pos)

    # ==========================================
    # 4. 動畫速度設定
    # ==========================================
    st.sidebar.header("動畫設定")
    anim_speed = st.sidebar.slider("每步延遲 (毫秒)", 10, 500, 100, step=10)
    
    # ==========================================
    # 5. 計算路徑與繪圖 (呼叫時加入 valid_traps)
    # ==========================================
    # 核心修改：呼叫 A* 時傳入陷阱
    solution_path = a_star(random_maze, start_pos[0], start_pos[1], end_pos[0], end_pos[1], traps=valid_traps)
    
    # 核心修改：呼叫 plot_maze 時傳入陷阱以繪製圖示
    fig, ax = plot_maze(random_maze, start=start_pos, end=end_pos, traps=valid_traps)
    
    if solution_path:
        plt.title(f"A* Path Found! Avoding Spikes ({width}x{height})")
        # 保留你上一版厲害的動畫功能
        fig, ax, ani = plot_path(random_maze, solution_path, fig, ax, speed_ms=anim_speed)
        
        with st.spinner("正在生成尋路動畫..."):
            # 保持滾動和高度設定
            components.html(ani.to_jshtml(), height=850, scrolling=True)
    else:
        plt.title(f"No Path Found... Spiked Blocked ({width}x{height})")
        st.pyplot(fig)
        st.error("糟糕！路徑被牆壁或尖刺陷阱完全封死了。請嘗試移動起終點，或按按鈕產生新地圖！")

if __name__ == "__main__":
    main()


