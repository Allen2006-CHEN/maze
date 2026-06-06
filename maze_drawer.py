import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.animation as animation  
from typing import List, Tuple, Optional, Set

def create_line(x1: float, x2: float, y1: float, y2: float, color: str = 'black', linewidth: int = 2) -> lines.Line2D:
    return lines.Line2D([x1, x2], [y1, y2], color=color, linewidth=linewidth)

def plot_maze(maze: List[List[int]], 
              start: Optional[Tuple[int, int]] = None, 
              end: Optional[Tuple[int, int]] = None,
              path: Optional[List[Tuple[int, int]]] = None,
              traps: Optional[Set[Tuple[int, int]]] = None) -> Tuple[plt.Figure, plt.Axes]: # ===== 新增 traps 參數 =====
    
    if not maze or not maze[0]:
        raise ValueError("迷宮資料不可為空")

    height = len(maze)
    width = len(maze[0])
    
    fig, ax = plt.subplots(figsize=(width/3, height/3))

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

    # ===== 新增：繪製尖刺陷阱 =====
    if traps:
        for r, c in traps:
            center_x = c + 0.5
            center_y = height - r - 0.5
            # 畫一個大大的灰色叉叉代表尖刺陷阱 (設定 linestyle='None' 避免連線)
            ax.plot(center_x, center_y, marker='X', markersize=12, color='dimgray', linestyle='None')

    # 繪製解答路徑
    if path:
        path_x = [col + 0.5 for row, col in path]
        path_y = [height - row - 0.5 for row, col in path]
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
    return fig, ax
                  
def plot_path(maze, path, fig, ax, speed_ms: int = 100):
    height = len(maze)

    adjusted_path = [(x+0.5, height-y-0.5) for y, x in path]
    x_data, y_data = zip(*adjusted_path)

    def init():
        line.set_data([], [])
        head.set_data([], [])
        return line, head

    def update(num):
        # 1. 更新走過的軌跡線
        line.set_data(x_data[:num+1], y_data[:num+1])
        
        # 2. 更新最前端的探路者 (只顯示在最新的一格)
        head.set_data([x_data[num]], [y_data[num]])

        # 3. 根據移動方向，改變三角形的朝向
        if num > 0:
            dx = x_data[num] - x_data[num-1]
            dy = y_data[num] - y_data[num-1]
            if dx > 0:
                head.set_marker('>') # 往右
            elif dx < 0:
                head.set_marker('<') # 往左
            elif dy > 0:
                head.set_marker('^') # 往上
            elif dy < 0:
                head.set_marker('v') # 往下
        else:
            # 剛出發的第一步，先給一個圓點
            head.set_marker('o') 

        return line, head

    # 繪製走過的軌跡 (藍色半透明線)
    line, = ax.plot([], [], color='blue', lw=4, alpha=0.6)
    
    # 繪製最前端的三角形 (橘色大標記，設定 linestyle='None' 避免畫出多餘的線)
    head, = ax.plot([], [], color='darkorange', markersize=14, linestyle='None')
    
    ani = animation.FuncAnimation(
        fig, update, frames=len(path), init_func=init,
        interval=speed_ms, blit=True, repeat=False
    )
    
    return fig, ax, ani



                  

