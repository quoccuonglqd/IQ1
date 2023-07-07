from collections import defaultdict

class BinaryLCA():
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        with open(self.file_name, "r") as f:
            self.data = f.read().split("\n")
            self.data = [i.split(" ") for i in self.data]
        
        self.name_to_id = defaultdict(int)
        self.id_to_name = defaultdict(str)
        cnt = 1
        for pair in self.data:
            for name in pair:
                if name not in self.name_to_id:
                    self.name_to_id[name] = cnt
                    self.id_to_name[str(cnt)] = name
                    cnt += 1

        self.N = cnt
        self.sibling = defaultdict(list)
        self.par = [0] * (self.N + 1)
        self.up = [[0] * 17 for _ in range(self.N+1)]

        for pair in self.data:
            u = self.name_to_id[pair[0]]
            v = self.name_to_id[pair[1]]
            self.par[v] = u
            self.sibling[u].append(v)

        self.preprocess()

    def preprocess(self):
        for u in range(1, self.N + 1):
            self.up[u][0] = self.par[u]
        for j in range(1, 17):
            for u in range(1, self.N + 1):
                self.up[u][j] = self.up[self.up[u][j - 1]][j - 1]

    def ancestor_k(self, u, k):
        for j in range(16, -1, -1):
            if k >= (1 << j):
                u = self.up[u][j]
                k -= 1 << j
        return u
    
    def find_all_sibling(self, name):
        u = self.name_to_id[name]
        return self.id_to_name[str(self.sibling[u])]
    
    def find_parent(self, name):
        u = self.name_to_id[name]
        return self.id_to_name[str(self.par[u])]
    
    def find_all_ancestor(self, name):
        u = self.name_to_id[name]
        ans = []
        u = self.par[u]
        while u:
            ans.append(self.id_to_name[str(u)])
            u = self.par[u]
        return ans
    
    def find_furthest_ancestor(self, name):
        u = self.name_to_id[name]
        for j in range(16, -1, -1):
            if self.up[u][j]:
                u = self.up[u][j]
        return self.id_to_name[str(u)]

    def check_same_ancestor(self, name1, name2):
        ancestor1 = self.find_furthest_ancestor(name1)
        ancestor2 = self.find_furthest_ancestor(name2)
        return ancestor1 == ancestor2
    
if __name__ == "__main__":
    file_name = "/media/bap/Storage/Code/IQ1/question/question3/hierarchycopy.txt"
    lca = BinaryLCA(file_name)
    import pdb; pdb.set_trace()