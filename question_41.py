class DeepFlatten:
    def __init__(self):
        self.result = []
    def deep_flatten(self,inp):
        if isinstance(inp,list):
            for ele in inp:
                self.deep_flatten(ele)
        else:
            self.result.append(inp)
        
testcases = [[1, [2, [3, 4], [5, [6, 7]]], 8],[[['a']], 'b', ['c', ['d']]],[],[1, 2, 3],[1, ['a', [True, [3.5]]], 'end'],[[[[[10]]]]],[[], [[], []], 1],[[1, 2], 3, [4, [5, []]], 6]]
for test in testcases:
    df = DeepFlatten()
    df.deep_flatten(test)
    print(df.result)