#include <iostream>
#include <algorithm>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <deque>
#include <stack>
#include <queue>
#include <cmath>
#include <iomanip>
#include <functional>
#include <list>
#include <cstring>
#include <cstdio>
#include <fstream>
#include <stdio.h>
#include <sstream>
#include <bitset>
#include <unordered_map>
#include <unordered_set>
#include <limits>
#include <cfloat>
#include <iomanip>
#include <random>

#include <stdio.h>
#include <chrono>
#include <omp.h>

using namespace std;

#define pi 3.14159265358979323846
#define pb push_back
#define mp make_pair
#define pll pair<ll, ll>
#define rep(i,n) for(int i = 0; i < n; ++i)
#define repo(i,n) for(int i = 1; i < n; ++i)

typedef unsigned long long ull;
typedef long long ll;

ll lcm(ll a, ll b) {
    return a / __gcd(a, b) * b;
}

bool isprime(ll p) {
    if (p < 2) return false;
    if (p == 2) return true;
    if (p % 2 == 0) return false;

    double limit = sqrt(p);

    for (ll i = 3; i <= limit; i += 2) {
        if ((p % i) == 0) return false;
    }

    return true;
}

ull fac(ull n) {
    ll an = 1;
    while (n > 1)
    {
        an = (an * n) % 1000000007;
        n--;
    }
    return an;
}

ll kor(ll n, ll st) {
    ll res = 1;
    while (st) {
        if (st & 1)
            res *= n;
        n *= n;
        st >>= 1;
    }
    return res;
}

#define NMAX 1000000007
#define N 200010

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    freopen("e.in", "r", stdin);
    freopen("e.out", "w", stdout);
    int m, n;
    cin >> m >> n;
    vector<pair<int, int>> v(n);
    rep(i, n) {
        cin >> v[i].first;
        v[i].second = i;
    }
    vector<int> result;
    int best = 0;
    auto st = chrono::high_resolution_clock::now();
#pragma omp parallel for
    for (int i = 0; i < 10000; ++i) {
        random_device rd;
        mt19937 g(rd());
        shuffle(v.begin(), v.end(), g);
        int curm = 0;
        vector<int> tmp;
        rep(i, n) {
            if (curm + v[i].first <= m) {
                curm += v[i].first;
                tmp.pb(v[i].second);
            }
        }
        if (curm > best) {
            best = curm;
            result = tmp;
            // if (best == m) break;
        }
    }
    auto end = chrono::high_resolution_clock::now();
    cout << chrono::duration_cast<chrono::microseconds>(end - st).count() << endl;
    // cout << result.size() << endl;
    // rep(i, result.size()) cout << result[i] << " ";
    return 0;
}
