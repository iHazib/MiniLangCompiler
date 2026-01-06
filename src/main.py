import sys
import os
from pprint import pprint
from lexer import lexer
from parser import parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

def compile_minilang(source_code, filename="Input"):
    print(f"\n{'='*20} Compiling: {filename} {'='*20}")

    # Phase 1: Lexical & Syntax Analysis
    print("\n[Phase 1] Lexical & Syntax Analysis...")
    ast = parser.parse(source_code)
    
    if ast:
        print("Success: Abstract Syntax Tree (AST) Generated:")
        pprint(ast)
    else:
        print("Failure: Syntax errors found.")
        return

    # Phase 2: Semantic Analysis
    print("\n[Phase 2] Semantic Analysis & Symbol Table...")
    try:
        sa = SemanticAnalyzer()
        sa.analyze(ast)
        print("Success: Semantic check passed.")
        print("Final Symbol Table:", sa.symbol_table)
    except Exception as e:
        print(f"Semantic Error: {e}")
        return

    # Phase 3: Intermediate Code Generation (TAC)
    print("\n[Phase 3] Intermediate Code Generation (TAC)...")
    cg = CodeGenerator()
    cg.generate_tac(ast)
    for line in cg.tac:
        print(f"  {line}")

    # Phase 4: Target Code Generation (Stack VM)
    print("\n[Phase 4] Target Code (Stack VM Implementation)...")
    stack_code = cg.get_stack_code()
    for code in stack_code:
        print(f"  {code}")
    
    print(f"\n{'='*50}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                code = f.read()
            compile_minilang(code, file_path)
        else:
            print(f"Error: File '{file_path}' not found.")
    else:
        print("No input file detected. Running default test case...")
        default_test = """
        let x = 10;
        let y = 20;
        let z = x + y * 5;
        print z;
        """
        compile_minilang(default_test, "DefaultInternalTest")
        print("Usage Tip: Run 'python main.py tests/test1.ml' to compile a specific file.")