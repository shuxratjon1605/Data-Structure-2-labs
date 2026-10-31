# Student name: Shuxratjon Jamshedov   Student ID: 5282959
# Data Structures 2 | Fall 2026 | Graph Algorithms Lab: BFS, DFS, Dijkstra
# Queue and stack are written by hand (array + indexes). No graph library is used.

INF = 10**9  # "infinity"

# ---------------------------------------------------------------
# Graph 1 (no weights). Letters -> numbers: A=0, B=1, ...
# ---------------------------------------------------------------
names1 = list("ABCDEFG")
edges1 = [("A","B"),("A","C"),("B","D"),("B","E"),("C","F"),("E","F"),("F","G")]
idx1 = {n: i for i, n in enumerate(names1)}
adj1 = [[] for _ in names1]
for a, b in edges1:
    adj1[idx1[a]].append(idx1[b])
    adj1[idx1[b]].append(idx1[a])
for lst in adj1:
    lst.sort()  # neighbours in alphabetical order


# ===============================================================
# TASK 1: BFS
# ===============================================================
class Queue:
    """Array queue: front = where we take from, back = where we add (FIFO)."""
    def __init__(self, cap):
        self.data = [0] * cap
        self.front = 0
        self.back = 0
    def enqueue(self, x):            # add at the BACK
        self.data[self.back] = x
        self.back += 1
    def dequeue(self):               # take from the FRONT
        x = self.data[self.front]
        self.front += 1
        return x
    def empty(self):
        return self.front == self.back


def bfs(adj, start):
    n = len(adj)
    discovered = [False] * n
    dist = [INF] * n
    parent = [-1] * n
    order = []
    q = Queue(n)
    discovered[start] = True          # mark when ENQUEUED
    dist[start] = 0
    q.enqueue(start)
    while not q.empty():
        u = q.dequeue()               # take from the front of the queue
        order.append(u)               # visit
        for v in adj[u]:              # A -> Z
            if not discovered[v]:
                discovered[v] = True
                dist[v] = dist[u] + 1
                parent[v] = u
                q.enqueue(v)          # add at the back of the queue
    return order, dist, parent


def shortest(names, adj, s, t):
    _, dist, parent = bfs(adj, s)
    if dist[t] == INF:
        return f"Shortest {names[s]} -> {names[t]}: no path"
    path = []
    v = t
    while v != -1:                    # rebuild the path from the target back to the start
        path.append(names[v])
        v = parent[v]
    path.reverse()
    return f"Shortest {names[s]} -> {names[t]}: distance {dist[t]}, path " + " -> ".join(path)


print("=== Task 1: BFS ===")
order, _, _ = bfs(adj1, idx1["A"])
print("BFS order from A:", " ".join(names1[i] for i in order))
print(shortest(names1, adj1, idx1["A"], idx1["G"]))
print(shortest(names1, adj1, idx1["D"], idx1["G"]))


# ---------------------------------------------------------------
# TASK 1 - WRITTEN PART
# ---------------------------------------------------------------
# A. Hand trace (Graph 1, start A)
#   init   : queue = A
#   Step 1 : dequeue A, enqueue B, C      | queue: B C
#   Step 2 : dequeue B, enqueue D, E      | queue: C D E
#   Step 3 : dequeue C, enqueue F         | queue: D E F
#   Step 4 : dequeue D, nothing new       | queue: E F
#   Step 5 : dequeue E, nothing new       | queue: F
#   Step 6 : dequeue F, enqueue G         | queue: G
#   Step 7 : dequeue G, nothing new       | queue: empty
#   Visit order: A B C D E F G
#
# C. Short answers
#   1. A node is marked when it is enqueued so it can never be put in the queue
#      twice. If we marked at dequeue, a node reachable from several nodes of the
#      same level (e.g. F from C and E) would be enqueued several times, and the
#      dist/parent values could be overwritten or work duplicated.
#   2. Running time is O(V + E): each node is enqueued and dequeued once, and each
#      edge is examined a constant number of times (twice in an undirected graph).
#      BFS counts edges, not weights: the path with the fewest edges is not
#      necessarily the cheapest one. E.g. in Graph 2, A-C-E has 2 edges but costs
#      12, while A-C-B-D-E has 4 edges and costs only 10.


# ===============================================================
# TASK 2: DFS (iterative, explicit stack)
# ===============================================================
class Stack:
    """Array stack: one position top (LIFO)."""
    def __init__(self, cap):
        self.data = [0] * cap
        self.top = 0
    def push(self, x):
        self.data[self.top] = x
        self.top += 1
    def pop(self):
        self.top -= 1
        return self.data[self.top]
    def empty(self):
        return self.top == 0


def dfs(adj, start):
    n = len(adj)
    visited = [False] * n
    order = []
    s = Stack(n * n + 1)              # a node can be in the stack more than once
    s.push(start)
    while not s.empty():
        u = s.pop()                   # take from the TOP of the stack
        if visited[u]:
            continue                  # second copy - skip it
        visited[u] = True             # mark when POPPED
        order.append(u)               # visit
        for v in reversed(adj[u]):    # Z -> A, so the alphabetically first comes out first
            if not visited[v]:
                s.push(v)
    return order


