from flask import Flask, render_template, request, jsonify
import sys
import os

# Ensure the 'src' directory is visible
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from lexer import lexer
from parser import parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    source_code = request.form.get('code', '')
    
    try:
        # 1. Parse
        ast = parser.parse(source_code)
        if not ast:
            return jsonify({'error': 'Syntax Error: Check your code structure.'})

        # 2. Semantic Analysis
        sa = SemanticAnalyzer()
        sa.analyze(ast)
        symbol_table = str(sa.symbol_table)

        # 3. Code Gen (TAC)
        cg = CodeGenerator()
        cg.generate_tac(ast)
        tac_code = "\n".join(cg.tac)

        # 4. Target Code
        stack_code = "\n".join(cg.get_stack_code())

        return jsonify({
            'ast': str(ast),
            'symbol_table': symbol_table,
            'tac': tac_code,
            'stack_code': stack_code
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)