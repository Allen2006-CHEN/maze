import heapq

def future_cost(y, x, target_y, target_x):
    return abs(y-target_y) + abs(x-target_x)

def barrier(graph, y, x, i, j):
    if i == 1:
        return graph[y][x] & 2
    if j == 1:
        return graph[y][x] & 1
    if i == -1:
        return graph[y-1][x] & 2
    return graph[y][x-1] & 1

def a_star(graph, start_y, start_x, target_y, target_x, traps=None):
    # 1. 確保 traps 有被正確初始化
    if traps is None:
        traps = set()
        
    n = len(graph)
    m = len(graph[0])
    ways = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    min_cost = [[float('inf')]*m for _ in range(n)]
    min_cost[start_y][start_x] = 0

    prev = [[None]*m for _ in range(n)]
    heap = [(0, 0, start_y, start_x)]

    # 2. 尋路主迴圈
    while heap:
        _, past_cost, y, x = heapq.heappop(heap)

        if y == target_y and x == target_x:
            break
        
        # ⚠️ 注意：這裡已經把原本的 past_cost += 1 刪掉了！
        for i, j in ways:
            nxt_y = y + i
            nxt_x = x + j
            
            # 邊界與牆壁防守 (不可跨越的障礙一樣要跳過)
            if nxt_y < 0 or nxt_x < 0 or nxt_y == n or nxt_x == m:
                continue
            if barrier(graph, y, x, i, j):
                continue
            
            # ==========================================
            # 3. 【核心修改】泥沼陷阱成本計算
            # ==========================================
            step_cost = 1  # 預設走平地，體力花費為 1
            
            if (nxt_y, nxt_x) in traps:
                step_cost = 1000  # 踩進泥沼，體力花費暴增為 15！
            
            new_cost = past_cost + step_cost # 計算走到下一格的總花費

            # 如果新的總花費比之前記錄的還要小，就更新並加入排程
            if new_cost < min_cost[nxt_y][nxt_x]:
                min_cost[nxt_y][nxt_x] = new_cost
                prev[nxt_y][nxt_x] = (y, x)
                tot_cost = future_cost(nxt_y, nxt_x, target_y, target_x) + new_cost
                heapq.heappush(heap, (tot_cost, new_cost, nxt_y, nxt_x))

    curr_y = target_y
    curr_x = target_x
    
    # 4. 防呆機制：如果真的被「牆壁」完全封死(沒有路)才回傳空陣列
    if prev[curr_y][curr_x] is None and (curr_y != start_y or curr_x != start_x):
        return []

    # 5. 往前推導出路徑
    path = [(curr_y, curr_x)]
    while prev[curr_y][curr_x] is not None:
        curr_y, curr_x = prev[curr_y][curr_x]
        path.append((curr_y, curr_x))
    path.reverse()

    return path

