#pragma once
#include <bits/stdc++.h>
#include <cassert>

// Tested C++17 reference implementations. All vertices and arrays are
// 0-indexed. Copy a complete snippet plus its stated dependencies into
// a contest solution.
namespace cpref {

// [snippet:scc:start]
struct SCC {
  int n;
  std::vector<std::vector<int>> g, rg;
  explicit SCC(int n) : n(n), g(n), rg(n) {}
  void add_edge(int u, int v) {
    g[u].push_back(v);
    rg[v].push_back(u);
  }

  // Kosaraju: component IDs are in topological order (source first).
  std::vector<int> components() const {
    std::vector<char> seen(n);
    std::vector<int> order, comp(n, -1);
    for (int root = 0; root < n; ++root)
      if (!seen[root]) {
        std::vector<std::pair<int, int>> st{{root, 0}};
        seen[root] = 1;
        while (!st.empty()) {
          auto &[u, i] = st.back();
          if (i == (int)g[u].size()) {
            order.push_back(u);
            st.pop_back();
          } else {
            int v = g[u][i++];
            if (!seen[v])
              seen[v] = 1, st.push_back({v, 0});
          }
        }
      }
    int id = 0;
    for (int i = n - 1; i >= 0; --i) {
      int root = order[i];
      if (comp[root] != -1)
        continue;
      std::vector<int> st{root};
      comp[root] = id;
      while (!st.empty()) {
        int u = st.back();
        st.pop_back();
        for (int v : rg[u])
          if (comp[v] == -1)
            comp[v] = id, st.push_back(v);
      }
      ++id;
    }
    return comp;
  }
};
// [snippet:scc:end]

// [snippet:two_sat:start]
// Depends on SCC above. Literal (variable x, truth value val) is 2*x +
// val.
struct TwoSAT {
  int n;
  SCC scc;
  explicit TwoSAT(int n) : n(n), scc(2 * n) {}
  int lit(int x, bool val) const { return 2 * x + int(val); }
  void implication(int a, int b) { scc.add_edge(a, b); }
  void add_or(int x, bool xv, int y, bool yv) {
    int a = lit(x, xv), b = lit(y, yv);
    implication(a ^ 1, b);
    implication(b ^ 1, a);
  }
  std::optional<std::vector<bool>> solve() const {
    auto c = scc.components();
    std::vector<bool> ans(n);
    for (int x = 0; x < n; ++x) {
      if (c[2 * x] == c[2 * x + 1])
        return std::nullopt;
      ans[x] = c[2 * x + 1] > c[2 * x];
    }
    return ans;
  }
};
// [snippet:two_sat:end]

// [snippet:bridges:start]
// Undirected multigraph: edge IDs prevent a parallel edge becoming a
// false bridge.
struct Bridges {
  int n, timer = 0;
  std::vector<std::vector<std::pair<int, int>>> g;
  std::vector<int> tin, low, bridge_ids;
  explicit Bridges(int n) : n(n), g(n), tin(n, -1), low(n) {}
  void add_edge(int u, int v, int id) {
    g[u].push_back({v, id});
    g[v].push_back({u, id});
  }
  void dfs(int u, int parent_edge = -1) {
    tin[u] = low[u] = timer++;
    for (auto [v, id] : g[u]) {
      if (id == parent_edge)
        continue;
      if (tin[v] != -1)
        low[u] = std::min(low[u], tin[v]);
      else {
        dfs(v, id);
        low[u] = std::min(low[u], low[v]);
        if (low[v] > tin[u])
          bridge_ids.push_back(id);
      }
    }
  }
  std::vector<int> find() {
    timer = 0;
    std::fill(tin.begin(), tin.end(), -1);
    std::fill(low.begin(), low.end(), 0);
    bridge_ids.clear();
    for (int u = 0; u < n; ++u)
      if (tin[u] == -1)
        dfs(u);
    return bridge_ids;
  }
}; // Recursive DFS: use an iterative version if depth may exceed stack
   // capacity.
// [snippet:bridges:end]

// [snippet:dinic:start]
struct Dinic {
  struct Edge {
    int to, rev;
    long long cap;
  };
  int n;
  std::vector<std::vector<Edge>> g;
  std::vector<int> level, ptr;
  explicit Dinic(int n) : n(n), g(n), level(n), ptr(n) {}
  void add_edge(int u, int v, long long cap) { // directed, cap >= 0
    if (u == v)
      return;
    int a = (int)g[u].size(), b = (int)g[v].size();
    g[u].push_back({v, b, cap});
    g[v].push_back({u, a, 0});
  }
  bool bfs(int s, int t) {
    std::fill(level.begin(), level.end(), -1);
    std::queue<int> q;
    level[s] = 0;
    q.push(s);
    while (!q.empty()) {
      int u = q.front();
      q.pop();
      for (auto &e : g[u])
        if (e.cap > 0 && level[e.to] < 0)
          level[e.to] = level[u] + 1, q.push(e.to);
    }
    return level[t] >= 0;
  }
  long long dfs(int u, int t, long long f) {
    if (u == t || f == 0)
      return f;
    for (int &i = ptr[u]; i < (int)g[u].size(); ++i) {
      Edge &e = g[u][i];
      if (e.cap == 0 || level[e.to] != level[u] + 1)
        continue;
      long long sent = dfs(e.to, t, std::min(f, e.cap));
      if (sent) {
        e.cap -= sent;
        g[e.to][e.rev].cap += sent;
        return sent;
      }
    }
    return 0;
  }
  long long max_flow(int s, int t) {
    if (s == t)
      return 0;
    long long ans = 0;
    while (bfs(s, t)) {
      std::fill(ptr.begin(), ptr.end(), 0);
      while (long long f = dfs(s, t, LLONG_MAX))
        ans += f;
    }
    return ans;
  }
}; // O(V^2 E) general bound. DFS is recursive.
// [snippet:dinic:end]

// [snippet:hopcroft_karp:start]
struct HopcroftKarp {
  int nl, nr;
  std::vector<std::vector<int>> g;
  std::vector<int> left, right, dist;
  int shortest;
  HopcroftKarp(int nl, int nr)
      : nl(nl), nr(nr), g(nl), left(nl, -1), right(nr, -1), dist(nl) {}
  void add_edge(int u, int v) {
    g[u].push_back(v);
  } // u in left, v in right
  bool bfs() {
    std::queue<int> q;
    shortest = INT_MAX;
    std::fill(dist.begin(), dist.end(), -1);
    for (int u = 0; u < nl; ++u)
      if (left[u] == -1)
        dist[u] = 0, q.push(u);
    while (!q.empty()) {
      int u = q.front();
      q.pop();
      if (dist[u] >= shortest)
        continue;
      for (int v : g[u]) {
        int w = right[v];
        if (w == -1)
          shortest = dist[u] + 1;
        else if (dist[w] == -1)
          dist[w] = dist[u] + 1, q.push(w);
      }
    }
    return shortest != INT_MAX;
  }
  bool dfs(int u) {
    for (int v : g[u]) {
      int w = right[v];
      if ((w == -1 && dist[u] + 1 == shortest) ||
          (w != -1 && dist[w] == dist[u] + 1 && dfs(w))) {
        left[u] = v;
        right[v] = u;
        return true;
      }
    }
    dist[u] = -1;
    return false;
  }
  int max_matching() {
    int ans = 0;
    for (int v : left) ans += (v != -1);
    while (bfs())
      for (int u = 0; u < nl; ++u)
        if (left[u] == -1 && dfs(u))
          ++ans;
    return ans;
  }
}; // O(E sqrt(V)); recursion may be deep.
// [snippet:hopcroft_karp:end]

// [snippet:euler_walk:start]
// Euler path/circuit of an undirected multigraph; returns vertices or
// nullopt.
struct EulerWalk {
  int n, edges = 0;
  std::vector<std::vector<std::pair<int, int>>> g;
  explicit EulerWalk(int n) : n(n), g(n) {}
  void add_edge(int u, int v) {
    g[u].push_back({v, edges});
    g[v].push_back({u, edges});
    ++edges;
  }
  std::optional<std::vector<int>> walk() const {
    if (!n)
      return std::vector<int>{};
    int start = -1, odd = 0;
    for (int u = 0; u < n; ++u) {
      if (g[u].size() % 2)
        ++odd, start = u;
      else if (start == -1 && !g[u].empty())
        start = u;
    }
    if (odd != 0 && odd != 2)
      return std::nullopt;
    if (start == -1)
      return std::vector<int>{0};
    std::vector<int> ptr(n), stack{start}, path;
    std::vector<char> used(edges);
    while (!stack.empty()) {
      int u = stack.back();
      while (ptr[u] < (int)g[u].size() && used[g[u][ptr[u]].second])
        ++ptr[u];
      if (ptr[u] == (int)g[u].size())
        path.push_back(u), stack.pop_back();
      else {
        auto [v, id] = g[u][ptr[u]++];
        if (!used[id])
          used[id] = 1, stack.push_back(v);
      }
    }
    if ((int)path.size() != edges + 1)
      return std::nullopt; // disconnected edges
    std::reverse(path.begin(), path.end());
    return path;
  }
}; // O(V+E). Isolated vertices are irrelevant when edges exist.
// [snippet:euler_walk:end]

// [snippet:mo:start]
struct MoQuery {
  int l, r, id;
}; // inclusive [l,r], IDs 0..Q-1
template <class Ans, class Add, class Remove, class Get>
std::vector<Ans> mo_process(int n, std::vector<MoQuery> qs, Add add,
                            Remove remove, Get get) {
  int block = std::max(1, (int)std::sqrt(std::max(1, n)));
  std::sort(
      qs.begin(), qs.end(), [&](const MoQuery &a, const MoQuery &b) {
        int x = a.l / block, y = b.l / block;
        if (x != y)
          return x < y;
        return (x & 1)
                   ? a.r > b.r
                   : a.r < b.r; // snake order limits pointer movement
      });
  std::vector<Ans> result(qs.size());
  int l = 0, r = -1; // current window is [l,r], initially empty
  for (auto q : qs) {
    while (l > q.l)
      add(--l);
    while (r < q.r)
      add(++r);
    while (l < q.l)
      remove(l++);
    while (r > q.r)
      remove(r--);
    result[q.id] = get();
  }
  return result;
} // Add/remove must be inverse; static array, offline queries.
// Adapted from Mohammadreza-mz's Mo Algorithm.cpp and the supplied
// notebook.
// [snippet:mo:end]

// [snippet:hungarian:start]
// Minimum-cost assignment; n rows, m columns, n<=m. Every row gets one
// distinct column.
struct Assignment {
  long long cost;
  std::vector<int> column_of_row;
};
inline Assignment
hungarian(const std::vector<std::vector<long long>> &a) {
  int n = (int)a.size();
  if (!n)
    return {0, {}};
  int m = (int)a[0].size();
  assert(n <= m && m > 0);
  for (auto &row : a)
    assert((int)row.size() == m);
  const long long INF = LLONG_MAX / 4;
  std::vector<long long> u(n + 1), v(m + 1);
  std::vector<int> p(m + 1), way(m + 1);
  for (int i = 1; i <= n; ++i) {
    p[0] = i;
    int j0 = 0;
    std::vector<long long> minv(m + 1, INF);
    std::vector<char> used(m + 1);
    do {
      used[j0] = 1;
      int i0 = p[j0], j1 = 0;
      long long delta = INF;
      for (int j = 1; j <= m; ++j)
        if (!used[j]) {
          long long cur = a[i0 - 1][j - 1] - u[i0] - v[j];
          if (cur < minv[j])
            minv[j] = cur, way[j] = j0;
          if (minv[j] < delta)
            delta = minv[j], j1 = j;
        }
      for (int j = 0; j <= m; ++j)
        if (used[j])
          u[p[j]] += delta, v[j] -= delta;
        else
          minv[j] -= delta;
      j0 = j1;
    } while (p[j0] != 0);
    do {
      int j1 = way[j0];
      p[j0] = p[j1];
      j0 = j1;
    } while (j0);
  }
  std::vector<int> col(n, -1);
  for (int j = 1; j <= m; ++j)
    if (p[j])
      col[p[j] - 1] = j - 1;
  return {-v[0], col};
} // O(n^2 m), handles negative costs. Use long long costs with safe
  // total bounds.
// Adapted from the supplied notebook, pp. 14-15.
// [snippet:hungarian:end]

// [snippet:z_function:start]
inline std::vector<int> z_function(const std::string &s) {
  int n = (int)s.size();
  std::vector<int> z(n);
  for (int i = 1, l = 0, r = 0; i < n; ++i) {
    if (i < r)
      z[i] = std::min(r - i, z[i - l]);
    while (i + z[i] < n && s[z[i]] == s[i + z[i]])
      ++z[i];
    if (i + z[i] > r)
      l = i, r = i + z[i];
  }
  return z; // z[0]=0; Z box is [l,r).
}
// [snippet:z_function:end]

// [snippet:manacher:start]
struct PalRadii {
  std::vector<int> odd, even;
};
inline PalRadii manacher(const std::string &s) {
  int n = (int)s.size();
  PalRadii p{{}, {}};
  p.odd.resize(n);
  p.even.resize(n);
  for (int i = 0, l = 0, r = -1; i < n; ++i) {
    int k = i > r ? 1 : std::min(p.odd[l + r - i], r - i + 1);
    while (i - k >= 0 && i + k < n && s[i - k] == s[i + k])
      ++k;
    p.odd[i] = k;
    if (i + k - 1 > r)
      l = i - k + 1, r = i + k - 1;
  }
  for (int i = 0, l = 0, r = -1; i < n; ++i) {
    int k = i > r ? 0 : std::min(p.even[l + r - i + 1], r - i + 1);
    while (i - k - 1 >= 0 && i + k < n && s[i - k - 1] == s[i + k])
      ++k;
    p.even[i] = k;
    if (i + k - 1 > r)
      l = i - k, r = i + k - 1;
  }
  return p; // odd palindrome length = 2*odd[i]-1; even = 2*even[i].
}
// [snippet:manacher:end]

// [snippet:aho:start]
struct AhoCorasick {
  struct Node {
    std::array<int, 26> next{};
    int link = 0, out = 0;
  };
  std::vector<Node> t{1};
  bool built = false;
  void
  add(const std::string &s) { // nonempty lowercase a-z patterns only
    assert(!built && !s.empty());
    int u = 0;
    for (char ch : s) {
      assert('a' <= ch && ch <= 'z');
      int c = ch - 'a';
      if (!t[u].next[c]) {
        t[u].next[c] = (int)t.size();
        t.emplace_back();
      }
      u = t[u].next[c];
    }
    ++t[u].out; // duplicates count separately
  }
  void build() {
    assert(!built);
    std::queue<int> q;
    for (int c = 0; c < 26; ++c)
      if (t[0].next[c])
        q.push(t[0].next[c]);
    while (!q.empty()) {
      int u = q.front();
      q.pop();
      t[u].out += t[t[u].link].out;
      for (int c = 0; c < 26; ++c) {
        int v = t[u].next[c];
        if (v)
          t[v].link = t[t[u].link].next[c], q.push(v);
        else
          t[u].next[c] = t[t[u].link].next[c];
      }
    }
    built = true;
  }
  long long count_matches(const std::string &text) const {
    assert(built);
    long long ans = 0;
    int u = 0;
    for (char ch : text) {
      if (ch < 'a' || ch > 'z') {
        u = 0;
        continue;
      }
      u = t[u].next[ch - 'a'];
      ans += t[u].out;
    }
    return ans;
  }
}; // O(total pattern length * alphabet + text length).
// [snippet:aho:end]

// [snippet:suffix_array:start]
struct SuffixArray {
  std::vector<int> sa,
      lcp; // sa has n entries, lcp[i]=LCP(sa[i],sa[i-1]), lcp[0]=0
  explicit SuffixArray(const std::string &s) {
    int n = (int)s.size();
    sa.resize(n);
    lcp.assign(n, 0);
    if (!n)
      return;
    std::vector<int> rank(n), tmp(n), pos(n);
    for (int i = 0; i < n; ++i)
      sa[i] = i, rank[i] = (unsigned char)s[i];
    for (int k = 1; k < n; k *= 2) {
      auto key = [&](int i) {
        return std::pair<int, int>{rank[i],
                                   i + k < n ? rank[i + k] : -1};
      };
      std::sort(sa.begin(), sa.end(),
                [&](int a, int b) { return key(a) < key(b); });
      tmp[sa[0]] = 0;
      for (int i = 1; i < n; ++i)
        tmp[sa[i]] = tmp[sa[i - 1]] + (key(sa[i - 1]) != key(sa[i]));
      rank.swap(tmp);
      if (rank[sa.back()] == n - 1)
        break;
    }
    for (int i = 0; i < n; ++i)
      pos[sa[i]] = i;
    for (int i = 0, k = 0; i < n; ++i) {
      int r = pos[i];
      if (!r)
        continue;
      int j = sa[r - 1];
      while (i + k < n && j + k < n && s[i + k] == s[j + k])
        ++k;
      lcp[r] = k;
      if (k)
        --k;
    }
  }
}; // O(n log^2 n) with std::sort; simpler to audit than radix version.
// [snippet:suffix_array:end]

// [snippet:rolling_hash:start]
// Static double rolling hash of half-open string ranges [l,r).
struct DoubleHash {
  static constexpr long long P1 = 1000000007LL, P2 = 1000000009LL,
                             B = 911382323LL;
  std::vector<long long> h1, h2, p1, p2;
  explicit DoubleHash(const std::string &s) {
    int n = (int)s.size();
    h1.resize(n + 1);
    h2.resize(n + 1);
    p1.resize(n + 1);
    p2.resize(n + 1);
    p1[0] = p2[0] = 1;
    for (int i = 0; i < n; ++i) {
      int ch = (unsigned char)s[i] + 1;
      h1[i + 1] = (h1[i] * B + ch) % P1;
      h2[i + 1] = (h2[i] * B + ch) % P2;
      p1[i + 1] = p1[i] * B % P1;
      p2[i + 1] = p2[i] * B % P2;
    }
  }
  std::pair<long long, long long> get(int l, int r) const {
    assert(0 <= l && l <= r && r < (int)h1.size());
    return {(h1[r] - h1[l] * p1[r - l] % P1 + P1) % P1,
            (h2[r] - h2[l] * p2[r - l] % P2 + P2) % P2};
  }
}; // O(N) build, O(1) substring hash; collision probability is low, not
   // zero.
// [snippet:rolling_hash:end]

// [snippet:crt:start]
inline long long extended_gcd(long long a, long long b, long long &x,
                              long long &y) {
  if (!b) {
    x = 1;
    y = 0;
    return a;
  }
  long long x1, y1, g = extended_gcd(b, a % b, x1, y1);
  x = y1;
  y = x1 - (a / b) * y1;
  return g;
}
// Return {smallest nonnegative solution, lcm}; nullopt if incompatible
// or overflow.
inline std::optional<std::pair<long long, long long>>
crt(long long a, long long m, long long b, long long n) {
  assert(m > 0 && n > 0);
  a %= m;
  if (a < 0)
    a += m;
  b %= n;
  if (b < 0)
    b += n;
  long long x, y, g = extended_gcd(m, n, x, y);
  __int128 diff = (__int128)b - a;
  if (diff % g)
    return std::nullopt;
  __int128 mod = (__int128)m / g * n;
  if (mod > LLONG_MAX)
    return std::nullopt;
  __int128 k = (diff / g) * x;
  long long ng = n / g;
  k = (k % ng + ng) % ng;
  long long rem = (long long)((a + k * m) % mod);
  return std::pair<long long, long long>{rem, (long long)mod};
}
// [snippet:crt:end]

// [snippet:phi_sieve:start]
inline std::vector<int> phi_sieve(int n) { // phi[1]=1, phi[0]=0
  assert(n >= 0);
  std::vector<int> phi(n + 1), primes;
  std::vector<char> composite(n + 1);
  if (n >= 1)
    phi[1] = 1;
  for (int i = 2; i <= n; ++i) {
    if (!composite[i])
      primes.push_back(i), phi[i] = i - 1;
    for (int p : primes) {
      if (1LL * i * p > n)
        break;
      composite[i * p] = 1;
      if (i % p == 0) {
        phi[i * p] = phi[i] * p;
        break;
      }
      phi[i * p] = phi[i] * (p - 1);
    }
  }
  return phi;
} // O(n) time and memory.
// [snippet:phi_sieve:end]

// [snippet:miller_rabin:start]
using u64 = uint64_t;
using u128 = __uint128_t;
inline u64 mul_mod(u64 a, u64 b, u64 mod) { return (u128)a * b % mod; }
inline u64 pow_mod(u64 a, u64 e, u64 mod) {
  assert(mod > 0);
  u64 r = 1 % mod;
  for (; e; e >>= 1, a = mul_mod(a, a, mod))
    if (e & 1)
      r = mul_mod(r, a, mod);
  return r;
}
inline bool is_prime(u64 n) { // deterministic for every uint64_t
  if (n < 2)
    return false;
  for (u64 p : {2ULL, 3ULL, 5ULL, 7ULL, 11ULL, 13ULL, 17ULL, 19ULL,
                23ULL, 29ULL, 31ULL, 37ULL}) {
    if (n % p == 0)
      return n == p;
  }
  u64 d = n - 1, s = 0;
  while (!(d & 1))
    d >>= 1, ++s;
  for (u64 a : {2ULL, 325ULL, 9375ULL, 28178ULL, 450775ULL, 9780504ULL,
                1795265022ULL}) {
    if (a % n == 0)
      continue;
    u64 x = pow_mod(a % n, d, n);
    if (x == 1 || x == n - 1)
      continue;
    bool passed = false;
    for (u64 r = 1; r < s; ++r) {
      x = mul_mod(x, x, n);
      if (x == n - 1) {
        passed = true;
        break;
      }
    }
    if (!passed)
      return false;
  }
  return true;
}
// [snippet:miller_rabin:end]

// [snippet:geometry_int:start]
struct IPoint {
  long long x, y;
  bool operator<(const IPoint &b) const {
    return std::tie(x, y) < std::tie(b.x, b.y);
  }
  bool operator==(const IPoint &b) const {
    return x == b.x && y == b.y;
  }
};
inline __int128 cross(IPoint a, IPoint b, IPoint c) {
  // Requires the determinant to fit signed __int128.
  return ((__int128)b.x - a.x) * ((__int128)c.y - a.y) -
         ((__int128)b.y - a.y) * ((__int128)c.x - a.x);
}
inline int sign(__int128 x) { return (x > 0) - (x < 0); }
inline bool on_segment(IPoint a, IPoint b, IPoint p) {
  return cross(a, b, p) == 0 && std::min(a.x, b.x) <= p.x &&
         p.x <= std::max(a.x, b.x) && std::min(a.y, b.y) <= p.y &&
         p.y <= std::max(a.y, b.y);
}
inline bool segments_intersect(IPoint a, IPoint b, IPoint c, IPoint d) {
  int x = sign(cross(a, b, c)), y = sign(cross(a, b, d));
  int z = sign(cross(c, d, a)), w = sign(cross(c, d, b));
  if (x == 0 && on_segment(a, b, c))
    return true;
  if (y == 0 && on_segment(a, b, d))
    return true;
  if (z == 0 && on_segment(c, d, a))
    return true;
  if (w == 0 && on_segment(c, d, b))
    return true;
  return x != y && z != w;
}
inline std::vector<IPoint> convex_hull(std::vector<IPoint> p) {
  std::sort(p.begin(), p.end());
  p.erase(std::unique(p.begin(), p.end()), p.end());
  if (p.size() < 2)
    return p;
  std::vector<IPoint> h;
  for (auto v : p) {
    while (h.size() >= 2 && cross(h[h.size() - 2], h.back(), v) <= 0)
      h.pop_back();
    h.push_back(v);
  }
  size_t lower = h.size();
  for (int i = (int)p.size() - 2; i >= 0; --i) {
    auto v = p[i];
    while (h.size() > lower && cross(h[h.size() - 2], h.back(), v) <= 0)
      h.pop_back();
    h.push_back(v);
  }
  h.pop_back();
  return h; // CCW, starts at lexicographic min; collinear interior
            // removed.
}
inline __int128
area2(const std::vector<IPoint> &p) { // signed twice area
  __int128 a = 0;
  int n = (int)p.size();
  for (int i = 0; i < n; ++i)
    a += (__int128)p[i].x * p[(i + 1) % n].y -
         (__int128)p[i].y * p[(i + 1) % n].x;
  return a;
}
inline int point_in_polygon(const std::vector<IPoint> &p, IPoint q) {
  bool inside = false;
  int n = (int)p.size();
  for (int i = 0, j = n - 1; i < n; j = i++) {
    IPoint a = p[j], b = p[i];
    if (on_segment(a, b, q))
      return 0; // boundary
    if ((a.y > q.y) != (b.y > q.y)) {
      // Compare crossing x without floating point; orientation flips
      // with edge direction.
      __int128 c = cross(a, b, q);
      if ((c > 0) == (b.y > a.y))
        inside = !inside;
    }
  }
  return inside ? 1 : -1; // inside=1, boundary=0, outside=-1
}
// [snippet:geometry_int:end]

// [snippet:geometry_circle:start]
struct FPoint {
  long double x, y;
};
inline FPoint operator+(FPoint a, FPoint b) {
  return {a.x + b.x, a.y + b.y};
}
inline FPoint operator-(FPoint a, FPoint b) {
  return {a.x - b.x, a.y - b.y};
}
inline FPoint operator*(FPoint a, long double k) {
  return {a.x * k, a.y * k};
}
inline long double dot(FPoint a, FPoint b) {
  return a.x * b.x + a.y * b.y;
}
// Intersection of infinite line AB and circle (center O, radius r).
inline std::vector<FPoint> circle_line(FPoint o, long double r,
                                       FPoint a, FPoint b) {
  assert(r >= 0);
  FPoint d = b - a;
  long double len2 = dot(d, d);
  if (len2 == 0)
    return {}; // degenerate line
  long double t = dot(o - a, d) / len2;
  FPoint foot = a + d * t;
  long double dist2 = dot(foot - o, foot - o);
  long double h2 = r * r - dist2;
  // Relative tolerance on squared distances preserves very small circles.
  long double tol = 64 * std::numeric_limits<long double>::epsilon() *
                    std::max(r * r, dist2);
  if (h2 < -tol)
    return {};
  if (h2 <= tol)
    return {foot};
  long double step = std::sqrt(h2 / len2);
  return {foot - d * step, foot + d * step};
}
// [snippet:geometry_circle:end]

} // namespace cpref
