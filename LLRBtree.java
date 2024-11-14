package TreeMap.LeftLeaningRedBlackTree;
import java.util.Scanner;
import java.util.Arrays;
import java.util.Collections;
public class LLRBtree{
    public static class Node<T extends Comparable<T>>{
        int color=0;//0 represents red, 1 represents black
        Node<T> father,left,right;
        T key;
        Node(Node<T> left,Node<T> right,T key){
            this.left=left;
            this.right=right;
            this.key=key;
            this.color=0;
            this.father=null;
        }
        Node(T key,int color){
            this.key=key;
            this.color=color;
            this.left=null;
            this.right=null;
            this.father=null;
        }
        public boolean isValidRedBlackTree() {
            // 检查根节点是否为黑色
            if (this != null && this.color == 0) {
                return false; // 根节点必须是黑色
            }
    
            // 计算黑高并检查是否一致
            return getBlackHeight(this) != -1; // 如果返回 -1，表示树不合法
        }
    
        // 计算黑高并检查是否满足红黑树性质
        private int getBlackHeight(Node<T> node) {
            if (node == null) {
                return 1; // 空节点视为黑色，返回黑高1
            }
    
            // 递归计算左右子树的黑高
            int leftHeight = getBlackHeight(node.left);
            int rightHeight = getBlackHeight(node.right);
    
            // 如果左右子树的黑高不一致，返回 -1
            if (leftHeight == -1 || rightHeight == -1 || leftHeight != rightHeight) {
                return -1; // 不一致，红黑树性质不满足
            }
    
            // 如果当前节点是红色，黑高不变；如果是黑色，黑高加1
            return (node.color == 0 ? 0 : 1) + leftHeight; // 红色不加黑高，黑色加1
        }    
    }
    public static <T extends Comparable<T>> Node<T> maxnode(Node<T> root){
        if(root==null)
            return root;
        while(root.right!=null){
            root=root.right;
        }
        return root;
    }
    public static <T extends Comparable<T>> Node<T> minnode(Node<T> root){
        if(root==null)
            return root;
        while(root.left!=null){
            root=root.left;
        }
        return root;
    }
    public static <T extends Comparable<T>> void display(Node<T> root, String indent, boolean last) {//0 represents that the current node is a left child, while 1 for the right child
        if (root != null) {
            System.out.print(indent);
            if (last) {
                System.out.print("R····");
                indent += "   ";
            } else {
                System.out.print("L····");
                indent += "|  ";
            }
            System.out.println(root.key + (root.color == 0 ? " (R)" : " (B)"));
            display(root.right, indent, true);
            display(root.left, indent, false);
        }
    }
    public static <T extends Comparable<T>> Node<T> search(Node<T> root,T target){
        if(root.key==null)
            return null;
        else if(root.key.compareTo(target)<0)
            return search(root.right,target);
        else if(root.key.compareTo(target)>0)
            return search(root.left,target);
        else
            return root;//return the node whose key is target
    }
    public static <T extends Comparable<T>> Node<T> LeftRotate(Node<T> root,Node<T> target){
        Node<T> x=target,y=target.right;
        x.right=y.left;
        y.left=x;
        if(x.father==null){
            y.father=null;
            root=y;
        }
        else{
            y.father=x.father;
            if(x.key==x.father.left.key)
                x.father.left=y;
            else
                x.father.right=y;
        }
        x.father=y;
        if(x.right!=null)
            x.right.father=x;
        return root;
    }
    public static <T extends Comparable<T>> Node<T> RightRotate(Node<T> root,Node<T> target){
        Node<T> x=target,y=target.left;
        x.left=y.right;
        y.right=x;
        if(x.father==null){
            y.father=null;
            root=y;
        }
        else{
            y.father=x.father;
            if(x==x.father.left)
                x.father.left=y;
            else
                x.father.right=y;
        }
        x.father=y;
        if(x.left!=null)
            x.left.father=x;
        return root;
    }
    public static <T extends Comparable<T>> Node<T> insert(Node<T> root, T key){
        Node<T> newnode=new Node<>(null,null,key);
        root=insertnode(root,newnode);
        root=fixviolation(root,newnode);
        return root;
    }
    public static <T extends Comparable<T>> Node<T> insertnode(Node<T> root,Node<T> newnode){
        if (root == null) {
            return newnode;
        }
        if (newnode.key.compareTo(root.key) < 0) {
            if(root.left!=null)
                root.left = insertnode(root.left, newnode);
            else{
                root.left=newnode;
                newnode.father=root;
            }
        } else if(newnode.key.compareTo(root.key)>0) {
            if(root.right!=null)
                root.right = insertnode(root.right, newnode);
            else{
                root.right=newnode;
                newnode.father=root;
            }
        }
        return root; 
    }
    public static <T extends Comparable<T>> Node<T> fixviolation(Node<T> root,Node<T> node){
        while (node != null && node.key!= root.key && node.father != null && node.father.color == 0) {
            Node<T> parent = node.father;
            Node<T> grandparent = parent.father;
            if (parent == grandparent.left) {
                Node<T> uncle = grandparent.right;
                if (uncle != null && uncle.color == 0) {
                    parent.color = 1;
                    uncle.color = 1;
                    grandparent.color = 0;
                    node = grandparent;
                } else {
                    if (node == parent.right) {
                        root = LeftRotate(root, parent);
                        node = parent;
                        parent = node.father;
                    }
                    parent.color = 1;
                    grandparent.color = 0;
                    root = RightRotate(root, grandparent);
                }
            } else {
                Node<T> uncle = grandparent.left;

                if (uncle != null && uncle.color == 0) {
                    parent.color = 1;
                    uncle.color = 1;
                    grandparent.color = 0;
                    node = grandparent;
                } else {
                    if (node == parent.left) {
                        root = RightRotate(root, parent);
                        node = parent;
                        parent = node.father;
                    }
                    parent.color = 1;
                    grandparent.color = 0;
                    root = LeftRotate(root, grandparent);
                }
            }
        }
        root.color = 1;
        return root;
    }
    public static <T extends Comparable<T>> Node<T> fixdoubleblacknode(Node<T> root,Node<T> node){//fix double black node during deletion
        Node<T> brother;
        if(node.father==null){
            node.color=1;
            return root;
        }
        else if(node==node.father.right)
            brother=node.father.left;
        else 
            brother=node.father.right;
        if(brother.color==1){
            if(brother.left!=null&&brother.left.color==0||brother.right!=null&&brother.right.color==0){//brother has at least one red child
                if(brother.left!=null&&brother.left.color==0){
                    if(brother==brother.father.left){// father brother and nephew form the LL type(L for leftchild and R for rightchild)
                        brother.left.color=brother.color;
                        brother.color=brother.father.color;
                        brother.father.color=1;
                        root=RightRotate(root, brother.father);
                    }
                    else if(brother==brother.father.right){//father brother and nephew form the RL type
                        brother.left.color=brother.father.color;
                        brother.father.color=1;
                        root=RightRotate(root, brother);
                        root=LeftRotate(root, node.father);
                    }
                }
                else if(brother.right!=null&&brother.right.color==0){//father brother and nephew form the RR type
                    if(brother.key==brother.father.right.key){
                        brother.right.color=brother.color;
                        brother.color=brother.father.color;
                        brother.father.color=1;
                        root=LeftRotate(root, brother.father);
                    }
                    else if(brother.key==brother.father.left.key){//father brother and nephew form the LR type
                        brother.right.color=brother.father.color;
                        brother.father.color=1;
                        root=LeftRotate(root, brother);
                        root=RightRotate(root, node.father);
                    }
                }
            }
            else{
                brother.color=0;
                if(node.father.color==0||node.father.father==null)
                    node.father.color=1;
                else
                    return fixdoubleblacknode(root, node.father);
            }
        }
        else{//red brother
            int tmp=brother.color;
            brother.color=brother.father.color;
            brother.father.color=tmp;
            if(node==node.father.right){
                root=RightRotate(root, node.father);
            }
            else{
                root=LeftRotate(root, node.father);
            }
            /*if(node.father.color==0)
                node.father.color=1;
            else if(node.father.father!=null){
                return fixdoubleblacknode(root, node.father);
            }*/
            return fixdoubleblacknode(root, node);
        }
        return root;
    }
    public static <T extends Comparable<T>> Node<T> delete(Node<T> root, T target){
        Node<T> node=search(root,target);
        if(node==null)
            return root;
        if(node.color==0&&node.right==null&&node.left==null){//red leaf
            if(node==node.father.right){
                node.father.right=null;
                return root;
            }
            else{
                node.father.left=null;
                return root;
            }
        }
        else if(node.left!=null&&node.right!=null){//has two children
            if(node.left!=null){
                T tmpkey=maxnode(node.left).key;
                root=delete(root, maxnode(node.left).key);
                node.key=tmpkey;
            }
            else if(node.right!=null){
                T tmpkey=minnode(node.right).key;
                root=delete(root,minnode(node.right).key);
                node.key=tmpkey;
            }
            else root=null;
        }
        else if(node.left==null&&node.right==null){//leaf
            if(node.color==0){//red leaf
                if(node==node.father.left)
                    node.father.left=null;
                else
                    node.father.right=null;
            }
            else{//black leaf
                Node<T> brother;
                if(node.father.left==node)
                    brother=node.father.right;
                else
                    brother=node.father.left;
                if(brother.color==1){//black brother
                    if(brother.left!=null&&brother.left.color==0||brother.right!=null&&brother.right.color==0){//brother has at least one red child
                        if(brother.left!=null&&brother.left.color==0){
                            if(brother==brother.father.left){// father brother and nephew form the LL type(L for leftchild and R for rightchild)
                                brother.left.color=brother.color;
                                brother.color=brother.father.color;
                                brother.father.color=1;
                                root=RightRotate(root, brother.father);
                                node.father.right=null;
                            }
                            else if(brother==brother.father.right){//father brother and nephew form the RL type
                                brother.left.color=brother.father.color;
                                brother.father.color=1;
                                root=RightRotate(root, brother);
                                root=LeftRotate(root, node.father);
                                node.father.left=null;
                            }
                        }
                        else if(brother.right!=null&&brother.right.color==0){
                            if(brother==brother.father.right){//father brother and nephew form the RR type
                                brother.right.color=brother.color;
                                brother.color=brother.father.color;
                                brother.father.color=1;
                                root=LeftRotate(root, brother.father);
                                node.father.left=null;
                            }
                            else if(brother==brother.father.left){//father brother and nephew form the LR type
                                brother.right.color=brother.father.color;
                                brother.father.color=1;
                                root=LeftRotate(root, brother);
                                root=RightRotate(root, node.father);
                                node.father.right=null;
                            }
                        }
                    }
                    else{//brother has no red child
                        brother.color=0;
                        if(node==node.father.right)
                            node.father.right=null;
                        else
                            node.father.left=null;
                        if(node.father.father!=null){
                            if(node.father.color==0)
                                node.father.color=1;
                            else{
                                root=fixdoubleblacknode(root, node.father);
                            }
                        }
                    }
                }
                else{//red brother
                    int tmp=brother.color;
                    brother.color=brother.father.color;
                    brother.father.color=tmp;
                    if(node==node.father.right){
                        root=RightRotate(root, node.father);
                        root=delete(root,node.key);
                    }
                    else{
                        root=LeftRotate(root, node.father);
                        root=delete(root, node.key);
                    }
                }
            }
        }
        else if((node.left==null||node.right==null)&&node.father==null){
            if(node.left!=null){
                node.key=node.left.key;
                node.left=null;
                return root;
            }
            else if(node.right!=null){
                node.key=node.right.key;
                node.right=null;
                return root;
            }
            else root=null;
        }
        else if(node.left==null&&node.color==1){//black node with one right red leaf
            node.right.father=node.father;
            if(node.father.left!=null&&node==node.father.left)
                node.father.left=node.right;
            else
                node.father.right=node.right;
            node.right.color=1;
        }
        else if(node.right==null&&node.color==1){//black node with one left red leaf
            node.left.father=node.father;
            if(node==node.father.left)
                node.father.left=node.left;
            else
                node.father.right=node.left;
            node.left.color=1;
        }
        return root;
    }
    public static void main(String[] args){
        Node<Integer> tree=null;
        Integer[] numbers = new Integer[100];
        for (int i = 0; i < 100; i++) {
            numbers[i] = i + 1;
        }
        Collections.shuffle(Arrays.asList(numbers));
        for (int number : numbers) {
            System.out.println("insert: " + number);
            tree=insert(tree,number); 
        }
        display(tree,"", true);
        Collections.shuffle(Arrays.asList(numbers));
        for (int i=0;i<99;i++) {
            System.out.println("delete: " + numbers[i]);
            tree=delete(tree,numbers[i]); 
            display(tree,"",true); 
            System.out.println("validation:"+tree.isValidRedBlackTree());
            if(tree.isValidRedBlackTree()==false)
                break;
        }
    }
    public static void linkParentChild(Node<T> parent) {
        if (parent == null) return;
        if (parent.left != null) parent.left.father = parent;
        if (parent.right != null) parent.right.father = parent;
        
        linkParentChild(parent.left);
        linkParentChild(parent.right);
    }
}