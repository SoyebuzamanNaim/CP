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

### 1.2 Custom Sort & Comparators
- **Trigger Prefix:** `custom_sort`
- **Time Complexity:** $O(N \log N)$
- **Includes:** Lambda comparator, free function, struct `operator<`, index sorting (argsort), and priority queue min-heap comparator.
```cpp
// 1. Lambda Comparator (Sort in-place without external function):
sort(v.begin(), v.end(), [](const auto& a, const auto& b) {
    if (a.first != b.first) return a.first < b.first; // Ascending by first
    return a.second > b.second;                       // Descending by second
});

// 2. Free Function Comparator:
bool comp(const pair<int, int>& a, const pair<int, int>& b) {
    return a.first < b.first;
}
sort(v.begin(), v.end(), comp);

// 3. Struct with Internal operator<:
struct Item {
    int val, id;
    bool operator<(const Item& o) const {
        if (val != o.val) return val < o.val;
        return id < o.id;
    }
};

// 4. Index Sorting (argsort - sort original indices by array values):
vector<int> p(n); iota(p.begin(), p.end(), 0);
sort(p.begin(), p.end(), [&](int i, int j) { return a[i] < a[j]; });

// 5. Comparator Struct for Priority Queue (Min-Heap by first):
struct ComparePQ {
    bool operator()(const pair<int, int>& a, const pair<int, int>& b) {
        return a.first > b.first; // Greater-than creates Min-Heap!
    }
};
priority_queue<pair<int, int>, vector<pair<int, int>>, ComparePQ> pq;
```

### 1.3 GCC Optimization Pragmas
- **When to use:** Hardware vectorization and loop unrolling for tight 1.0s time limits.
```cpp
#pragma GCC optimize("O3,unroll-loops")
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")
```

### 1.4 __int128 Fast I/O & Recursive Output
- **Trigger Prefix:** `int128`
- **Range:** $\approx [-3.4 \cdot 10^{38}, 3.4 \cdot 10^{38}]$
- **When to use:** Large multiplication products that exceed 64-bit `long long` before modulo.
```cpp
__int128 read128() {
    __int128 x = 0; int f = 1; char ch = getchar();
    while (ch < '0' || ch > '9') { if (ch == '-') f = -1; ch = getchar(); }
    while (ch >= '0' && ch <= '9') { x = x * 10 + ch - '0'; ch = getchar(); }
    return x * f;
}
void print128(__int128 x) {
    if (x < 0) { putchar('-'); x = -x; }
    if (x > 9) print128(x / 10);
    putchar(x % 10 + '0');
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

### 2.2 C++ `<cmath>` Math Functions (exp, ln, root, sin, cos)
```cpp
const double PI = acos(-1.0); // Exact value of π: 3.141592653589793

// 1. Exponential (e^x) & Powers:
double e_to_x   = exp(x);              // e^x (for long double use expl(x))
double power    = pow(base, exp);      // base^exp (e.g. pow(2.0, 10.0) = 1024.0)

// 2. Natural Logarithm (ln) & Logarithms:
double natural  = log(x);              // ln(x) (natural log, base e)
double log_10   = log10(x);            // log10(x) (base 10)
double log_2    = log2(x);             // log2(x) (base 2)
double log_b    = log(x) / log(b);     // log_b(x) in arbitrary base b

// 3. Roots (Square, Cube & k-th Root):
double sq_root  = sqrt(x);             // √x (Square root: x >= 0)
double cb_root  = cbrt(x);             // ∛x (Cube root: works for negative inputs too!)
double kth_root = pow(x, 1.0 / k);     // k-th root of x: x^(1/k)

// 4. Trigonometry: sin, cos, tan (Input MUST be in RADIANS!):
double deg = 60.0;
double rad = deg * (PI / 180.0);       // Degrees to Radians!
double s   = sin(rad);                 // sin(60°) = √3 / 2 ≈ 0.866025
double c   = cos(rad);                 // cos(60°) = 0.5
double t   = tan(rad);                 // tan(60°) ≈ 1.73205

// 5. Inverse Trigonometry & Angles:
double angle_rad = atan2(y, x);        // Angle in radians [-π, π] from (x, y)
double angle_deg = angle_rad * 180.0 / PI; // Radians to Degrees!
double asin_val  = asin(s);            // arcsin (returns [-π/2, π/2])
double acos_val  = acos(c);            // arccos (returns [0, π])

