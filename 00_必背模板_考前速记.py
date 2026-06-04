"""
============================================================
蓝桥杯 Python 国赛 必背模板 —— 考前48小时速记
江西赛区 Python 高职组（C组）| 2026.6.6
============================================================
背熟这 10 个模板，覆盖 70% 的题目！
"""

# ============================================================
# 一、输入输出提速（每道编程题第一行就写）
# ============================================================
import sys
sys.setrecursionlimit(500000)  # 递归深度，DFS必备
input = sys.stdin.readline      # 比 input() 快10倍

# 读整数
n = int(input())
# 读一行多个整数
a, b, c = map(int, input().split())
# 读数组
arr = list(map(int, input().split()))
# 读n行
data = [int(input()) for _ in range(n)]


# ============================================================
# 二、DFS / BFS 搜索框架（考得最多！）
# ============================================================

# --- DFS 模板（连通块、路径搜索）---
def dfs(x, y):
    # 越界/障碍/已访问 → 返回
    if x < 0 or x >= n or y < 0 or y >= m:
        return
    if grid[x][y] != 1 or visited[x][y]:
        return
    visited[x][y] = True
    # 四个方向
    for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
        dfs(x + dx, y + dy)


# --- BFS 模板（最短路径、最少步数）---
from collections import deque

def bfs(start_x, start_y):
    q = deque()
    q.append((start_x, start_y, 0))  # (x, y, 步数)
    visited = [[False] * m for _ in range(n)]
    visited[start_x][start_y] = True

    while q:
        x, y, step = q.popleft()
        # 到达终点
        if x == target_x and y == target_y:
            return step
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if not visited[nx][ny] and grid[nx][ny] == 0:
                    visited[nx][ny] = True
                    q.append((nx, ny, step + 1))
    return -1  # 无法到达


# ============================================================
# 三、动态规划（DP）—— 必考！
# ============================================================

# --- 0/1 背包 ---
# 容量 W，n 件物品，重量 w[i]，价值 v[i]
def knapsack_01(W, w, v):
    n = len(w)
    dp = [0] * (W + 1)
    for i in range(n):
        for j in range(W, w[i] - 1, -1):  # 倒序！
            dp[j] = max(dp[j], dp[j - w[i]] + v[i])
    return dp[W]


# --- 完全背包（每件物品无限个）---
def knapsack_complete(W, w, v):
    n = len(w)
    dp = [0] * (W + 1)
    for i in range(n):
        for j in range(w[i], W + 1):  # 正序！
            dp[j] = max(dp[j], dp[j - w[i]] + v[i])
    return dp[W]


# --- 最长公共子序列（LCS）---
def lcs(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[n][m]


# --- 最长递增子序列（LIS）---
import bisect
def lis(arr):
    tails = []
    for x in arr:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


# ============================================================
# 四、图论 —— 最短路必考
# ============================================================

# --- Dijkstra 堆优化（单源最短路）---
import heapq

def dijkstra(start, graph):  # graph: 邻接表 [(邻接点, 边权), ...]
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    pq = [(0, start)]  # (距离, 节点)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


# --- Floyd（多源最短路，n ≤ 300）---
def floyd(n, edges):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
        dist[v][u] = min(dist[v][u], w)  # 无向图
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


# ============================================================
# 五、并查集 —— 连通性问题
# ============================================================
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # 路径压缩
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[px] = py


# ============================================================
# 六、数学工具函数
# ============================================================
import math

# --- 快速幂 (a^b mod m) ---
def fast_pow(a, b, mod):
    res = 1
    while b:
        if b & 1:
            res = res * a % mod
        a = a * a % mod
        b >>= 1
    return res

# --- 素数筛（埃氏筛，1~n内所有素数）---
def get_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return primes, is_prime

# --- GCD 和 LCM ---
def gcd(a, b):
    return math.gcd(a, b)

def lcm(a, b):
    return a // math.gcd(a, b) * b

# --- 组合数 C(n, k) ---
def nCr(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    res = 1
    for i in range(k):
        res = res * (n - i) // (i + 1)
    return res


# ============================================================
# 七、常用内置库速查
# ============================================================
from collections import Counter      # 统计频率：Counter([1,2,1,3,1])
from collections import defaultdict  # 默认值字典：defaultdict(int)
from collections import deque        # 双端队列：q.append(), q.popleft()
from itertools import permutations   # 排列：permutations([1,2,3], 2)
from itertools import combinations   # 组合：combinations([1,2,3], 2)
from itertools import accumulate     # 前缀和：list(accumulate(arr))
import bisect                        # 二分：bisect_left(arr, x)
import heapq                         # 堆：heapq.heappush(pq, x)


# ============================================================
# 八、常用技巧速查
# ============================================================

# --- 前缀和（一维）---
def prefix_sum(arr):
    pre = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        pre[i+1] = pre[i] + arr[i]
    # 区间 [l, r] 的和 = pre[r+1] - pre[l]
    return pre

# --- 差分数组（区间加减）---
def difference(arr):
    diff = [0] * (len(arr) + 1)
    # [l, r] 区间加 x:
    # diff[l] += x; diff[r+1] -= x
    return diff

# --- 二分查找 ---
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# --- 二分答案模板 ---
def check(mid):
    # 判断 mid 是否可行，返回 True/False
    pass

def binary_answer():
    left, right = 0, 10**9  # 答案范围
    while left < right:
        mid = (left + right) // 2
        if check(mid):
            right = mid  # 可行，尝试更小
        else:
            left = mid + 1  # 不可行，需要更大
    return left


# =============================================================
# 九、考场"救命"技巧
# =============================================================
"""
1. 填空题不写代码！用 Excel / Windows计算器 / 简单 Python 脚本算
2. 判断质数：如果 n <= 10^6，直接用素数筛；> 10^6 用试除法 O(sqrt(n))
3. 大数运算：Python 自动支持大整数，不需要担心溢出！
4. 取模技巧：求个位数 = %10，求最后两位 = %100，求最后k位 = %(10**k)
5. 斐波那契/序列取模 → 必存在周期（Pisano周期），用 while 找周期
6. 排列组合问题 → from itertools import permutations, combinations
7. 正则匹配 → import re
8. 日期计算 → import datetime
9. n <= 10 → 全排列暴力
   n <= 100 → O(n^3) 可过
   n <= 10^5 → O(n log n) 可过
   n <= 10^6 → O(n) 可过
   更大 → 必须 O(log n) 或 O(1)
"""
