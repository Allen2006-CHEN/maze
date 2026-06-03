import random
from typing import List

def generate_maze(width: int, height: int) -> List[List[int]]:
    """
    使用深度優先搜尋法 (DFS) 生成隨機迷宮。
    
    回傳的二維陣列編碼：
    1: 有右牆
    2: 有底牆
    3: 有右牆與底牆
    0: 沒有右牆與底牆
    """
    # 初始狀態：每個格子都有一道右牆(1)和一道底牆(2)，所以數值都是 3
    maze = [[3 for _ in range(width)] for _ in range(height)]
    # 用來記錄哪些格子已經走訪過
    visited = [[False for _ in range(width)] for _ in range(height)]

    # 定義移動方向：上、下、左、右 (row變化, col變化)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def break_wall(r1: int, c1: int, r2: int, c2: int):
        """鑿穿 (r1, c1) 與 (r2, c2) 之間的牆壁"""
        if r2 == r1 - 1:    # 往上走：打掉上面那格的底牆 (~2 代表清空底牆位元)
            maze[r2][c2] &= ~2
        elif r2 == r1 + 1:  # 往下走：打掉自己這格的底牆
            maze[r1][c1] &= ~2
        elif c2 == c1 - 1:  # 往左走：打掉左邊那格的右牆 (~1 代表清空右牆位元)
            maze[r2][c2] &= ~1
        elif c2 == c1 + 1:  # 往右走：打掉自己這格的右牆
            maze[r1][c1] &= ~1

    # 使用 Stack (堆疊) 來實作 DFS 走訪
    stack = [(0, 0)]
    visited[0][0] = True

    while stack:
        # 取出目前所在的格子 (但不從堆疊中移除)
        r, c = stack[-1]
        
        # 尋找四周還沒走訪過的鄰居
        unvisited_neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # 確認鄰居在邊界內，且還沒被走訪過
            if 0 <= nr < height and 0 <= nc < width and not visited[nr][nc]:
                unvisited_neighbors.append((nr, nc))

        if unvisited_neighbors:
            # 如果有沒走訪過的鄰居，隨機挑選一個
            nr, nc = random.choice(unvisited_neighbors)
            break_wall(r, c, nr, nc) # 打破牆壁
            visited[nr][nc] = True   # 標記為已走訪
            stack.append((nr, nc))   # 將鄰居加入堆疊，下一步從它開始走
        else:
            # 如果四周都走過了 (死胡同)，就退回上一步
            stack.pop()

    return maze
