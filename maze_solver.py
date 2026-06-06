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

    # 2. 只有一個 while 迴圈
    while heap:
        _, past_cost, y, x = heapq.heappop(heap)

        if y==target_y and x==target_x:
            break
        
        past_cost += 1
        for i, j in ways:
            nxt_y = y+i
            nxt_x = x+j
            
            # 邊界防守
            if nxt_y<0 or nxt_x<0 or nxt_y==n or nxt_x==m:
                continue
            # 牆壁防守
            if barrier(graph, y, x, i, j):
                continue
            # 關鍵新增：陷阱防守 (如果是陷阱，絕對不走！)
            if (nxt_y, nxt_x) in traps:
                continue

            # 更新最小成本與路徑
            if past_cost < min_cost[nxt_y][nxt_x]:
                min_cost[nxt_y][nxt_x] = past_cost
                prev[nxt_y][nxt_x] = (y, x)
                tot_cost = future_cost(nxt_y, nxt_x, target_y, target_x) + past_cost
                heapq.heappush(heap, (tot_cost, past_cost, nxt_y, nxt_x))

    curr_y = target_y
    curr_x = target_x
    
    # 3. 防呆機制：如果根本沒走到終點(被陷阱或牆壁封死)，就回傳空陣列
    if prev[curr_y][curr_x] is None and (curr_y != start_y or curr_x != start_x):
        return []

    # 4. 往前推導出路徑
    path = [(curr_y, curr_x)]
    while prev[curr_y][curr_x] != None:
        curr_y, curr_x = prev[curr_y][curr_x]
        path.append((curr_y, curr_x))
    path.reverse()

    return path