// 6. Absolute & Hypotenuse:
double abs_val   = fabs(x);            // |x| for floating point (fabsl for long double)
double hyp       = hypot(x, y);        // √(x^2 + y^2) (safely prevents overflow)
```

### 2.3 Matrix I/O & 2D Grid Helpers
- **Time Complexity:** $O(N \times M)$
```cpp
// 1. Numeric Matrix N x M Input
int n, m; cin >> n >> m;
vector<vector<int>> a(n, vector<int>(m));
for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++)
        cin >> a[i][j];

// Matrix Output (space-separated, newline per row)
for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++)
        cout << a[i][j] << (j == m - 1 ? "" : " ");
    cout << '\n';
}

// 2. Character Grid (Maze / Labyrinth Input)
vector<string> grid(n);
for (int i = 0; i < n; i++) cin >> grid[i];

// 3. Direction Arrays for Grid Navigation
int dx4[] = {-1, 1, 0, 0}, dy4[] = {0, 0, -1, 1}; // Up, Down, Left, Right
int dx8[] = {-1,-1,-1, 0, 0, 1, 1, 1};             // 8 directions (with diagonals)
int dy8[] = {-1, 0, 1,-1, 1,-1, 0, 1};
bool valid(int x, int y, int n, int m) { return x >= 0 && x < n && y >= 0 && y < m; }
```

### 2.3 All Type Converters & String Parsers
```cpp
// 1. Number <-> String
string s = to_string(12345LL);          // int / LL to string
int num = stoi("123");                   // string to int
long long lnum = stoll("1234567890123"); // string to long long
double d = stod("3.14159");              // string to double
long double ld = stold("3.1415926535");  // string to long double

// 2. Char <-> Digit & Alphabets
int digit = '7' - '0';                   // '7' -> 7
char ch = 7 + '0';                       // 7 -> '7'
int lower_idx = 'c' - 'a';               // 'c' -> 2 (0 to 25)
int upper_idx = 'C' - 'A';               // 'C' -> 2 (0 to 25)
char lower_c = tolower('A');             // 'A' -> 'a'
char upper_c = toupper('a');             // 'a' -> 'A'
// Entire string to lower/upper:
transform(s.begin(), s.end(), s.begin(), ::tolower);

// 3. Base Conversions (Binary, Hex, Octal)
int from_bin = stoi("10110", nullptr, 2);  // "10110" -> 22
int from_hex = stoi("1A", nullptr, 16);    // "1A" -> 26
int from_oct = stoi("75", nullptr, 8);     // "75" -> 61
string to_bin = bitset<32>(22).to_string(); // 22 -> "00...0010110"
to_bin = to_bin.substr(to_bin.find('1'));  // Trim leading zeros
stringstream ss; ss << hex << 255; string hex_str = ss.str(); // "ff"

// 4. String Tokenizer (split by space / delimiter)
stringstream ss2("apple banana cherry");
string word; while (ss2 >> word) { /* process each word */ }
stringstream ss3("1,2,3,4");
string item; while (getline(ss3, item, ',')) { int val = stoi(item); }
```

### 2.4 All STL Containers: Operations & Complexity
```cpp
// 1. VECTOR (Dynamic Array - O(1) push/pop_back, O(1) random access)
vector<int> v = {1, 2, 3};
v.push_back(4); v.pop_back(); v.front(); v.back(); v.size(); v.empty();
v.resize(10, 0); v.assign(5, -1); v.clear();
v.insert(v.begin() + 1, 99); v.erase(v.begin() + 1); // O(N)

// 2. PAIR & TUPLE
pair<int, string> p = {1, "ab"}; auto [id, name] = p; // C++17 structured binding
tuple<int, int, int> tp = {1, 2, 3}; auto [x, y, z] = tp; int f = get<0>(tp);

// 3. SET & MULTISET (Red-Black Tree - O(log N) operations, sorted)
set<int> s; s.insert(5); s.erase(5); bool has = s.count(5);
auto it_lb = s.lower_bound(x); // first element >= x
auto it_ub = s.upper_bound(x); // first element > x
multiset<int> ms; ms.insert(5); ms.insert(5);
ms.erase(ms.find(5)); // Erases ONLY ONE 5! (ms.erase(5) deletes ALL 5s)

