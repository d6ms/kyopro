# ABC 035 D
# ナイーブなDijkstraは O(|V|^2) だが、優先度キューを使うと O(|E|log|V|) で解ける
# 報酬が最も大きい都市になるべく早く到達し、その後帰ると解釈 = 最短経路問題

from heapq import heappush, heappop
from math import isinf


class Edge(object):

    def __init__(self, src, dst, cost):
        self.src = src
        self.dst = dst
        self.cost = cost


class Dijkstra(object):

    def __init__(self, v_len, edges, start, directed=False):
        """
        ダイクストラ法で最短経路を求める。

        :param v_len: グラフのノード数 通常は|V|、1-indexedなグラフなら |V| + 1
        :param edges: グラフの構造
        :param start: 始点 単一視点最短経路問題として解くので必要
        :param directed: 有向グラフの場合True 隣接行列を対称行列にするかが変わる
        """

        # 隣接行列 (adjacency matrix)
        # adj[i][j] でi番目の頂点からj番目の頂点へのコストを示す パスがなければINF
        self._adj = [[float('inf') for _ in range(v_len)] for _ in range(v_len)]
        for e in edges:
            self._adj[e.src][e.dst] = e.cost
            if not directed:
                self._adj[e.dst][e.src] = e.cost
        self._dist = [float('inf') for i in range(v_len)]  # 始点から各頂点までの最短距離
        self._prev = [float('inf') for i in range(v_len)]  # 最短経路における，その頂点の前の頂点のIDを格納する

        self._solve(start)

    def _solve(self, start):
        # 「最短距離が確定した頂点」に隣接する点からBFSするにあたり、それをどう探すかが問題になる
        # 安直に実装すればここで O(|V|) かかってしまうが、優先度キューを使えば O(log|V|) になる
        self._dist[start] = 0
        q = list()
        heappush(q, (0, start))  # キューの要素は (始点から頂点v_iへの仮の距離, v_iのID)

        while len(q) != 0:
            c, src = heappop(q)
            if self._dist[src] < c:
                continue

            # 隣接行列から隣接するノードを全て調べる = BFS
            for dst in range(len(self._adj)):
                cost = self._adj[src][dst]
                if isinf(cost):
                    continue
                if self._dist[src] + cost < self._dist[dst]:
                    self._dist[dst] = self._dist[src] + cost
                    heappush(q, (self._dist[dst], dst))
                    self._prev[dst] = src

    def distance(self, goal):
        return self._dist[goal]

    def path(self, goal):
        path = list()
        path.append(goal)
        cursor = goal

        while not isinf(self._prev[cursor]):
            path.append(self._prev[cursor])
            cursor = self._prev[cursor]

        return list(reversed(path))


N, M, T = map(int, input().split())
A = list(map(int, input().split()))
edges = list()
edges_rev = list()
for _ in range(M):
    a, b, c = map(int, input().split())
    edges.append(Edge(a, b, c))
    edges_rev.append(Edge(b, a, c))
d = Dijkstra(N + 1, edges, 1, directed=True)
d_rev = Dijkstra(N + 1, edges_rev, 1, directed=True)

ans = 0
for i in range(1, N + 1):
    taizai_time = T - (d.distance(i) + d_rev.distance(i))
    if taizai_time < 0:
        continue
    ans = max(ans, A[i - 1] * taizai_time)

print(ans)
