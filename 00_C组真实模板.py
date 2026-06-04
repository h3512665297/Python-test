"""
============================================================
蓝桥杯 Python C组（高职）国赛 必背模板
难度：基础为主，暴力为王！
============================================================
背熟前 6 个就够，后面4个看情况。
"""

import sys
sys.setrecursionlimit(500000)
input = sys.stdin.readline

# ============================================================
# ✅ 必考 1：枚举 + 暴力搜索
# C组最爱考！填空题基本就是暴力枚举
# ============================================================
from itertools import permutations, combinations

# 全排列暴力（n ≤ 10 直接用）
# for p in permutations(range(1, n+1)):
#     if 满足条件(p):
#         ans += 1

# 组合暴力
# for c in combinations(arr, k):
#     if 满足条件(c):
#         ans += 1

# 三重循环暴力（数字范围小的时候直接上）
# ans = 0
# for i in range(1, n+1):
#     for j in range(i+1, n+1):
#         for k in range(j+1, n+1):
#             if i+j+k == target:
#                 ans += 1


# ============================================================
# ✅ 必考 2：模拟题
# 题目说什么你就做什么，一步一步来
# ============================================================
def simulate():
    """模拟题的万能框架"""
    n = int(input())
    arr = list(map(int, input().split()))

    step = 0
    while True:
        # 按题目描述的规则操作数组
        # 例如：找最大值减1，找最小值加1
        changed = False
        for i in range(n):
            if 某个条件:
                # 执行操作
                changed = True
        if not changed:
            break
        step += 1
    print(step)


# ============================================================
# ✅ 必考 3：递归 + 记忆化
# 斐波那契不要用递归直接算！要么迭代，要么找周期
# ============================================================
from functools import lru_cache

# 记忆化递归（有记忆就不会爆栈）
@lru_cache(None)
def fib_memo(n):
    if n <= 1:
        return n
    return fib_memo(n-1) + fib_memo(n-2)

# 但！如果是斐波那契取某位，一定要找周期！
# 个位数 → 周期60
# 最后2位 → 周期300
# mod m → 周期 ≤ 6m


# ============================================================
# ✅ 必考 4：BFS（最短步数、最少次数）
# 这个还是会考的，但通常是最基础的迷宫
# ============================================================
from collections import deque

def bfs_basic(start, target):
    """一维 BFS：求最少步数"""
    q = deque([(start, 0)])
    visited = set([start])

    while q:
        pos, step = q.popleft()
        if pos == target:
            return step
        # 枚举所有可能的下一步
        for next_pos in [pos + 1, pos - 1, pos * 2]:  # 按题目规则改
            if next_pos not in visited and 0 <= next_pos <= 100000:
                visited.add(next_pos)
                q.append((next_pos, step + 1))
    return -1


# ============================================================
# ✅ 必考 5：基础 DP
# C组考 DP 最多考到 0/1 背包！不会考树形DP、状压DP
# ============================================================

# --- 0/1 背包（最重要，必须会）---
def knapsack(W, w, v):
    """W=容量, w=重量列表, v=价值列表"""
    dp = [0] * (W + 1)
    for i in range(len(w)):
        for j in range(W, w[i] - 1, -1):  # 倒序！
            dp[j] = max(dp[j], dp[j - w[i]] + v[i])
    return dp[W]

# --- 完全背包 ---
def knapsack_full(W, w, v):
    dp = [0] * (W + 1)
    for i in range(len(w)):
        for j in range(w[i], W + 1):  # 正序！
            dp[j] = max(dp[j], dp[j - w[i]] + v[i])
    return dp[W]

# --- 简单线性 DP（一维）---
def simple_dp(n):
    """爬楼梯 / 斐波那契"""
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# ============================================================
# ✅ 必考 6：数学基础
# GCD/LCM、素数、快速幂 —— 这三个C组常考
# ============================================================
import math

# GCD（最大公约数）
g = math.gcd(12, 18)  # 6

# LCM（最小公倍数）
l = a * b // math.gcd(a, b)

# 判断素数（试除法，O(√n)）
def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

# 素数筛（求 1~n 的所有素数）
def sieve(n):
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, n+1, i):
                is_p[j] = False
    return [i for i in range(n+1) if is_p[i]]

# 快速幂（求 a^b % mod）
def fast_pow(a, b, mod):
    res = 1
    while b:
        if b & 1:
            res = res * a % mod
        a = a * a % mod
        b >>= 1
    return res


# ============================================================
# ⚠️ 以下内容 C组大概率不考，了解即可
# ============================================================

# --- 前缀和（可能考，很简单）---
def prefix_sum(arr):
    pre = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        pre[i+1] = pre[i] + arr[i]
    return pre  # 区间[l, r]和 = pre[r+1] - pre[l]

# --- 二分查找 ---
import bisect
# pos = bisect.bisect_left(arr, target)  # 第一个 >= target 的位置

# --- 贪心：区间调度（可能考）---
def max_meetings(intervals):
    intervals.sort(key=lambda x: x[1])  # 按结束时间排序
    count, last = 0, -1
    for s, e in intervals:
        if s >= last:
            count += 1
            last = e
    return count

# --- Floyd（n≤100 的最短路，偶尔考）---
def floyd_small(n, edges):
    INF = 10**9
    dist = [[INF]*n for _ in range(n)]
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
# 🎯 C组终极口诀
# ============================================================
"""
1. 填空题 → 用 Python 暴力算！不要手算！
2. 不会做 → 先写暴力，O(n²) 也能过 30% 测试点
3. 做不出 → print(0) 或 print(-1)，不留白卷
4. 字符串题 → Python 是神，切片/正则/in/find/join/split 随便用
5. 日期题 → datetime 模块直接算，不要自己写逻辑
6. 数字太大 → 找周期！找规律！有限状态必循环
7. 递归太深 → 改迭代！或者加 @lru_cache
8. 输入多 → sys.stdin.readline，别用 input()
"""