// 4. MAP (Sorted key-value - O(log N)) & Frequency Counter
map<string, int> mp; mp["apple"] = 5; mp.count("apple"); mp.erase("apple");
for (auto &[key, val] : mp) { /* sorted by key */ }
// Frequency counter snippet:
map<int, int> freq; for (int x : v) freq[x]++;
int max_f = 0, most_frequent = -1;
for (auto &[val, count] : freq) {
    if (count > max_f) { max_f = count; most_frequent = val; }
}

// 5. PRIORITY_QUEUE (Heap - O(log N) push/pop, O(1) top)
priority_queue<int> max_pq; // Max heap by default
priority_queue<int, vector<int>, greater<int>> min_pq; // Min heap
max_pq.push(10); max_pq.top(); max_pq.pop();

// 6. DEQUE, STACK & QUEUE (O(1) push/pop)
deque<int> dq; dq.push_front(1); dq.push_back(2); dq.pop_front(); dq.pop_back();
stack<int> st; st.push(1); st.top(); st.pop();
queue<int> q; q.push(1); q.front(); q.pop();

// 7. BITSET (Fixed-size bit array - 64x faster bitwise ops)
bitset<64> bs(15); bs.set(2); bs.reset(2); bs.flip(); bool bit = bs.test(0);
int set_bits = bs.count(); unsigned long long val = bs.to_ullong();
```

### 2.5 All STL Algorithms: Quick Syntax & Uses
```cpp
// 1. Sorting & Bounds (v is vector<int>)
sort(all(v));                            // Ascending: O(N log N)
sort(rall(v));                           // Descending: O(N log N)
stable_sort(all(v), comp);               // Preserves relative order
auto it1 = lower_bound(all(v), x);       // First iterator with *it >= x
int idx1 = lower_bound(all(v), x) - v.begin(); // 0-based index of first >= x
auto it2 = upper_bound(all(v), x);       // First iterator with *it > x
bool found = binary_search(all(v), x);   // True if x exists (O(log N))

// 2. Element Operations & Deduplication
v.erase(unique(all(v)), v.end());        // Remove duplicates (sort first!)
reverse(all(v));                         // Invert order: O(N)
rotate(v.begin(), v.begin() + k, v.end()); // Left-rotates by k positions
int mn = *min_element(all(v));           // Minimum element: O(N)
int mx = *max_element(all(v));           // Maximum element: O(N)
int cnt = count(all(v), x);              // Count occurrences of x: O(N)
fill(all(v), 0);                         // Fill all with 0

// 3. Numeric & Prefix Sums (<numeric>)
int sum = accumulate(all(v), 0LL);       // Sum (use 0LL to prevent overflow!)
vector<int> pref(n);
partial_sum(all(v), pref.begin());       // Prefix sum array in-place: O(N)
iota(all(v), 0);                         // Fills with 0, 1, 2, ..., n-1

// 4. Permutations & Order Statistics
next_permutation(all(v));                // Next lexicographical order
prev_permutation(all(v));                // Previous order
// nth_element: Rearranges so element at index k is in its sorted position: O(N) avg
nth_element(v.begin(), v.begin() + k, v.end()); // v[k] is the k-th smallest!
```

### 2.6 Coordinate Compression
- **Trigger Prefix:** `compress`
- **Time Complexity:** $O(N \log N)$
- **When to use:** Mapping large arbitrary numbers (up to $10^9$) into compact 0-based ranks $[0, K-1]$ for BIT, SegTree, or frequency tables.
```cpp
// 1. In-place coordinate compression on vector 'a':
vector<int> vals = a;
sort(vals.begin(), vals.end());
vals.erase(unique(vals.begin(), vals.end()), vals.end());
for (int &x : a) {
    x = lower_bound(vals.begin(), vals.end(), x) - vals.begin(); // 0-based rank
}
// 2. Query original value: vals[compressed_id]
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

