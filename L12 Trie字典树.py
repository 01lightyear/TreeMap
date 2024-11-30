class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False  # 标记是否为单词的结束

class Trie:
    def __init__(self):
        self.root = TrieNode()
        
    def insert(self, word):
        node = self.root
        for char in word:
            # 如果子节点中没有当前字符，则添加
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True  # 标记单词结束
    
    def search(self, word):
        node = self.root
        for char in word:
            # 如果在子节点中找不到字符，返回 False
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word  # 检查是否为完整单词
        
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            # 如果在子节点中找不到字符，返回 False
            if char not in node.children:
                return False
            node = node.children[char]
        return True  # 前缀存在
    
    def delete(self,word):
        def _delete(node,word,depth):
            if not node:
                return False#节点不存在即word不存在
            if depth==len(word):#到达word最后一位
                if not node.is_end_of_word:
                    return False#单词不存在
                node.is_end_of_word=False
                return len(node.children)==0#如果该节点有孩子，则只需删除当前节点“作为end”的属性即可，返回False终止递归
            char=word[depth]
            if char not in node.children:
                return False#单词不存在
            should_delete_child=_delete(node.children[char],word,depth+1)
            if should_delete_child:
                del node.children[char]
                #如果当前节点不是结束节点也没有孩子，则需要删除
                return not node.is_end_of_word and len(node.children)==0
            return False
        _delete(self.root,word,0)
    def count_words_with_prefix(self,prefix):
        node=self.root
        for char in prefix:
            if not char in node.children:
                return 0
            node=node.children[char]
        def _count_words(node):
            count=1 if node.is_end_of_word else 0
            for child in node.children.values():
                count+=_count_words(child)
            return count
        return _count_words(node)
def main():
    trie = Trie()
    trie.insert("apple")
    trie.insert("app")
    trie.insert("application")
    trie.insert("banana")
    print(trie.count_words_with_prefix("app"))  # 输出 3
    trie.delete("app")
    print(trie.search("app"))                   # 输出 False
    print(trie.count_words_with_prefix("app"))  # 输出 2
if __name__=='__main__':
    main()