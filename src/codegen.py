class CodeGenerator:
    def __init__(self):
        self.tac = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate_tac(self, node):
        node_type = node[0]

        if node_type == 'number':
            return str(node[1])
        
        elif node_type == 'id':
            return node[1]

        elif node_type == 'binop':
            left = self.generate_tac(node[2])
            right = self.generate_tac(node[3])
            temp = self.new_temp()
            self.tac.append(f"{temp} = {left} {node[1]} {right}")
            return temp

        elif node_type == 'assign':
            rhs = self.generate_tac(node[2])
            self.tac.append(f"{node[1]} = {rhs}")

        elif node_type == 'print':
            val = self.generate_tac(node[1])
            self.tac.append(f"PRINT {val}")

        elif node_type == 'program':
            for stmt in node[1]:
                self.generate_tac(stmt)

    def get_stack_code(self):
        """Converts TAC to Stack VM Code (Simplified Target Code)"""
        stack_code = []
        for line in self.tac:
            parts = line.split()
            if len(parts) == 3: # x = y
                stack_code.append(f"PUSH {parts[2]}")
                stack_code.append(f"STORE {parts[0]}")
            elif len(parts) == 5: # t1 = a + b
                stack_code.append(f"LOAD {parts[2]}")
                stack_code.append(f"LOAD {parts[4]}")
                op = "ADD" if parts[3] == "+" else "SUB" if parts[3] == "-" else "MUL"
                stack_code.append(op)
                stack_code.append(f"STORE {parts[0]}")
            elif "PRINT" in line:
                stack_code.append(f"LOAD {parts[1]}")
                stack_code.append("OUT")
        return stack_code