### 3.4 Linear Sieve & Fast Prime Factorization (SPF)
- **Trigger Prefix:** `spf`
- **Time Complexity:** $O(N)$ precomputation, $O(\log X)$ per factorization query.
- **When to use:** When you need to factorize multiple queries $Q \le 10^5$ with values up to $10^7$.
```cpp
const int MAXV = 1e7 + 5;
vector<int> spf(MAXV), primes_list;

void linear_sieve() {
    for (int i = 2; i < MAXV; ++i) {
        if (spf[i] == 0) { spf[i] = i; primes_list.push_back(i); }
        for (int p : primes_list) {
            if (p > spf[i] || i * p >= MAXV) break;
            spf[i * p] = p;
        }
    }
}

// Factorize any number x in O(log x):
vector<pair<int, int>> get_factors(int x) {
    vector<pair<int, int>> factors;
    while (x > 1) {
        int p = spf[x], count = 0;
        while (x % p == 0) { count++; x /= p; }
        factors.push_back({p, count});
    }
    return factors;
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

### 3.8 Numerically Stable Quadratic Equation Solver
- **Trigger Prefix:** `quadf`
- **Time Complexity:** $O(1)$
- **Algorithm:** Citardauq formula $q = -0.5 \cdot (b + \text{copysign}(\sqrt{D}, b))$ avoids catastrophic floating-point cancellation when $b \approx \sqrt{b^2 - 4ac}$.
- **Handles:** Degenerate linear cases ($a = 0$), repeated roots ($D = 0$), and no real roots ($D < 0$).
```cpp
using ld = long double;
const ld EPS = 1e-12;

void solve_quadratic(ld a, ld b, ld c) {
    cout << fixed << setprecision(12);
    // Linear equation: bx + c = 0
    if (fabsl(a) < EPS) {
        if (fabsl(b) < EPS) cout << "No solution\n";
        else cout << -c / b << '\n';
        return;
    }

    ld d = b * b - 4 * a * c;

    // No real roots
    if (d < -EPS) {
        cout << "No real roots\n";
        return;
    }

    // One repeated root
    if (fabsl(d) <= EPS) {
        cout << -b / (2 * a) << '\n';
        return;
    }

    // Two real roots with Citardauq numerical stability
    ld sq = sqrtl(d);
    ld q = -0.5L * (b + copysignl(sq, b));

    ld x1 = q / a;
    ld x2 = c / q;

    if (x1 > x2) swap(x1, x2);

    cout << x1 << '\n' << x2 << '\n';
}
```

### 3.9 Basis Conversion (Arbitrary Base 2 to 16)
- **Time Complexity:** $O(\log_b N)$
- **Capability:** Bidirectional conversion between base-$b$ string and `unsigned long long` for any base $b \le 16$.
```cpp
#include <algorithm>
#include <string>
#include <vector>

const std::string DIGITS = "0123456789ABCDEF";

// Convert base-b string to unsigned long long
unsigned long long int basis_string_to_number(std::string &s, int b) {
    unsigned long long int result = 0ULL;
    for (char d : s) {
        result = b * result + (std::find(DIGITS.begin(), DIGITS.end(), d) - DIGITS.begin());
    }
    return result;
}

// Convert unsigned long long to base-b string
std::string number_to_basis_string(unsigned long long int n, int b) {
    std::vector<char> ds;
    do {
        ds.push_back(DIGITS[n % b]);
        n = n / b;
    } while (n != 0);
    return std::string(ds.rbegin(), ds.rend());
}
```

### 3.10 All Binary Operations & Bit Manipulation Hacks
- **Time Complexity:** $O(1)$ per operation
```cpp
// 1. GCC Builtin Functions (Append 'll' for 64-bit integers: e.g. __builtin_popcountll)
int ones = __builtin_popcountll(x);   // Count set bits (number of 1s)
int clz  = __builtin_clzll(x);        // Count leading zeros (undefined if x=0!)
int ctz  = __builtin_ctzll(x);        // Count trailing zeros (lowest set bit index)
int par  = __builtin_parityll(x);     // Parity: 1 if odd number of 1s, 0 if even
int msb  = 63 - __builtin_clzll(x);   // Index of highest set bit (= floor(log2(x)))

// 2. Essential Bit Hacks
bool is_set   = (n >> k) & 1;          // Check if k-th bit is 1 (0-indexed)
n |= (1LL << k);                      // Set k-th bit to 1
n &= ~(1LL << k);                     // Clear k-th bit to 0
n ^= (1LL << k);                      // Toggle k-th bit (flip 0 <-> 1)
bool is_pow2  = n > 0 && !(n & (n - 1)); // True if n is a power of 2
int lsb       = n & (-n);             // Isolates lowest set bit: e.g. 12 (1100) -> 4 (0100)
n &= (n - 1);                         // Clears the lowest set bit

