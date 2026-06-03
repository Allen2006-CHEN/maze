import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.animation as animation  
from typing import List, Tuple, Optional

def create_line(x1: float, x2: float, y1: float, y2: float, color: str = 'black', linewidth: int = 2) -> lines.Line2D:
    return lines.Line2D([x1, x2], [y1, y2], color=color, linewidth=linewidth)

def plot_maze(maze: List[List[int]], 
              start: Optional[Tuple[int, int]] = None, 
              end: Optional[Tuple[int, int]] = None,
              path: Optional[List[Tuple[int, int]]] = None) -> Tuple[plt.Figure, plt.Axes]: # 新增 path 參數
    
    if not maze or not maze[0]:
        raise ValueError("迷宮資料不可為空")

    height = len(maze)
    width = len(maze[0])
    
    fig, ax = plt.subplots(figsize=(width/1.5, height/1.5))

    ax.add_line(create_line(0, 0, 0, height, linewidth=3))
    ax.add_line(create_line(0, width, height, height, linewidth=3))
    ax.add_line(create_line(width, width, 0, height, linewidth=3))
    ax.add_line(create_line(0, width, 0, 0, linewidth=3))

    for i in range(height):
        for j in range(width):
            y_top = height - i
            y_bottom = height - i - 1
            
            if maze[i][j] & 1:  
                ax.add_line(create_line(j + 1, j + 1, y_bottom, y_top))
            if maze[i][j] & 2:  
                ax.add_line(create_line(j, j + 1, y_bottom, y_bottom))

    # ===== 新增：繪製解答路徑 =====
    if path:
        # 將陣列的 (row, col) 轉換為畫布的中心點 (x, y) 座標
        path_x = [col + 0.5 for row, col in path]
        path_y = [height - row - 0.5 for row, col in path]
        # 畫出一條藍色的線，alpha=0.4 設定為半透明以免遮擋起點終點字樣
        ax.plot(path_x, path_y, color='green', linewidth=4, alpha=0.4)

    if start:
        row, col = start
        ax.plot(col + 0.5, height - row - 0.5, marker='o', markersize=16, color='green')
        ax.text(col + 0.5, height - row - 0.5, 'S', color='white', ha='center', va='center', fontweight='bold')

    if end:
        row, col = end
        ax.plot(col + 0.5, height - row - 0.5, marker='o', markersize=16, color='red')
        ax.text(col + 0.5, height - row - 0.5, 'E', color='white', ha='center', va='center', fontweight='bold')

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_aspect('equal') 
    ax.axis('off')  
                  
def plot_path(maze, path, fig, ax):
    height = len(maze)

    # 初始化函數
    adjusted_path = [(x+0.5, height-y-0.5) for y, x in path]
    x_data, y_data = zip(*adjusted_path)

    def init():
        line.set_data([], [])
        return line,

    # 更新函數
    def update(num):
        line.set_data(x_data[:num+1], y_data[:num+1])
        return line,

    # lw (線寬) 稍微調粗一點，顏色換成藍色以免跟終點的紅色搞混
    line, = ax.plot([], [], color='blue', lw=4, alpha=0.6)
    
    # 建立動畫
    ani = animation.FuncAnimation(
        fig, update, frames=len(path), init_func=init,
        interval=100, blit=True, repeat=False
    )
    
    return fig, ax, ani

                  

