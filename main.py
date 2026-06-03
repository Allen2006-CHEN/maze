import matplotlib.pyplot as plt

# 匯入我們的兩個自製模組
from maze_generator import generate_maze
from maze_drawer import plot_maze

def main():
    # 1. 設定你想要的迷宮大小
    width = 20
    height = 15
    
    print(f"正在生成 {width}x{height} 的隨機迷宮...")
    # 2. 呼叫演算法產生隨機陣列
    random_maze = generate_maze(width, height)
    
    # 3. 呼叫繪圖函式，並自動將起點設為左上角，終點設為右下角
    print("正在繪製迷宮圖形...")
    start_pos = (0, 0)
    end_pos = (height - 1, width - 1)
    
    fig, ax = plot_maze(random_maze, start=start_pos, end=end_pos)
    
    # 4. 加上標題並顯示視窗
    plt.title(f"Random Maze ({width}x{height})")
    plt.show()

if __name__ == "__main__":
    main()