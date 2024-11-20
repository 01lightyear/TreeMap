from random import shuffle
def find_place(sorted_array, target):
    low=0
    end=len(sorted_array)-1
    while low <= end:
        mid = (low + end) // 2
        if sorted_array[mid] == target:
            return mid
        elif sorted_array[mid] < target:
            low = mid + 1
        else:
            end = mid - 1
    return low
class Node:
    def __init__(self,keys,father=None,children=None):
        self.keys=keys
        self.father=father
        self.children=children
    def __repr__(self):
        return str(self.keys)
def search(root,target):
    temp=find_place(root.keys,target)
    if temp<len(root.keys) and root.keys[temp]==target:
        return root,temp
    if not root.children:
        return None
    return search(root.children[temp],target)
class BTree:
    t=None
    def __init__(self,t,root=None):
        self.t=t
        self.root=root
    def print(self,node=None,level=0):
        if not node:
            node=self.root
            if not node:
                print("B树为空")
                return 
        print('    ' * level + str(node.keys))
        if node.children:
            for child in node.children:
                self.print(child,level+1)
    def insert(self, target):
        if self.root is None:
            self.root = Node(keys=[target])
            return
        if search(self.root,target):
                    return
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            self.split(root)  # 修改这里，传入需要分裂的节点
            self.root = root.father
        self._insert_non_full(self.root,target)
    def _insert_non_full(self, node, target):
        i = len(node.keys) - 1
        if node.children is None:
            # 节点是叶子节点，直接插入
            node.keys.insert(find_place(node.keys,target),target)
        else:
            # 节点不是叶子节点，找到子节点
            while i >= 0 and target < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.split(node.children[i])  # 传入需要分裂的子节点
                if target > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], target)

    def split(self, node_to_split):
        parent = node_to_split.father
        if parent is None:
            # 如果要分裂的节点是根节点，需要创建一个新的根
            parent = Node(keys=[], children=[node_to_split])
            self.root = parent
            node_to_split.father = parent

        # 找到 node_to_split 在 parent.children 中的索引
        index = parent.children.index(node_to_split)

        t = self.t
        new_node = Node(
            keys=node_to_split.keys[t:], 
            father=parent, 
            children=node_to_split.children[t:] if node_to_split.children else None
        )
        if new_node.children:
            for child in new_node.children:
                child.father=new_node

        # 中间键上移到父节点
        insert_pos = find_place(parent.keys, node_to_split.keys[t - 1])
        parent.keys.insert(insert_pos, node_to_split.keys[t - 1])
        parent.children.insert(insert_pos + 1, new_node)

        # 更新被分割的节点
        node_to_split.keys = node_to_split.keys[:t - 1]
        node_to_split.children = node_to_split.children[:t] if node_to_split.children else None
    def find_predecessor(self,node):
        while node.children:
            node=node.children[-1]
        return node.keys[-1]
    def find_successor(self,node):
        while node.children:
            node=node.children[0]
        return node.keys[0]
    def rebalance_after_merge(self, node):

    #处理合并后父节点键数量不足的情况

        if node == self.root:
            if len(node.keys) == 0 and node.children:
                self.root = node.children[0]
                self.root.father = None
            return

        parent = node.father
        if len(parent.keys) >= self.t - 1:
            return

        index = parent.children.index(node)

        # 尝试从左兄弟借键
        if index > 0 and len(parent.children[index - 1].keys) > self.t - 1:
            left_sibling = parent.children[index - 1]
            borrowed_key = left_sibling.keys.pop(-1)
            parent_key = parent.keys[index - 1]
            parent.keys[index - 1] = borrowed_key
            node.keys.insert(0, parent_key)
            if left_sibling.children:
                borrowed_child = left_sibling.children.pop(-1)
                node.children.insert(0, borrowed_child)
                borrowed_child.father = node
            return

        # 尝试从右兄弟借键
        if index < len(parent.children) - 1 and len(parent.children[index + 1].keys) > self.t - 1:
            right_sibling = parent.children[index + 1]
            borrowed_key = right_sibling.keys.pop(0)
            parent_key = parent.keys[index]
            parent.keys[index] = borrowed_key
            node.keys.append(parent_key)
            if right_sibling.children:
                borrowed_child = right_sibling.children.pop(0)
                node.children.append(borrowed_child)
                borrowed_child.father = node
            return

        # 合并左兄弟
        if index > 0:
            left_sibling = parent.children[index - 1]
            parent_key = parent.keys.pop(index - 1)
            parent.children.pop(index)
            left_sibling.keys.append(parent_key)
            left_sibling.keys += node.keys
            if node.children:
                for child in node.children:
                    left_sibling.children.append(child)
                    child.father = left_sibling
            self.rebalance_after_merge(parent)
            return

        # 合并右兄弟
        right_sibling = parent.children[index + 1]
        parent_key = parent.keys.pop(index)
        parent.children.pop(index + 1)
        node.keys.append(parent_key)
        node.keys += right_sibling.keys
        if right_sibling.children:
            for child in right_sibling.children:
                node.children.append(child)
                child.father = node
        self.rebalance_after_merge(parent)
    def delete(self,target,node):
        if search(node,target):
            root,position=search(node,target)
        else: return
        if root.children:#非叶子
            newkey=self.find_predecessor(root.children[position])
            root.keys[position]=newkey
            self.delete(newkey,root.children[position])
        else:#叶子
            if len(root.keys)>=self.t:
                root.keys.remove(target)
                return
            else:
                if not root.father:#根
                    root.keys.remove(target)
                    return
                index=root.father.children.index(root)
                if index > 0 and len(root.father.children[index - 1].keys) > self.t - 1:
                    # 从左兄弟借键
                    renter = root.father.children[index - 1]
                    root.keys.insert(0, root.father.keys[index - 1])
                    root.father.keys[index - 1] = renter.keys.pop(-1)
                    if renter.children:
                        borrowed_child = renter.children.pop(-1)
                        root.children.insert(0, borrowed_child)
                        borrowed_child.father = root
                    root.keys.remove(target)
                elif index < len(root.father.children) - 1 and len(root.father.children[index + 1].keys) > self.t - 1:
                    # 从右兄弟借键
                    renter = root.father.children[index + 1]
                    root.keys.append(root.father.keys[index])
                    root.father.keys[index] = renter.keys.pop(0)
                    if renter.children:
                        borrowed_child = renter.children.pop(0)
                        root.children.append(borrowed_child)
                        borrowed_child.father = root
                    root.keys.remove(target)
                else:
                    # 合并左兄弟或右兄弟
                    if index > 0:
                        left_sibling = root.father.children[index - 1]
                        parent_key = root.father.keys.pop(index - 1)
                        root.father.children.pop(index)
                        left_sibling.keys.append(parent_key)
                        root.keys.remove(target)
                        left_sibling.keys += root.keys
                        if root.children:
                            for child in root.children:
                                left_sibling.children.append(child)
                                child.father = left_sibling
                        self.rebalance_after_merge(left_sibling.father)
                    else:
                        right_sibling = root.father.children[index + 1]
                        parent_key = root.father.keys.pop(index)
                        root.father.children.pop(index + 1)
                        root.keys.append(parent_key)
                        root.keys += right_sibling.keys
                        root.keys.remove(target)
                        if right_sibling.children:
                            for child in right_sibling.children:
                                root.children.append(child)
                                child.father = root
                        self.rebalance_after_merge(root.father)
                    
def main():
    btree = BTree(t=2)
    keys_to_insert = [12, 5, 6, 10, 7, 20, 17, 30]
    #shuffle(keys_to_insert)
    print("插入顺序:", keys_to_insert)
    for key in keys_to_insert:
        btree.insert(key)
    btree.print()
    #shuffle(keys_to_insert)
    keys_to_insert=[30, 5, 12, 10, 6, 20, 17, 7]
    print("删除顺序:", keys_to_insert)
    for key in keys_to_insert:
        print(f"删除{key}")
        btree.delete(key,btree.root)
        btree.print()
if __name__=="__main__":
    main()