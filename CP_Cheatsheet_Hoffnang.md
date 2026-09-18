# Competitive Programming Reference Guide & Cheatsheet

**Team:** Hoffnang  
**Contestant:** Soyebuzaman Naim  
**Affiliation:** Southeast University (SEU CS Carnival 2026)  
**Standard:** C++17 / Fast I/O / 64-bit Int  

---

> [!IMPORTANT]
> **About this Notebook:**
> This document is designed for the **25-page competition notebook limit**. Every section includes:
> - 📌 **When to Use & Purpose**
> - ⏱️ **Time & Space Complexity**
> - ⚠️ **Key Traps & Constraints (e.g. 1LL overflow, 1-indexed vs 0-indexed)**
> - ⌨️ **VS Code Snippet Trigger Prefix** (matching your personal snippet library)

---

## Table of Contents
1. [Section 1: Contest Setup & Fast I/O](#section-1-contest-setup--fast-io)
2. [Section 2: C++ Basics & STL Essentials](#section-2-c-basics--stl-essentials)
3. [Section 3: Math, Number Theory & Bit Manipulation](#section-3-math-number-theory--bit-manipulation)
4. [Section 4: Graph Representations & Traversals](#section-4-graph-representations--traversals)
5. [Section 5: Shortest Paths & Negative Cycles](#section-5-shortest-paths--negative-cycles)
6. [Section 6: Tree Algorithms](#section-6-tree-algorithms)
7. [Section 7: Data Structures (DSU, Fenwick & Segment Tree)](#section-7-data-structures-dsu-fenwick--segment-tree)
8. [Section 8: String Algorithms (KMP)](#section-8-string-algorithms-kmp)
9. [Section 9: Search Paradigms & Dynamic Programming](#section-9-search-paradigms--dynamic-programming)
10. [Section 10: Advanced Tools (Kruskal, Matrix Power & Geometry)](#section-10-advanced-tools-kruskal-matrix-power--geometry)

---

# Section 1: Contest Setup & Fast I/O

### 1.1 Fast I/O Contest Template
- **Trigger Prefix:** `cpp`
- **When to use:** Starter boilerplate for every problem.
- **Why:** `cin.tie(nullptr)` and `sync_with_stdio(false)` speed up I/O by ~10x. `#define int long long` eliminates 32-bit overflow errors on variable declarations.
```cpp
#include <bits/stdc++.h>
using namespace std;

#define int long long
#define endl '\n'
#define all(x) (x).begin(), (x).end()
#define rall(x) (x).rbegin(), (x).rend()
#define sz(x) (int)(x).size()

void fast_io() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
}

signed main() {
    fast_io();

    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> v(n);
        for (int &x : v)
            cin >> x;
    }
}
```

---

# Section 2: C++ Basics & STL Essentials

### 2.1 Primitive Types, Overflow Prevention & Float Comparisons
| Type | Bytes | Range | Key Rule |
|---|---|---|---|
| `int` | 4 | $\approx [-2 \cdot 10^9, 2 \cdot 10^9]$ | Default array indexing, sizes |
| `long long` | 8 | $\approx [-9 \cdot 10^{18}, 9 \cdot 10^{18}]$ | Required for sums, factorials, products |
| `double` | 8 | 15–17 decimal digits | Compare using `fabs(a - b) < 1e-9` |

```cpp
// 1. Preventing Integer Overflow
int a = 1e6, b = 1e6;
long long ans = 1LL * a * b; // 1LL forces 64-bit calculation!

// 2. Safe Floating Point Equality
const double EPS = 1e-9;
bool are_equal(double a, double b) { return fabs(a - b) < EPS; }

// 3. Fixed Precision Print
cout << fixed << setprecision(9) << ans << "\n";
```

### 2.2 Standard Library Containers
```cpp
// Vector (Dynamic Array)
vector<int> v; v.push_back(10); v.pop_back(); int sz = v.size();

// Set (Strictly unique, ascending order, O(log N))
set<int> s; s.insert(5); s.erase(5); bool has = s.count(5);
int min_val = *s.begin(), max_val = *s.rbegin();

// Multiset (Allows duplicates, ascending order, O(log N))
multiset<int> ms; ms.insert(5); ms.insert(5);
ms.erase(ms.find(5)); // Erases ONLY ONE 5! (ms.erase(5) deletes ALL 5s)

// Map (Key-Value associative map, O(log N))
map<string, int> mp; mp["team"] = 1;
for (auto &[k, val] : mp) { /* sorted iteration */ }

// Heaps / Priority Queue: O(log N) push/pop, O(1) top
priority_queue<int> max_heap; // largest on top
priority_queue<int, vector<int>, greater<int>> min_heap; // smallest on top
```

### 2.3 `<algorithm>` Essentials
```cpp
vector<int> a = {5, 2, 8, 1, 9};

// 1. Sort O(N log N)
sort(all(a));                  // Ascending: {1, 2, 5, 8, 9}
sort(rall(a));                 // Descending: {9, 8, 5, 2, 1}

// 2. Binary Search on Sorted Arrays: O(log N)
auto it1 = lower_bound(all(a), 5); // first element >= 5
int idx1 = it1 - a.begin();        // convert iterator to index
auto it2 = upper_bound(all(a), 5); // first element > 5

// 3. Deduplication (Coordinate Compression)
sort(all(a));
a.erase(unique(all(a)), a.end());
```

---

# Section 3: Math, Number Theory & Bit Manipulation

### 3.1 Greatest Common Divisor (GCD)
- **Trigger Prefix:** `gcdf`
- **Time Complexity:** $O(\log(\min(a, b)))$
```cpp
int gcd(int a, int b) {
    while (b) {
        a %= b;
        swap(a, b);
    }
    return a;
}
```

### 3.2 Least Common Multiple (LCM)
- **Trigger Prefix:** `lcmf`
- **Time Complexity:** $O(\log(\min(a, b)))$
- **Safety:** Divides before multiplying to prevent premature integer overflow.
```cpp
int lcm(int a, int b) {
    if (a == 0 || b == 0) return 0;
    return a / __gcd(a, b) * b;
}
```

### 3.3 Sieve of Eratosthenes (Prime Generation)
- **Trigger Prefix:** `gprime`
- **Time Complexity:** $O(N \log \log N)$
- **Usage:** Precomputes all primes up to $N \approx 10^7$ in milliseconds.
```cpp
// ---------- SIEVE OF ERATOSTHENES ----------
vector<int> primes;
vector<bool> is_prime;

void gprime(int n) {
    is_prime.assign(n + 1, true);
    is_prime[0] = is_prime[1] = false;
    for (int i = 2; i * i <= n; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j <= n; j += i)
                is_prime[j] = false;
        }
    }
    primes.clear();
    for (int i = 2; i <= n; i++) {
        if (is_prime[i]) primes.push_back(i);
    }
}
```

### 3.4 Binary Exponentiation with Modulo ($a^b \pmod m$)
- **Trigger Prefix:** `binExpoMod`
- **Time Complexity:** $O(\log b)$
```cpp
long long binpow(long long a, long long b, long long m) {
    a %= m;
    long long res = 1;
    while (b > 0) {
        if (b & 1)
            res = res * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return res;
}
```

### 3.5 Binary Exponentiation Standard ($a^b$)
- **Trigger Prefix:** `binExpo`
- **Time Complexity:** $O(\log b)$
```cpp
long long binpow(long long a, long long b) {
    long long res = 1;
    while (b > 0) {
        if (b & 1)
            res = res * a;
        a = a * a;
        b >>= 1;
    }
    return res;
}
```

### 3.6 Count Total Set Bits (1s) from 0 to N
- **Trigger Prefix:** `numofonef`
- **Time Complexity:** $O(\log N)$
- **Purpose:** Counts the total number of set bits ('1's) across all integers in $[0, n]$.
```cpp
int numofone(int n)
{
    int ans = 0;
    for (int i = 0; (1ULL << i) <= n; i++)
    {
        int vag = 1ULL << (i + 1);
        int arektavag = (n + 1) / vag;
        ans += (arektavag * (vag >> 1ULL));
        int obos = (n + 1) % vag;
        if (obos > (vag >> 1ULL))
        {
            ans += ((obos) - (vag >> 1ULL));
        }
        if (arektavag == 0)
            break;
    }
    return ans;
}
```

### 3.7 Extended GCD & Modular Inverse
- **Time Complexity:** $O(\log(\min(a, b)))$
```cpp
pair<int, int> ext_gcd(int a, int b) {
    if (b == 0) return {1, 0};
    auto [x1, y1] = ext_gcd(b, a % b);
    return {y1, x1 - y1 * (a / b)};
}

int mod_inverse(int a, int m) {
    auto [x, y] = ext_gcd(a, m);
    return (x % m + m) % m;
}
```

---

# Section 4: Graph Representations & Traversals

### 4.1 Adjacency List Input
- **Trigger Prefix:** `adjlist`
- **Usage:** Input for general weighted graph with $V$ vertices and $E$ edges.
```cpp
int V, E;
cin >> V >> E;

// Adjacency list: adj[u] = vector of {v, weight}
vector<vector<pair<int, int>>> adj(V);

for (int i = 0; i < E; ++i) {
    int u, v, w;
    cin >> u >> v >> w;
    adj[u].push_back({v, w}); // for directed graph
    // adj[v].push_back({u, w}); // for undirected graph
}
```

### 4.2 Edge List Input
- **Trigger Prefix:** `adjmat`
```cpp
int V, E;
cin >> V >> E;

// Edge list: each edge is a vector of 3 integers {u, v, weight}
vector<vector<int>> edges;

for (int i = 0; i < E; ++i) {
    int u, v, w;
    cin >> u >> v >> w;
    edges.push_back({u, v, w});
}
```

### 4.3 DFS Traversal with Graph Input
- **Trigger Prefix:** `dfs`
- **Time Complexity:** $O(V + E)$
```cpp
void dfs(int node, const vector<int> adj[], vector<bool>& visited) {
    visited[node] = true;
    for (int neighbor : adj[node]) {
        if (!visited[neighbor]) {
            dfs(neighbor, adj, visited);
        }
    }
}

signed main() {
    int n, m; cin >> n >> m;
    vector<int> adj[n + 1];
    vector<bool> visited(n + 1, false);

    for (int i = 0; i < m; ++i) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u); // Remove if directed
    }

    for (int i = 1; i <= n; ++i) {
        if (!visited[i]) dfs(i, adj, visited);
    }
    return 0;
}
```

### 4.4 DFS Function Only
- **Trigger Prefix:** `dfsfunc`
```cpp
void dfs(int node, const vector<int> adj[], vector<bool>& visited) {
    visited[node] = true;
    for (int neighbor : adj[node]) {
        if (!visited[neighbor]) {
            dfs(neighbor, adj, visited);
        }
    }
}
```

### 4.5 BFS Traversal with Graph Input
- **Trigger Prefix:** `bfs`
- **Time Complexity:** $O(V + E)$
```cpp
void bfs(int start, const vector<int> adj[], vector<bool>& visited) {
    queue<int> q;
    q.push(start);
    visited[start] = true;

    while (!q.empty()) {
        int node = q.front(); q.pop();
        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }
}

signed main() {
    int n, m; cin >> n >> m;
    vector<int> adj[n + 1];
    vector<bool> visited(n + 1, false);

    for (int i = 0; i < m; ++i) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u); // Remove if directed
    }

    for (int i = 1; i <= n; ++i) {
        if (!visited[i]) bfs(i, adj, visited);
    }
}
```

### 4.6 BFS Function Only
- **Trigger Prefix:** `bfsfunc`
```cpp
void bfs(int start, const vector<int> adj[], vector<bool>& visited) {
    queue<int> q;
    q.push(start);
    visited[start] = true;

    while (!q.empty()) {
        int node = q.front(); q.pop();
        for (int neighbor : adj[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }
}
```

### 4.7 Topological Sort (Kahn's In-Degree BFS)
- **Time Complexity:** $O(V + E)$
- **Condition:** Graph must be a Directed Acyclic Graph (DAG).
```cpp
vector<int> topo_sort(int n, const vector<vector<int>> &adj) {
    vector<int> in_deg(n, 0), order;
    for (int u = 0; u < n; ++u)
        for (int v : adj[u]) in_deg[v]++;
    queue<int> q;
    for (int i = 0; i < n; ++i) if (in_deg[i] == 0) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (int v : adj[u])
            if (--in_deg[v] == 0) q.push(v);
    }
    return (order.size() == n) ? order : vector<int>(); // empty if cycle
}
```

---

# Section 5: Shortest Paths & Negative Cycles

### 5.1 Dijkstra's Algorithm (Priority Queue & Path Print)
- **Trigger Prefix:** `dijkstra`
- **Time Complexity:** $O((V + E) \log V)$
- **Constraint:** All edge weights must be non-negative ($w \ge 0$).
```cpp
int n, m; cin >> n >> m;
vector<vector<pair<int, int>>> adj(n + 1);
for (int i = 0; i < m; i++) {
    int u, v, w; cin >> u >> v >> w;
    adj[u].emplace_back(v, w);
    adj[v].emplace_back(u, w);
}
int s = 1, inf = LLONG_MAX / 2;
vector<int> dis(n + 1, inf), parent(n + 1, -1);
dis[s] = 0;
priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
pq.emplace(0, s);
while (!pq.empty()) {
    auto [dv, v] = pq.top(); pq.pop();
    if (dv > dis[v]) continue;
    for (auto &edge : adj[v]) {
        int to = edge.first, d = edge.second;
        if (dis[v] + d < dis[to]) {
            dis[to] = dis[v] + d;
            parent[to] = v;
            pq.emplace(dis[to], to);
        }
    }
}
if (dis[n] == inf) {
    cout << -1 << endl;
} else {
    vector<int> path;
    for (int i = n; i != -1; i = parent[i]) path.push_back(i);
    reverse(path.begin(), path.end());
    for (int node : path) cout << node << " ";
    cout << endl;
}
```

### 5.2 Dijkstra's Algorithm (Set-Based)
- **Trigger Prefix:** `dijkstraSet`
- **Time Complexity:** $O((V + E) \log V)$
```cpp
const int INF = 1000000000;
vector<vector<pair<int, int>>> adj;

void dijkstra(int s, vector<int> & d, vector<int> & p) {
    int n = adj.size();
    d.assign(n, INF);
    p.assign(n, -1);
    d[s] = 0;
    set<pair<int, int>> q;
    q.insert({0, s});
    while (!q.empty()) {
        int v = q.begin()->second;
        q.erase(q.begin());

        for (auto edge : adj[v]) {
            int to = edge.first, len = edge.second;
            if (d[v] + len < d[to]) {
                q.erase({d[to], to});
                d[to] = d[v] + len;
                p[to] = v;
                q.insert({d[to], to});
            }
        }
    }
}
```

### 5.3 Bellman-Ford Algorithm
- **Trigger Prefix:** `bellman_ford`
- **Time Complexity:** $O(V \cdot E)$
- **Capability:** Supports negative edge weights; detects negative cycle reachable from $S$.
```cpp
vector<int> bellman_ford(int n, vector<vector<int>>& edges, int S) {
    vector<int> dis(n, 1e9);
    dis[S] = 0;
    for (int i = 0; i < n - 1; i++) {
        bool updated = false;
        for (auto &e : edges) {
            int u = e[0], v = e[1], w = e[2];
            if (dis[u] != 1e9 && dis[u] + w < dis[v]) {
                dis[v] = dis[u] + w;
                updated = true;
            }
        }
        if (!updated) break;
    }
    // Check for negative cycle
    for (auto &e : edges) {
        int u = e[0], v = e[1], w = e[2];
        if (dis[u] != 1e9 && dis[u] + w < dis[v]) return {-1};
    }
    return dis;
}
```

### 5.4 Negative Cycle Detection & Path Reconstruction
- **Trigger Prefix:** `negcyclef`
- **Time Complexity:** $O(V \cdot E)$
- **Key Detail:** Steps back $N$ times (`x = p[x]`) to guarantee the pointer enters the cycle before printing.
```cpp
int n, m; cin >> n >> m;
vector<vector<int>> edges;
for (int i = 0; i < m; ++i) {
    int u, v, w; cin >> u >> v >> w;
    edges.push_back({u, v, w});
}
vector<int> dist(n + 1, 0), p(n + 1, -1);
int x;
for (int i = 0; i < n; i++) {
    x = -1;
    for (auto &edge : edges) {
        int u = edge[0], v = edge[1], w = edge[2];
        if (dist[u] + w < dist[v]) {
            dist[v] = dist[u] + w;
            p[v] = u;
            x = v;
        }
    }
}
if (x == -1) {
    cout << "NO" << endl;
    return 0;
}
for (int i = 0; i < n; i++) x = p[x];
cout << "YES" << endl;
vector<int> path;
int cur = x; path.push_back(cur);
while (true) {
    cur = p[cur];
    path.push_back(cur);
    if (cur == x) break;
}
reverse(all(path));
for (int node : path) cout << node << " ";
cout << endl;
```

### 5.5 Floyd-Warshall (All-Pairs Shortest Path)
- **Time Complexity:** $O(V^3)$ (Suitable for $N \le 500$)
```cpp
for (int k = 0; k < n; ++k)
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            if (dist[i][k] < INF && dist[k][j] < INF)
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
```

---

# Section 6: Tree Algorithms

### 6.1 Tree Diameter via Double BFS
- **Trigger Prefix:** `treeDiameter`
- **Time Complexity:** $O(V + E)$
- **Theorem:** An arbitrary BFS from node 1 finds node $u$ (one endpoint of diameter). A second BFS from $u$ finds node $v$ and the exact diameter length.
```cpp
pair<int, int> bfs_farthest(int start, const vector<vector<int>>& adj, int n) {
    vector<int> dist(n + 1, -1);
    queue<int> q;
    q.push(start);
    dist[start] = 0;
    int farthest_node = start;

    while (!q.empty()) {
        int node = q.front(); q.pop();
        for (int neighbor : adj[node]) {
            if (dist[neighbor] == -1) {
                dist[neighbor] = dist[node] + 1;
                q.push(neighbor);
                if (dist[neighbor] > dist[farthest_node])
                    farthest_node = neighbor;
            }
        }
    }
    return {farthest_node, dist[farthest_node]};
}

signed main() {
    fastIO();
    int n; cin >> n;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v); adj[v].push_back(u);
    }
    int far1 = bfs_farthest(1, adj, n).first;
    int diameter = bfs_farthest(far1, adj, n).second;
    cout << diameter << '\n';
}
```

---

# Section 7: Data Structures (DSU, Fenwick & Segment Tree)

### 7.1 Disjoint Set Union (Union by Size)
- **Trigger Prefix:** `dsu-size`
- **Time Complexity:** $O(\alpha(N)) \approx O(1)$ per operation
```cpp
// Union by size
class DisjointSet {
    vector<int> rank, parent, size;

public:
    DisjointSet(int n) {
        rank.resize(n + 1, 0);
        parent.resize(n + 1);
        size.resize(n + 1, 1);
        for (int i = 0; i <= n; i++) parent[i] = i;
    }

    int findUPar(int node) {
        if (node == parent[node]) return node;
        return parent[node] = findUPar(parent[node]);
    }

    void unionBySize(int u, int v) {
        int ulpU = findUPar(u), ulpV = findUPar(v);
        if (ulpU == ulpV) return;
        if (size[ulpU] < size[ulpV]) {
            parent[ulpU] = ulpV;
            size[ulpV] += size[ulpU];
        } else {
            parent[ulpV] = ulpU;
            size[ulpU] += size[ulpV];
        }
    }

    bool connected(int u, int v) {
        return findUPar(u) == findUPar(v);
    }
};
```

### 7.2 Fenwick Tree (Binary Indexed Tree / BIT)
- **Time Complexity:** $O(\log N)$ query and update, $O(N)$ memory.
```cpp
struct Fenwick {
    int n; vector<int> bit;
    Fenwick(int n) : n(n), bit(n + 1, 0) {}

    void add(int idx, int val) { // add val at index idx (1-based)
        for (; idx <= n; idx += idx & -idx) bit[idx] += val;
    }

    int query(int idx) { // prefix sum [1, idx]
        int sum = 0;
        for (; idx > 0; idx -= idx & -idx) sum += bit[idx];
        return sum;
    }

    int range_query(int l, int r) { return query(r) - query(l - 1); }
};
```

### 7.3 Iterative Segment Tree (Range Sum & Point Update)
- **Time Complexity:** $O(\log N)$ query and update
- **Advantage:** Non-recursive, zero recursion overhead, memory size $2N$.
```cpp
struct SegTree {
    int n; vector<int> t;
    SegTree(int n) : n(n), t(2 * n, 0) {}

    void update(int p, int val) {
        for (t[p += n] = val; p > 1; p >>= 1)
            t[p >> 1] = t[p] + t[p ^ 1];
    }

    int query(int l, int r) { // sum on interval [l, r] (0-indexed)
        int res = 0;
        for (l += n, r += n + 1; l < r; l >>= 1, r >>= 1) {
            if (l & 1) res += t[l++];
            if (r & 1) res += t[--r];
        }
        return res;
    }
};
```

---

# Section 8: String Algorithms (KMP)

### 8.1 Knuth-Morris-Pratt (KMP) Pattern Search
- **Trigger Prefix:** `kmp`
- **Time Complexity:** $O(N + M)$
- **Returns:** All 0-based match start positions of `pat` in `text`.
```cpp
// Preprocess pattern to build LPS array
vector<int> buildLPS(const string &pat) {
    int m = pat.size(), len = 0;
    vector<int> lps(m, 0);
    for (int i = 1; i < m;) {
        if (pat[i] == pat[len]) {
            len++; lps[i] = len; i++;
        } else {
            if (len != 0) len = lps[len - 1];
            else { lps[i] = 0; i++; }
        }
    }
    return lps;
}

// KMP search: find occurrences of pattern in text
vector<int> KMPsearch(const string &text, const string &pat) {
    int n = text.size(), m = pat.size();
    vector<int> lps = buildLPS(pat), positions;
    int i = 0, j = 0;
    while (i < n) {
        if (text[i] == pat[j]) {
            i++; j++;
            if (j == m) {
                positions.push_back(i - j); // match at i - m
                j = lps[j - 1];
            }
        } else {
            if (j != 0) j = lps[j - 1];
            else i++;
        }
    }
    return positions;
}
```

---

# Section 9: Search Paradigms & Dynamic Programming

### 9.1 Bitmasking Complete Search (Apple Division)
- **Trigger Prefix:** `bitMaskingAppleDivision`
- **Time Complexity:** $O(2^N \cdot N)$ (Feasible for $N \le 20$)
```cpp
int n; cin >> n;
vector<int> v(n);
for (int &x : v) cin >> x;

int ans = LLONG_MAX;
for (int i = 0; i < (1 << n); i++) {
    int a = 0, b = 0;
    for (int pos = 0; pos < n; pos++) {
        if (i & (1 << pos)) a += v[pos];
        else b += v[pos];
    }
    ans = min(ans, llabs(a - b));
}
cout << ans << endl;
```

### 9.2 Two Pointers Merge of Two Sorted Lists
- **Trigger Prefix:** `twoPointer`
- **Time Complexity:** $O(N + M)$
```cpp
vector<int> a(n), b(m), c;
for (int &x : a) cin >> x;
for (int &x : b) cin >> x;

int i = 0, j = 0;
while (i < n || j < m) {
    while ((i < n) && (j >= m || (a[i] <= b[j]))) {
        c.push_back(a[i]); i++;
    }
    while ((j < m) && (i >= n || b[j] <= a[i])) {
        c.push_back(b[j]); j++;
    }
}
```

### 9.3 0-1 Knapsack & Unbounded Knapsack
- **Time Complexity:** $O(N \cdot W)$ with $O(W)$ space.
```cpp
// 0-1 Knapsack (each item at most once)
int knapsack_01(int W, const vector<int>& wt, const vector<int>& val, int n) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < n; i++)
        for (int w = W; w >= wt[i]; w--) // BACKWARDS
            dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
    return dp[W];
}

// Unbounded Knapsack: change loop to: for (int w = wt[i]; w <= W; w++)
```

### 9.4 Longest Increasing Subsequence ($O(N \log N)$)
```cpp
int lis(const vector<int>& a) {
    vector<int> tails;
    for (int x : a) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    return tails.size();
}
```

---

# Section 10: Advanced Tools (Kruskal, Matrix Power & Geometry)

### 10.1 Kruskal's Minimum Spanning Tree (MST)
- **Time Complexity:** $O(E \log E)$
```cpp
struct Edge {
    int u, v, w;
    bool operator<(const Edge& o) const { return w < o.w; }
};

int kruskal(int n, vector<Edge>& edges) {
    sort(all(edges));
    DisjointSet dsu(n);
    int total_cost = 0, count = 0;
    for (auto& e : edges) {
        if (!dsu.connected(e.u, e.v)) {
            dsu.unionBySize(e.u, e.v);
            total_cost += e.w;
            if (++count == n - 1) return total_cost;
        }
    }
    return -1;
}
```

### 10.2 Matrix Exponentiation ($O(K^3 \log N)$)
```cpp
template<typename T = long long>
struct Matrix {
    int n; vector<vector<T>> a;
    Matrix(int n) : n(n), a(n, vector<T>(n, 0)) {}
    static Matrix eye(int n) {
        Matrix res(n); for (int i = 0; i < n; i++) res.a[i][i] = 1;
        return res;
    }
    Matrix operator*(const Matrix& o) const {
        Matrix res(n);
        for (int i = 0; i < n; i++)
            for (int k = 0; k < n; k++)
                for (int j = 0; j < n; j++)
                    res.a[i][j] = (res.a[i][j] + a[i][k] * o.a[k][j]) % 1000000007;
        return res;
    }
    static Matrix power(Matrix m, long long p) {
        Matrix res = Matrix::eye(m.n);
        while (p) {
            if (p & 1) res = res * m;
            m = m * m; p >>= 1;
        }
        return res;
    }
};
```

### 10.3 Shoelace Formula (Polygon Area)
- **Time Complexity:** $O(N)$
```cpp
struct Point { double x, y; };

double polygon_area(const vector<Point>& p) {
    double area = 0.0;
    int n = p.size();
    for (int i = 0; i < n; ++i) {
        int j = (i + 1) % n;
        area += p[i].x * p[j].y - p[j].x * p[i].y;
    }
    return fabs(area) / 2.0;
}
```