print("\n=== Task 2: DFS ===")
for st in ("A", "G"):
    o = dfs(adj1, idx1[st])
    print(f"DFS order from {st}:", " ".join(names1[i] for i in o))


# ---------------------------------------------------------------
# TASK 2 - WRITTEN PART
# ---------------------------------------------------------------
# A. Hand trace (Graph 1, start A)  - stack is written top first
#   init   : push A                        | stack: A
#   Step 1 : pop A, visit, push C, B       | stack: B C
#   Step 2 : pop B, visit, push E, D       | stack: D E C
#   Step 3 : pop D, visit, nothing pushed  | stack: E C
#   Step 4 : pop E, visit, push F          | stack: F C
#   Step 5 : pop F, visit, push G, C       | stack: C G C
#   Step 6 : pop C, visit, nothing pushed  | stack: G C
#   Step 7 : pop G, visit, nothing pushed  | stack: C
#   Step 8 : pop C, already visited, skip  | stack: empty
#   Visit order: A B D E F C G
#
# C. Short answers
#   1. A node is marked only when popped, so while it is still waiting in the
#      stack another node can push it again. Here C is pushed in step 1 (from A)
#      and again in step 5 (from F). The second copy is popped and skipped in
#      step 8.
#   2. BFS: A B C D E F G (level by level). DFS: A B D E F C G (goes deep first,
#      then backtracks). The difference is explained by the data structure: BFS
#      uses a queue (FIFO), DFS uses a stack (LIFO).


# ===============================================================
# TASK 3: Dijkstra (Graph 2, weighted)
# ===============================================================
names2 = list("ABCDEF")
edges2 = [("A","B",4),("A","C",2),("B","C",1),("B","D",5),("C","D",8),
          ("C","E",10),("D","E",2),("D","F",6),("E","F",3)]
idx2 = {n: i for i, n in enumerate(names2)}
adj2 = [[] for _ in names2]
for a, b, w in edges2:
    adj2[idx2[a]].append((idx2[b], w))
    adj2[idx2[b]].append((idx2[a], w))
for lst in adj2:
    lst.sort()


def show(dist):
    return " ".join(f"{names2[i]}={'INF' if d >= INF else d}" for i, d in enumerate(dist))


def dijkstra(adj, source):
    n = len(adj)
    dist = [INF] * n
    prev = [-1] * n
    settled = [False] * n
    dist[source] = 0
    print("init |", show(dist))
    while True:
        # simple search for the minimum among unsettled nodes
        u = -1
        for i in range(n):
            if not settled[i] and dist[i] < INF and (u == -1 or dist[i] < dist[u]):
                u = i
        if u == -1:
            break
        settled[u] = True             # dist[u] is now final
        for v, w in adj[u]:
            if not settled[v] and dist[u] + w < dist[v]:   # relaxation
                dist[v] = dist[u] + w
                prev[v] = u
        print(f"settle {names2[u]} ({dist[u]}) |", show(dist))
    return dist, prev


print("\n=== Task 3: Dijkstra ===")
src = idx2["A"]
dist, prev = dijkstra(adj2, src)
for t in range(len(names2)):
    if t == src:
        continue
    path, v = [], t
    while v != -1:
        path.append(names2[v])
        v = prev[v]
    path.reverse()
    print(f"A to {names2[t]}: cost {dist[t]}: " + " -> ".join(path))


# ---------------------------------------------------------------
# TASK 3 - WRITTEN PART
# ---------------------------------------------------------------
# A. Hand trace (Graph 2, source A)
#   init   : A=0, B=INF, C=INF, D=INF, E=INF, F=INF
#   Step 1 : settle A (0)  -> B = 4 via A, C = 2 via A
#   Step 2 : settle C (2)  -> B = 3 via C, D = 10 via C, E = 12 via C
#   Step 3 : settle B (3)  -> D = 8 via B
#   Step 4 : settle D (8)  -> E = 10 via D, F = 14 via D
#   Step 5 : settle E (10) -> F = 13 via E
#   Step 6 : settle F (13) -> no updates
#
#   Node        A    B    C    D    E    F
#   Final dist  0    3    2    8    10   13
#   Final prev  -    C    A    B    D    E
#
# C. Short answers
#   1. Relaxation checks whether going through the just-settled node u gives a
#      cheaper route to v. In the line "settle C (2)": dist[C] + w(C,B) = 2 + 1 = 3
#      is less than the current dist[B] = 4, so dist[B] becomes 3 and prev[B]
#      becomes C.
#   2. Dijkstra settles a node when it has the smallest dist and assumes no later
#      path can be cheaper. With a negative edge a later path could be cheaper,
#      but the node is already settled and never updated, so the result can be
#      wrong. When every weight is 1, Dijkstra behaves like BFS: the node with the
#      smallest dist is exactly the next node of the BFS queue (nodes come out
#      level by level), and dist equals the number of edges.
