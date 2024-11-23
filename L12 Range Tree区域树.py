'''
n维区域树，按层数循环中分第axis维上的点（每次把中位数的点存放在该节点，把左右两部分递归构建成子树）
查询时，先检查当前节点的元素是否符合，如果符合加入到reslut中，并且将可能在当前维度上符合条件的左右子树递归进入下一维度检查处理
'''
class RangeTreeNode:
    def __init__(self, points, depth=0):
        if not points:
            self.point = None
            self.left = None
            self.right = None
            return
        k = len(points[0])
        axis = depth % k
        points.sort(key=lambda x: x[axis])
        median = len(points) // 2
        self.point = points[median]
        self.left = RangeTreeNode(points[:median], depth + 1)
        self.right = RangeTreeNode(points[median + 1:], depth + 1)

    def range_query(self, lower, upper, depth=0):
        if self.point is None:
            return []
        k = len(self.point)
        axis = depth % k
        results = []
        if all(lower[i] <= self.point[i] <= upper[i] for i in range(k)):
            results.append(self.point)
        if self.left and lower[axis] <= self.point[axis]:
            results.extend(self.left.range_query(lower, upper, depth + 1))
        if self.right and self.point[axis] <= upper[axis]:
            results.extend(self.right.range_query(lower, upper, depth + 1))
        return results
# 一维测试点集
points_1d = [1, 3, 5, 7, 9, 11]

# 构建1维区域树
tree_1d = RangeTreeNode([[x] for x in points_1d])
result_1d = tree_1d.range_query([4], [10])
print("1维查询结果:", result_1d)
# 二维测试点集
points_2d = [
    [2, 3],
    [5, 4],
    [9, 6],
    [4, 7],
    [8, 1],
    [7, 2],
    [6, 5],
    [3, 8]
]

# 构建2维区域树
tree_2d = RangeTreeNode(points_2d)
result_2d = tree_2d.range_query([4, 2], [8, 5])
print("2维查询结果:", result_2d)
# 三维测试点集
points_3d = [
    [2, 3, 5],
    [5, 4, 2],
    [9, 6, 7],
    [4, 7, 1],
    [8, 1, 3],
    [7, 2, 6],
    [6, 5, 4],
    [3, 8, 2]
]

# 构建3维区域树
tree_3d = RangeTreeNode(points_3d)
result_3d = tree_3d.range_query([4, 2, 1], [8, 5, 5])
print("3维查询结果:", result_3d)
# 四维测试点集
points_4d = [
    [2, 3, 5, 7],
    [5, 4, 2, 6],
    [9, 6, 7, 1],
    [4, 7, 1, 8],
    [8, 1, 3, 5],
    [7, 2, 6, 4],
    [6, 5, 4, 3],
    [3, 8, 2, 9]
]

# 构建4维区域树
tree_4d = RangeTreeNode(points_4d)
result_4d = tree_4d.range_query([4, 2, 1, 3], [8, 5, 5, 7])
print("4维查询结果:", result_4d)
# 五维测试点集
points_5d = [
    [2, 3, 5, 7, 9],
    [5, 4, 2, 6, 8],
    [9, 6, 7, 1, 3],
    [4, 7, 1, 8, 2],
    [8, 1, 3, 5, 4],
    [7, 2, 6, 4, 5],
    [6, 5, 4, 3, 7],
    [3, 8, 2, 9, 1]
]

# 构建5维区域树
tree_5d = RangeTreeNode(points_5d)
result_5d = tree_5d.range_query([4, 2, 1, 3, 2], [8, 5, 5, 7, 6])
print("5维查询结果:", result_5d)
