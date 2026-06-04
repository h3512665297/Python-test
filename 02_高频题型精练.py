"""
============================================================
蓝桥杯 Python C组 国赛 高频题型精练（附答案）
考试前一天过一遍，重点看懂思路！
============================================================
"""

# ============================================================
# 题型1：找周期/找规律
# 真题：斐波那契与7（2022国赛A题）
# ============================================================
"""
关键思想：有限状态必然产生循环！
- 斐波那契的个位数 → 周期60
- 斐波那契 mod m → 周期不超过 6m
- 找周期的方法：while True 跑，找到循环起点
"""
def fibonacci_period(mod):
    """找斐波那契数列对 mod 取模的周期"""
    a, b = 0, 1
    for period in range(1, mod * mod + 1):
        a, b = b, (a + b) % mod
        if a == 0 and b == 1:
            return period
    return -1

# print(fibonacci_period(10))  # 60（个位数周期）
# print(fibonacci_period(100)) # 300（后两位周期）


# ============================================================
# 题型2：取模与鸽巢原理
# 真题：取模（2022国赛C题）
# ============================================================
"""
题目：判断是否存在 1 ≤ x < y ≤ m，使得 n % x == n % y
关键：当 m > n 时，由鸽巢原理必然存在 → 直接 Yes
"""
def solve_mod(t, queries):
    """queries: [(n, m), ...]"""
    results = []
    for n, m in queries:
        if m > n:
            results.append("Yes")  # 鸽巢原理
            continue
        found = False
        # m ≤ n 时暴力（范围不大）
        seen = set()
        for x in range(1, m + 1):
            r = n % x
            if r in seen:
                found = True
                break
            seen.add(r)
        results.append("Yes" if found else "No")
    return results


# ============================================================
# 题型3：BFS 最短路径
# ============================================================
"""
最经典的迷宫问题变种：
- 二维迷宫 → 标准 BFS
- 一维跳格子 → BFS（每个位置有跳跃规则）
- 最少次数/最少步数 → 一定是 BFS！
"""
from collections import deque

def maze_bfs(grid, start, end):
    """二维迷宫 BFS，0可走1是墙"""
    n, m = len(grid), len(grid[0])
    q = deque([(start[0], start[1], 0)])
    visited = [[False] * m for _ in range(n)]
    visited[start[0]][start[1]] = True

    while q:
        x, y, step = q.popleft()
        if (x, y) == end:
            return step
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if not visited[nx][ny] and grid[nx][ny] == 0:
                    visited[nx][ny] = True
                    q.append((nx, ny, step + 1))
    return -1


# ============================================================
# 题型4：贪心（简单但高频）
# ============================================================
"""
常见贪心策略：
- 区间问题 → 按右端点排序
- 排队打水 → 按时间排序（小的先打）
- 合并果子 → 用小根堆 heapq
"""
def max_intervals(intervals):
    """最多不重叠区间数（按右端点排序）"""
    intervals.sort(key=lambda x: x[1])  # 按右端点排序
    count = 0
    last_end = -float('inf')
    for start, end in intervals:
        if start >= last_end:
            count += 1
            last_end = end
    return count


# ============================================================
# 题型5：前缀和（把 O(n*m) 优化到 O(1)）
# ============================================================
def range_sum(arr, queries):
    """arr 查询 [l, r] 区间和，queries = [(l1, r1), ...]"""
    n = len(arr)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + arr[i]

    res = []
    for l, r in queries:
        res.append(pre[r + 1] - pre[l])  # O(1) 查询！
    return res


# ============================================================
# 题型6：素数/质数问题
# ============================================================
def is_prime(n):
    """试除法判断素数，O(sqrt(n))"""
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def sieve(n):
    """埃氏筛，[1, n] 内所有素数，n ≤ 10^7 可用"""
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return [i for i in range(2, n + 1) if is_p[i]], is_p


# ============================================================
# 题型7：排列组合（itertools 一句话搞定）
# ============================================================
from itertools import permutations, combinations, combinations_with_replacement

# 全排列：permutations([1,2,3]) → (1,2,3), (1,3,2), (2,1,3), ...
# 组合(不重复)：combinations([1,2,3], 2) → (1,2), (1,3), (2,3)
# 组合(可重复)：combinations_with_replacement([1,2,3], 2)
# 笛卡尔积：product([1,2], [3,4]) → (1,3), (1,4), (2,3), (2,4)

# 全排列暴力枚举（n ≤ 10 时直接用）
def permute_brute(arr):
    """用全排列暴力验证某个条件"""
    ans = []
    for p in permutations(arr):
        # 检查 p 是否满足条件
        # if check(p):
        #     ans.append(p)
        pass
    return ans


# ============================================================
# 题型8：日期问题（datetime 模块救命）
# ============================================================
from datetime import date, timedelta

def count_dates(start, end):
    """统计从 start 到 end 之间满足条件的日期数"""
    # start = date(2000, 1, 1), end = date(2020, 12, 31)
    cnt = 0
    current = start
    while current <= end:
        # 条件示例：日期是回文 date(2020, 2, 2) → 20200202
        s = current.strftime("%Y%m%d")
        if s == s[::-1]:  # 回文判断
            cnt += 1
        current += timedelta(days=1)
    return cnt


# ============================================================
# 题型9：简单 DP（线性DP + 背包DP）
# ============================================================

# --- 爬楼梯（基础中的基础）---
def climb_stairs(n):
    """每次爬 1 或 2 级，n 级台阶有多少种爬法"""
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

# --- 打家劫舍（不能选相邻元素）---
def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    return dp[-1]


# ============================================================
# 题型10：Floyd 最短路（n ≤ 300 直接用）
# ============================================================
def floyd_example(n, edges):
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
        dist[v][u] = min(dist[v][u], w)  # 无向图
    # 三重循环
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


# ============================================================
# ⚠️ 终极提醒：Python 竞赛避坑
# ============================================================
"""
❌ 用 input() 读大量数据 → 太慢！
✅ 用 sys.stdin.readline

❌ 递归不设深度 → 稍微深一点就 RE！
✅ sys.setrecursionlimit(500000)

❌ 用 list 动态 append 上百万次 → 很慢！
✅ 预分配 list = [0] * n

❌ 用 float 做精确比较 → 精度问题！
✅ 用 int 运算，比如比较 a/b > c/d 写成 a*d > c*b

❌ 直接暴力算天文数字 → Python 大整数也扛不住时间！
✅ 找周期、取模、找规律

❌ print 在循环里每行都输出 → 慢！
✅ 收集到 list 然后用 '\n'.join() 一次性输出
"""
