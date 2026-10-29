#include "algorithms.hpp"
using namespace std;
using namespace cpref;

int main() {
  mt19937 rng(1234567);
  auto rnd = [&](int n) { return int(rng()%n); };

  // SCC and 2-SAT against reachability / exhaustive Boolean assignments.
  for (int trial=0;trial<250;++trial) {
    int n=1+rnd(7); SCC s(n);
    vector<vector<bool>> reach(n,vector<bool>(n));
    for (int i=0;i<n;++i) reach[i][i]=true;
    for (int i=0;i<n*n;++i) if (rnd(3)==0) {
      int u=rnd(n),v=rnd(n); s.add_edge(u,v); reach[u][v]=true;
    }
    for (int k=0;k<n;++k) for (int i=0;i<n;++i) for (int j=0;j<n;++j)
      reach[i][j]=reach[i][j] || (reach[i][k] && reach[k][j]);
    auto c=s.components();
    for (int i=0;i<n;++i) for (int j=0;j<n;++j)
      assert((c[i]==c[j])==(reach[i][j] && reach[j][i]));
  }
  for (int trial=0;trial<300;++trial) {
    int n=1+rnd(5),q=rnd(12); TwoSAT sat(n);
    struct Clause { int x,y;bool a,b; };
    vector<Clause> clauses;
    for (int i=0;i<q;++i) {
      Clause z{rnd(n),rnd(n),bool(rnd(2)),bool(rnd(2))};
      clauses.push_back(z);sat.add_or(z.x,z.a,z.y,z.b);
    }
    bool feasible=false;
    for (int mask=0;mask<(1<<n);++mask) {
      bool ok=true;
      for (auto z:clauses) ok &= ((bool(mask&(1<<z.x))==z.a) || (bool(mask&(1<<z.y))==z.b));
      feasible |= ok;
    }
    auto got=sat.solve();assert(bool(got)==feasible);
    if (got) for (auto z:clauses) assert((got->at(z.x)==z.a) || (got->at(z.y)==z.b));
  }

  // Bridges: remove each edge and compare connected-component count.
  for (int trial=0;trial<220;++trial) {
    int n=2+rnd(6),m=rnd(12); Bridges b(n);
    vector<pair<int,int>> edges;
    for (int i=0;i<m;++i) {
      int u=rnd(n),v=rnd(n);edges.push_back({u,v});b.add_edge(u,v,i);
    }
    auto components_without=[&](int ban) {
      vector<int> p(n);iota(p.begin(),p.end(),0);
      auto find=[&](int x){while(p[x]!=x)x=p[x];return x;};
      for (int i=0;i<m;++i) if (i!=ban) {
        auto [u,v]=edges[i];p[find(u)]=find(v);
      }
      set<int> roots;for(int i=0;i<n;++i)roots.insert(find(i));
      return int(roots.size());
    };
    int base=components_without(-1);
    auto found=b.find();set<int> got(found.begin(),found.end());
    for (int i=0;i<m;++i) assert(got.count(i)==size_t(components_without(i)>base));
  }

  // Max flow equals minimum s-t cut for small networks.
  for (int trial=0;trial<180;++trial) {
    int n=2+rnd(6);Dinic d(n);vector<tuple<int,int,int>> edges;
    for (int i=0;i<2*n;++i) {
      int u=rnd(n),v=rnd(n),cap=rnd(6);
      d.add_edge(u,v,cap);edges.push_back({u,v,cap});
    }
    long long best=LLONG_MAX;
    for (int mask=0;mask<(1<<n);++mask) if ((mask&1) && !(mask&(1<<(n-1)))) {
      long long cut=0;
      for (auto [u,v,c]:edges) if ((mask&(1<<u)) && !(mask&(1<<v)))cut+=c;
      best=min(best,cut);
    }
    assert(d.max_flow(0,n-1)==best);
  }

  // Bipartite matching against brute force.
  for (int trial=0;trial<160;++trial) {
    int nl=1+rnd(6),nr=1+rnd(6);HopcroftKarp h(nl,nr);
    for (int u=0;u<nl;++u)for(int v=0;v<nr;++v)if(rnd(2))h.add_edge(u,v);
    auto dfs=[&](auto &&self,int u,int used)->int {
      if(u==nl)return 0;
      int best=self(self,u+1,used);
      for(int v:h.g[u])if(!(used&(1<<v)))best=max(best,1+self(self,u+1,used|(1<<v)));
      return best;
    };
    int want=dfs(dfs,0,0);
    assert(h.max_matching()==want);
    assert(h.max_matching()==want);
  }
  for (int trial=0;trial<160;++trial) {
    int n=1+rnd(5),m=rnd(8);EulerWalk e(n);
    vector<pair<int,int>> ed;
    for(int i=0;i<m;++i){int u=rnd(n),v=rnd(n);e.add_edge(u,v);ed.push_back({u,v});}
    auto possible=[&](auto &&self,int u,int used)->bool {
      if(used==(1<<m)-1)return true;
      for(int i=0;i<m;++i)if(!(used&(1<<i))) {
        auto [a,b]=ed[i];
        if(a==u && self(self,b,used|(1<<i)))return true;
        if(b==u && self(self,a,used|(1<<i)))return true;
      }
      return false;
    };
    bool feasible=(m==0);
    for(int u=0;u<n;++u)feasible|=possible(possible,u,0);
    auto got=e.walk();assert(bool(got)==feasible);
    if(got){
      assert(int(got->size())==m+1);
      multiset<pair<int,int>> want,actual;
      for(auto [u,v]:ed)want.insert(minmax(u,v));
      for(int i=1;i<int(got->size());++i)actual.insert(minmax((*got)[i-1],(*got)[i]));
      assert(want==actual);
    }
  }

  // Mo with non-invertible distinct-count answers and ordinary range sums.
  for (int trial=0;trial<150;++trial) {
    int n=1+rnd(35),q=1+rnd(35);vector<int>a(n);
    for(auto &x:a)x=rnd(9);
    vector<MoQuery> qs;
    for(int i=0;i<q;++i){int l=rnd(n),r=rnd(n);if(l>r)swap(l,r);qs.push_back({l,r,i});}
    array<int,9> freq{};int distinct=0;
    auto add=[&](int i){if(freq[a[i]]++==0)++distinct;};
    auto remove=[&](int i){if(--freq[a[i]]==0)--distinct;};
    auto got=mo_process<int>(n,qs,add,remove,[&](){return distinct;});
    for(auto z:qs){set<int>s;for(int i=z.l;i<=z.r;++i)s.insert(a[i]);assert(got[z.id]==int(s.size()));}
  }

  // Rectangular Hungarian assignment and negative costs.
  for(int trial=0;trial<180;++trial){
    int n=1+rnd(4),m=n+rnd(3);vector<vector<long long>>a(n,vector<long long>(m));
    for(auto &row:a)for(auto &x:row)x=rnd(21)-10;
    long long best=LLONG_MAX;
    auto rec=[&](auto &&self,int i,int used,long long cost)->void {
      if(i==n){best=min(best,cost);return;}
      for(int j=0;j<m;++j)if(!(used&(1<<j)))self(self,i+1,used|(1<<j),cost+a[i][j]);
    };
    rec(rec,0,0,0);auto got=hungarian(a);assert(got.cost==best);
    set<int> columns(got.column_of_row.begin(),got.column_of_row.end());
    assert(int(columns.size())==n);
    long long cost=0;for(int i=0;i<n;++i)cost+=a[i][got.column_of_row[i]];
    assert(cost==best);
  }

  // String tools against direct enumeration.
  for(int trial=0;trial<170;++trial){
    int n=rnd(25);string s;for(int i=0;i<n;++i)s+=char('a'+rnd(3));
    auto z=z_function(s);
    auto p=manacher(s);
    for(int i=1;i<n;++i){int want=0;while(i+want<n && s[want]==s[i+want])++want;assert(z[i]==want);}
    for(int i=0;i<n;++i){
      int odd=0,even=0;
      while(i-odd>=0 && i+odd<n && s[i-odd]==s[i+odd])++odd;
      while(i-even-1>=0 && i+even<n && s[i-even-1]==s[i+even])++even;
      assert(p.odd[i]==odd && p.even[i]==even);
    }
    SuffixArray sa(s);vector<int> expected(n);iota(expected.begin(),expected.end(),0);
    sort(expected.begin(),expected.end(),[&](int a,int b){return s.substr(a)<s.substr(b);});
    assert(sa.sa==expected);
    for(int i=1;i<n;++i){int k=0;while(sa.sa[i]+k<n && sa.sa[i-1]+k<n && s[sa.sa[i]+k]==s[sa.sa[i-1]+k])++k;assert(sa.lcp[i]==k);}
    AhoCorasick ac;vector<string> patterns;
    for(int j=0;j<5;++j){string p;for(int k=rnd(4)+1;k--;)p+=char('a'+rnd(3));patterns.push_back(p);ac.add(p);}
    ac.build();long long count=0;
    for(auto &p:patterns)for(int i=0;i+int(p.size())<=n;++i)count+=(s.substr(i,p.size())==p);
    assert(ac.count_matches(s)==count);
    DoubleHash dh(s);
    for(int a=0;a<=n;++a)for(int b=a;b<=n;++b)
      for(int c=0;c<=n;++c)if(c+b-a<=n)
        assert((s.substr(a,b-a)==s.substr(c,b-a))==(dh.get(a,b)==dh.get(c,c+b-a)));
  }

  // CRT, totients, primality.
  for(int m=1;m<15;++m)for(int n=1;n<15;++n)for(int a=-2;a<3;++a)for(int b=-2;b<3;++b){
    auto got=crt(a,m,b,n);int l=lcm(m,n),want=-1;
    for(int x=0;x<l;++x)if((x-a)%m==0 && (x-b)%n==0){want=x;break;}
    assert(bool(got)==(want!=-1));if(got)assert(got->first==want && got->second==l);
  }
  auto phi=phi_sieve(500);
  for(int x=1;x<=500;++x){int want=0;for(int y=1;y<=x;++y)want+=(gcd(x,y)==1);assert(phi[x]==want);}
  for(int x=0;x<100000;++x){bool prime=x>=2;for(int p=2;p*p<=x;++p)if(x%p==0)prime=false;assert(is_prime(x)==prime);}
  assert(is_prime(18446744073709551557ULL));
  assert(!is_prime(18446744073709551615ULL));
  assert(pow_mod(42,0,1)==0);
  assert(pow_mod(42,100,1)==0);

  // Integer geometry: intersections, hull, area, boundary and circle tangency.
  IPoint a{0,0},b{4,0},c{4,4},d{0,4};
  assert(segments_intersect(a,c,b,d));
  assert(segments_intersect(a,b,{2,0},{7,0}));
  assert(!segments_intersect(a,b,{5,0},{7,0}));
  vector<IPoint> square{a,b,c,d};
  assert(area2(square)==32);
  assert(point_in_polygon(square,{2,2})==1);
  assert(point_in_polygon(square,{0,2})==0);
  assert(point_in_polygon(square,{5,2})==-1);
  auto hull=convex_hull({a,b,c,d,{2,2},{0,0}});
  assert(hull==square);
  assert(convex_hull({{0,0},{1,1},{2,2}}).size()==2);
  auto hits=circle_line({0,0},5,{-10,0},{10,0});
  assert(hits.size()==2 && fabsl(hits[0].x+5)<1e-10 && fabsl(hits[1].x-5)<1e-10);
  assert(circle_line({0,0},5,{-10,5},{10,5}).size()==1);
  assert(circle_line({0,0},5,{-10,6},{10,6}).empty());
  assert(circle_line({0,0},1e-7L,{-1,0},{1,0}).size()==2);
  assert(circle_line({0,0},1,{0,0},{1e-7L,0}).size()==2);

  cout << "All reference behavior checks passed.\n";
}
