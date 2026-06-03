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

def a_star(graph, start_y, start_x, target_y, target_x):
    n = len(graph)
    m = len(graph[0])
    ways = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    min_cost = [[float('inf')]*m for _ in range(n)]
    min_cost[start_y][start_x] = 0

    prev = [[None]*m for _ in range(n)]
    heap = [(0, 0, start_y, start_x)]

    while heap:
        _, past_cost, y, x = heapq.heappop(heap)

        if y==target_y and x==target_x:
            break
        
        past_cost += 1
        for i, j in ways:
            nxt_y = y+i
            nxt_x = x+j
            if nxt_y<0 or nxt_x<0 or nxt_y==n or nxt_x==m:
                continue
            if barrier(graph, y, x, i, j):
                continue

            if past_cost < min_cost[nxt_y][nxt_x]:
                min_cost[nxt_y][nxt_x] = past_cost
                prev[nxt_y][nxt_x] = (y, x)
                # 這裡幫你修正了 target_y 與 target_x 的傳入順序
                tot_cost = future_cost(nxt_y, nxt_x, target_y, target_x) + past_cost
                heapq.heappush(heap, (tot_cost, past_cost, nxt_y, nxt_x))

    curr_y = target_y
    curr_x = target_x
    path = [(curr_y, curr_x)]
    while prev[curr_y][curr_x] != None:
        curr_y, curr_x = prev[curr_y][curr_x]
        path.append((curr_y, curr_x))
    path.reverse()

    return path