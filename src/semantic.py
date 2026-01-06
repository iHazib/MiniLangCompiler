class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        node_type = node[0]

        if node_type == 'program':
            for stmt in node[1]:
                self.analyze(stmt)
        
        elif node_type == 'assign':
            var_name = node[1]
            self.analyze(node[2]) 
            self.symbol_table[var_name] = 'int'
            print(f"Symbol Table Update: {var_name} declared.")

        elif node_type == 'id':
            var_name = node[1]
            if var_name not in self.symbol_table:
                raise Exception(f"Semantic Error: Variable '{var_name}' used before declaration.")

        elif node_type == 'binop':
            self.analyze(node[2])
            self.analyze(node[3])

        elif node_type == 'while':
            self.analyze(node[1]) 
            for stmt in node[2]:
                self.analyze(stmt)
        
        elif node_type == 'print':
            self.analyze(node[1])