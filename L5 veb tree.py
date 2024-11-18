import math

class vanEmdeBoasTree:
    def __repr__(self) -> str:
        return self.id
    def __init__(self, u,parent_id=None):
        self.u = u
        self.min = None
        self.max = None
        if parent_id is None:
            self.id = "root"
        else:
            self.id = f"{parent_id}_c{len(getattr(self, 'cluster', []))}"
        if u > 2:
            cluster_size = math.isqrt(u)
            self.cluster = [vanEmdeBoasTree(cluster_size, self.id) for _ in range(cluster_size)]
            self.summary = vanEmdeBoasTree(cluster_size, f"{self.id}_sum")
        else:
            self.cluster = [False] * u

    def high(self, x):
        return x // math.isqrt(self.u)

    def low(self, x):
        return x % math.isqrt(self.u)

    def index(self, high, low):
        return high * math.isqrt(self.u) + low

    def empty_insert(self, x):
        self.min = self.max = x

    def insert(self, x):
        if self.min is None:
            self.empty_insert(x)
            if self.u == 2:  # 添加这个条件
                self.cluster[x] = True  # 此时整个universe即为这一个cluster
        else:
            if x < self.min:
                x, self.min = self.min, x
            if self.u > 2:
                high = self.high(x)
                low = self.low(x)
                if self.cluster[high].min is None:
                    self.summary.insert(high)
                self.cluster[high].insert(low)
            else:
                self.cluster[x] = True
            if x > self.max:
                self.max = x

    def successor(self, x):
        if self.min == None:
            return None
        if self.u == 2:
            if x < 0 or x == 0:
                return 1 if self.cluster[1] else None
            return None
        if x < self.min:
                return self.min
        if x >= self.max:
                return None
        high = self.high(x)
        low = self.low(x)
        # 在当前簇中查找
        if self.cluster[high].max is not None:
            if low < self.cluster[high].max:
                offset = self.cluster[high].successor(low)
                if offset is not None:
                    return self.index(high, offset)
        # 如果在当前簇中找不到后继（包括low等于max的情况）
        # 递归在summary中查找下一个簇
        '''next_cluster = high + 1
        while next_cluster < math.isqrt(self.u):
            if self.cluster[next_cluster].min is not None:
                offset = self.cluster[next_cluster].min
                return self.index(next_cluster, offset)
            next_cluster += 1'''
        succ_cluster = self.summary.successor(high)
        if succ_cluster is not None:
            offset = self.cluster[succ_cluster].min
            return self.index(succ_cluster, offset)
        return None

    def delete(self, x):
        if self.min == self.max:
            self.min = self.max = None
        elif self.u == 2:
            self.cluster[x] = False
            if self.cluster[0]:
                self.min = 0
                self.max = 0
            elif self.cluster[1]:
                self.min = 1
                self.max = 1
            else:
                self.min = self.max = None
        else:
            if x == self.min:
                first_cluster = self.summary.min
                if first_cluster is None:
                    self.min = self.max = None
                    return
                x = self.index(first_cluster, self.cluster[first_cluster].min)
                self.min = x
            high = self.high(x)
            low = self.low(x)
            self.cluster[high].delete(low)
            if self.cluster[high].min is None:
                self.summary.delete(high)
                if x == self.max:
                    summary_max = self.summary.max
                    if summary_max is None:
                        self.max = self.min
                    else:
                        self.max = self.index(summary_max, self.cluster[summary_max].max)
            elif x == self.max:
                self.max = self.index(high, self.cluster[high].max)
if __name__ == '__main__':
    # 创建一个universe大小为16的vEB树
    veb = vanEmdeBoasTree(16)
    
    # 测试插入操作
    print("测试插入操作：")
    numbers = [3, 7, 10, 14]
    for num in numbers:
        veb.insert(num)
        print(f"插入 {num}")
    
    # 测试后继操作
    print("\n测试后继操作：")
    for i in range(15):
        succ = veb.successor(i)
        print(f"{i} 的后继是: {succ}")
    #succ=veb.successor(6)
    # 测试删除操作
    print("\n测试删除操作：")
    delete_numbers = [7, 3, 14]
    for num in delete_numbers:
        veb.delete(num)
        print(f"删除 {num} 后，最小值为 {veb.min}，最大值为 {veb.max}")
    small_veb = vanEmdeBoasTree(2)
    small_veb.insert(1)