// 3. Iterate All Submasks of Mask m (in strictly descending order)
for (int s = m; s > 0; s = (s - 1) & m) {
    // s is a non-empty submask of m. Total operations across all masks: O(3^N)
}

// 4. Iterate All Masks of Size N
for (int mask = 0; mask < (1 << n); ++mask) { /* O(2^N) */ }
```

### 3.11 Complete Modulo Sheet & $O(1)$ nCr Combinatorics
- **Primes:** Standard CP moduli are $10^9 + 7$ or $998244353$ (NTT friendly).
```cpp
const int MOD = 1e9 + 7; // or 998244353

// 1. Safe Operations (handles negatives & prevents overflow)
long long add(long long a, long long b) { return (a + b) % MOD; }
long long sub(long long a, long long b) { return (a - b + MOD) % MOD; }
long long mul(long long a, long long b) { return (1LL * a * b) % MOD; }

// 2. Fast Exponentiation: (base^exp) % MOD
long long power(long long base, long long exp) {
    long long res = 1; base %= MOD;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}

// 3. Modular Inverse via Fermat's Little Theorem (MOD must be prime) & Division
long long modInverse(long long n) { return power(n, MOD - 2); }
long long divi(long long a, long long b) { return mul(a, modInverse(b)); }

// 4. O(N) Precomputation for O(1) nCr Modulo P (N up to 10^6):
const int MAXN = 1000005;
long long fact[MAXN], invFact[MAXN];
void precompute_nCr(int n = MAXN - 1) {
    fact[0] = invFact[0] = 1;
    for (int i = 1; i <= n; i++) fact[i] = mul(fact[i - 1], i);
    invFact[n] = modInverse(fact[n]);
    for (int i = n - 1; i >= 1; i--) invFact[i] = mul(invFact[i + 1], i + 1);
}
long long nCr_mod(int n, int r) {
    if (r < 0 || r > n) return 0;
    return mul(fact[n], mul(invFact[r], invFact[n - r]));
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

### 4.8 Bipartite Graph Check & 2-Coloring (BFS)
- **Trigger Prefix:** `bipartite`
- **Time Complexity:** $O(V + E)$
- **When to use:** Check if graph has no odd-length cycles and can be partitioned into two independent sets.
```cpp
bool is_bipartite(int n, const vector<vector<int>> &adj, vector<int> &color) {
    color.assign(n + 1, -1);
    for (int start = 1; start <= n; ++start) {
        if (color[start] != -1) continue;
        queue<int> q; q.push(start); color[start] = 0;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (int v : adj[u]) {
                if (color[v] == -1) {
                    color[v] = color[u] ^ 1; q.push(v);
                } else if (color[v] == color[u]) return false; // Odd cycle!
            }
        }
    }
    return true;
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

### 5.3 0-1 BFS (Deque Shortest Path)
- **Trigger Prefix:** `bfs01`
- **Time Complexity:** $O(V + E)$
- **When to use:** Shortest paths on graphs where edge weights are strictly $0$ or $1$. Much faster than Dijkstra ($O(V+E)$ vs $O(E \log V)$).
```cpp
vector<int> zero_one_bfs(int start, int n, const vector<vector<pair<int, int>>> &adj) {
    vector<int> dist(n + 1, 1e9);
    deque<int> dq;
    dist[start] = 0;
    dq.push_back(start);
    while (!dq.empty()) {
        int u = dq.front(); dq.pop_front();
        for (auto &[v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (w == 0) dq.push_front(v); // Push 0-cost edge to front!
                else dq.push_back(v);        // Push 1-cost edge to back!
            }
        }
    }
    return dist;
}
```

### 5.4 Bellman-Ford Algorithm
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

### 7.2 Fenwick Tree (BIT: Sum & Range Average)
- **Time Complexity:** $O(\log N)$ query and update, $O(N)$ memory.
- **Average Property:** Average is easily computed as `sum / (r - l + 1)`.
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

    // Range Average (Integer & Decimal): average = sum / number_of_elements
    int avg(int l, int r) { // Integer average
        return range_query(l, r) / (r - l + 1);
    }
    double avg_d(int l, int r) { // Decimal average
        return (double)range_query(l, r) / (r - l + 1);
    }
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

### 7.4 Segment Tree for MIN & MAX (Minimal Adaptations)
- **Segment Tree for MIN:**
  1. Initialize with infinity: `SegTree(int n) : n(n), t(2 * n, INT_MAX) {}`
  2. Update change: `t[p >> 1] = min(t[p], t[p ^ 1]);`
  3. Query:
  ```cpp
  int query(int l, int r) {
      int res = INT_MAX;
      for (l += n, r += n + 1; l < r; l >>= 1, r >>= 1) {
          if (l & 1) res = min(res, t[l++]);
          if (r & 1) res = min(res, t[--r]);
      }
      return res;
  }
  ```
- **Segment Tree for MAX:**
  1. Initialize: `SegTree(int n) : n(n), t(2 * n, INT_MIN) {}`
  2. Update change: `t[p >> 1] = max(t[p], t[p ^ 1]);`
  3. Query:
  ```cpp
  int query(int l, int r) {
      int res = INT_MIN;
      for (l += n, r += n + 1; l < r; l >>= 1, r >>= 1) {
          if (l & 1) res = max(res, t[l++]);
          if (r & 1) res = max(res, t[--r]);
      }
      return res;
  ```

### Basis conversion (Arbitrary Base 2 to 16)
- **Time Complexity:** $O(\log_b N)$
- **Capability:** Bidirectional conversion between base-$b$ string and `unsigned long long` for any base $b \le 16$.
```cpp
#include <algorithm>
#include <string>
#include <vector>

const std::string DIGITS = "0123456789ABCDEF";

// Convert base-b string to unsigned long long
unsigned long long int basis_string_to_number(std::string &s, int b) {
    unsigned long long int result = 0ULL;
    for (char d : s) {
        result = b * result + (std::find(DIGITS.begin(), DIGITS.end(), d) - DIGITS.begin());
    }
    return result;
}

// Convert unsigned long long to base-b string
std::string number_to_basis_string(unsigned long long int n, int b) {
    std::vector<char> ds;
    do {
        ds.push_back(DIGITS[n % b]);
        n = n / b;
    } while (n != 0);
    return std::string(ds.rbegin(), ds.rend());
}
```

### 7.5 KACTL Iterative Segment Tree (Associative f, [b, e))
- **Time Complexity:** $O(\log N)$
- **Interval:** Semi-open $[b, e)$.
```cpp
struct Tree {
    typedef int T;
    static constexpr T unit = INT_MIN;
    T f(T a, T b) { return max(a, b); } // any associative fn
    vector<T> s; int n;
    Tree(int n = 0, T def = unit) : s(2 * n, def), n(n) {}
    void update(int pos, T val) {
        for (s[pos += n] = val; pos /= 2;)
            s[pos] = f(s[pos * 2], s[pos * 2 + 1]);
    }
    T query(int b, int e) { // query [b, e)
        T ra = unit, rb = unit;
        for (b += n, e += n; b < e; b /= 2, e /= 2) {
            if (b % 2) ra = f(ra, s[b++]);
            if (e % 2) rb = f(s[--e], rb);
        }
        return f(ra, rb);
    }
};
```

### 7.6 Lazy Segment Tree (Range Add, Set & Max)
- **Time Complexity:** $O(\log N)$ per operation
```cpp
const int inf = 1e9;
struct Node {
    Node *l = 0, *r = 0;
    int lo, hi, mset = inf, madd = 0, val = -inf;
    Node(int lo, int hi) : lo(lo), hi(hi) {}
    Node(vector<int>& v, int lo, int hi) : lo(lo), hi(hi) {
        if (lo + 1 < hi) {
            int mid = lo + (hi - lo) / 2;
            l = new Node(v, lo, mid); r = new Node(v, mid, hi);
            val = max(l->val, r->val);
        } else val = v[lo];
    }
    int query(int L, int R) {
        if (R <= lo || hi <= L) return -inf;
        if (L <= lo && hi <= R) return val;
        push();
        return max(l->query(L, R), r->query(L, R));
    }
    void set(int L, int R, int x) {
        if (R <= lo || hi <= L) return;
        if (L <= lo && hi <= R) mset = val = x, madd = 0;
        else {
            push(), l->set(L, R, x), r->set(L, R, x);
            val = max(l->val, r->val);
        }
    }
    void add(int L, int R, int x) {
        if (R <= lo || hi <= L) return;
        if (L <= lo && hi <= R) {
            if (mset != inf) mset += x;
            else madd += x;
            val += x;
        } else {
            push(), l->add(L, R, x), r->add(L, R, x);
            val = max(l->val, r->val);
        }
    }
    void push() {
        if (!l) {
            int mid = lo + (hi - lo) / 2;
            l = new Node(lo, mid); r = new Node(mid, hi);
        }
        if (mset != inf)
            l->set(lo, hi, mset), r->set(lo, hi, mset), mset = inf;
        else if (madd)
            l->add(lo, hi, madd), r->add(lo, hi, madd), madd = 0;
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

### 9.2 Two Pointers & Sliding Window Patterns
- **Time Complexity:** $O(N)$
```cpp
// 1. OPPOSITE DIRECTION (Target Sum on Sorted Array: O(N))
int l = 0, r = n - 1;
while (l < r) {
    int sum = a[l] + a[r];
    if (sum == target) { /* found pair (l, r) */ break; }
    else if (sum < target) l++;
    else r--;
}

// 2. SAME DIRECTION (Sliding Window: Longest subarray with sum <= K: O(N))
int left = 0, cur_sum = 0, max_len = 0;
for (int right = 0; right < n; ++right) {
    cur_sum += a[right];
    while (cur_sum > K && left <= right) cur_sum -= a[left++];
    max_len = max(max_len, right - left + 1);
}

// 3. MERGING TWO SORTED LISTS (Original twoPointer snippet: O(N + M))
vector<int> a(n), b(m), c;
for (int &x : a) cin >> x;
for (int &x : b) cin >> x;
int i = 0, j = 0;
while (i < n || j < m) {
    while ((i < n) && (j >= m || (a[i] <= b[j]))) { c.push_back(a[i]); i++; }
    while ((j < m) && (i >= n || b[j] <= a[i])) { c.push_back(b[j]); j++; }
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

// Unbounded Knapsack: change inner loop to: for (int w = wt[i]; w <= W; w++)
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

### 9.5 Kadane's Algorithm (Max Subarray Sum with Range Indices)
- **Time Complexity:** $O(N)$
```cpp
long long max_sum = -1e18, cur = 0;
int best_l = 0, best_r = 0, start = 0;
for (int i = 0; i < n; i++) {
    cur += a[i];
    if (cur > max_sum) { max_sum = cur; best_l = start; best_r = i; }
    if (cur < 0) { cur = 0; start = i + 1; }
} // Max contiguous subarray sum is on range [best_l, best_r]
```

### 9.6 Longest Common Subsequence (LCS with Path Reconstruction)
- **Time Complexity:** $O(N \cdot M)$
```cpp
string get_lcs(const string &s, const string &t) {
    int n = s.size(), m = t.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
            dp[i][j] = (s[i - 1] == t[j - 1]) ? 1 + dp[i - 1][j - 1] : max(dp[i - 1][j], dp[i][j - 1]);
    string res = ""; int i = n, j = m;
    while (i > 0 && j > 0) {
        if (s[i - 1] == t[j - 1]) { res += s[i - 1]; i--; j--; }
        else if (dp[i - 1][j] > dp[i][j - 1]) i--;
        else j--;
    }
    reverse(res.begin(), res.end());
    return res; // Length is dp[n][m]
}
```

### 9.7 Coin Change (Min Coins & Total Combinations)
- **Time Complexity:** $O(N \cdot X)$
```cpp
// 1. Min coins to make target amount X:
vector<int> dp(X + 1, 1e9); dp[0] = 0;
for (int i = 1; i <= X; i++)
    for (int c : coins) if (i >= c) dp[i] = min(dp[i], dp[i - c] + 1);
int min_coins = (dp[X] >= 1e9 ? -1 : dp[X]);

// 2. Number of distinct combinations (coins outer loop):
vector<int> ways(X + 1, 0); ways[0] = 1;
for (int c : coins)
    for (int i = c; i <= X; i++) ways[i] = (ways[i] + ways[i - c]) % MOD;
```

### 9.8 Edit Distance (Levenshtein Distance)
- **Time Complexity:** $O(N \cdot M)$
```cpp
int edit_distance(const string &s1, const string &s2) {
    int n = s1.size(), m = s2.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1));
    for (int i = 0; i <= n; i++) dp[i][0] = i;
    for (int j = 0; j <= m; j++) dp[0][j] = j;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (s1[i - 1] == s2[j - 1]) dp[i][j] = dp[i - 1][j - 1];
            else dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
        }
    }
    return dp[n][m];
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

### 10.4 2D Point, Vectors, Dot & Cross Products
```cpp
struct Pt {
    double x, y;
    Pt(double x = 0, double y = 0) : x(x), y(y) {}
    Pt operator+(Pt p) const { return {x + p.x, y + p.y}; }
    Pt operator-(Pt p) const { return {x - p.x, y - p.y}; }
    Pt operator*(double d) const { return {x * d, y * d}; }
    Pt operator/(double d) const { return {x / d, y / d}; }
    double dot(Pt p) const { return x * p.x + y * p.y; }       // |a||b|cos(θ)
    double cross(Pt p) const { return x * p.y - y * p.x; }     // |a||b|sin(θ)
    double dist2() const { return x * x + y * y; }
    double dist() const { return sqrt(dist2()); }
    double angle() const { return atan2(y, x); }
};
// Orientation: > 0 = CCW (left turn), < 0 = CW (right turn), == 0 = Collinear
double ccw(Pt a, Pt b, Pt c) { return (b - a).cross(c - a); }
```

### 10.5 Lines, Segments & Triangles Equations
```cpp
// 1. Distance from point P to line AB:
double dist_to_line(Pt p, Pt a, Pt b) {
    return fabs((b - a).cross(p - a)) / (b - a).dist();
}

// 2. Line Intersection (A1*x + B1*y = C1 and A2*x + B2*y = C2 via Cramer):
bool line_inter(double a1, double b1, double c1, double a2, double b2, double c2, Pt &out) {
    double d = a1 * b2 - a2 * b1;
    if (fabs(d) < 1e-9) return false; // Parallel or collinear
    out.x = (c1 * b2 - c2 * b1) / d;
    out.y = (a1 * c2 - a2 * c1) / d;
    return true;
}

// 3. Triangle Formulas: sides a, b, c
// Heron's Area: s = (a + b + c) / 2
double heron(double a, double b, double c) {
    double s = (a + b + c) / 2.0;
    return sqrt(max(0.0, s * (s - a) * (s - b) * (s - c)));
}
// Inradius: r = Area / s | Circumradius: R = (a * b * c) / (4 * Area)
double inradius(double a, double b, double c) { return heron(a, b, c) / ((a + b + c) / 2.0); }
double circumradius(double a, double b, double c) { return (a * b * c) / (4.0 * heron(a, b, c)); }
```

### 10.6 Pick's Theorem, Centroid & 3D Solids
```cpp
// 1. Pick's Theorem: Area = I + B/2 - 1  =>  I = Area - B/2 + 1
// B = boundary lattice points = sum(gcd(|x2-x1|, |y2-y1|)) for all polygon edges
// I = strictly interior lattice points

// 2. Polygon Centroid (Center of Mass):
Pt polygon_centroid(const vector<Pt>& p) {
    Pt c(0, 0); double A = 0; int n = p.size();
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n; double cross = p[i].cross(p[j]);
        A += cross; c = c + (p[i] + p[j]) * cross;
    }
    return c / (3.0 * A);
}

// 3. Circles & 3D Solid Geometry Equations:
// Circle:   Area = π * r^2, Circumference = 2 * π * r
// Sphere:   Volume = (4/3) * π * r^3, Surface Area = 4 * π * r^2
// Cylinder: Volume = π * r^2 * h, Surface Area = 2 * π * r * (r + h)
// Cone:     Volume = (1/3) * π * r^2 * h, Slant height s = sqrt(r^2 + h^2)
```

### 10.7 Math Series, Logarithms & Algebra Cheatsheet
```cpp
// 1. Summation Formulas:
// Sum of 1..N:           N * (N + 1) / 2
// Sum of squares 1..N^2: N * (N + 1) * (2N + 1) / 6
// Sum of cubes 1..N^3:   (N * (N + 1) / 2)^2
// Geometric Progression: a + a*r + ... + a*r^(n-1) = a * (r^n - 1) / (r - 1)

// 2. Logarithm & Exponent Rules:
// log_b(a) = ln(a) / ln(b) = log10(a) / log10(b)
// log(a * b) = log(a) + log(b), log(a / b) = log(a) - log(b), log(a^k) = k * log(a)

// 3. Number of Digits of N in Base B: floor(log_B(N)) + 1
// 4. Stirling's Approximation: n! ≈ sqrt(2 * π * n) * (n / e)^n
```
