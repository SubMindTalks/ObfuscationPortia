import random
import ast
import astor

# Sample rewriting rules
def rewrite_static_to_function(node):
    """Rewrite static values as function outputs."""
    if isinstance(node, ast.Constant):
        value = node.value
        if isinstance(value, (int, float)):
            # Replace constant with a function call
            return ast.Call(
                func=ast.Name(id=f"generate_static_{value}", ctx=ast.Load()),
                args=[],
                keywords=[]
            )
    return node

def rewrite_if_to_while(node):
    """Rewrite an if-statement as a while-statement with break."""
    if isinstance(node, ast.If):
        return ast.While(
            test=node.test,
            body=node.body + [ast.Break()],
            orelse=node.orelse
        )
    return node

def split_expression(node):
    """Split a simple expression into multiple statements."""
    if isinstance(node, ast.BinOp):
        temp_var = f"temp_{random.randint(1000, 9999)}"
        new_assign = ast.Assign(
            targets=[ast.Name(id=temp_var, ctx=ast.Store())],
            value=node.left
        )
        new_binop = ast.BinOp(
            left=ast.Name(id=temp_var, ctx=ast.Load()),
            op=node.op,
            right=node.right
        )
        return [new_assign, new_binop]
    return node

# Apply random rewriting rules
def apply_random_transformations(tree, rules, iterations=3):
    for _ in range(iterations):
        rule = random.choice(rules)
        transformer = CustomTransformer(rule)
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)
    return tree

# Custom NodeTransformer
class CustomTransformer(ast.NodeTransformer):
    def __init__(self, transformation):
        self.transformation = transformation

    def visit(self, node):
        node = self.transformation(node)
        return super().visit(node)

# Example: Static value function generator
def generate_static_functions(values):
    functions = []
    for value in values:
        func_code = f"""
def generate_static_{value}():
    return {value}
"""
        functions.append(func_code)
    return "\n".join(functions)

# Example Usage
if __name__ == "__main__":
    # Original code block
    original_code = """
def test_func(x, y):
    if x > y:
        return x + y
    else:
        return x - y
"""

    # Parse the code into an AST
    tree = ast.parse(original_code)

    # Rewriting rules
    rules = [rewrite_static_to_function, rewrite_if_to_while, split_expression]

    # Apply transformations
    transformed_tree = apply_random_transformations(tree, rules)

    # Generate supporting static functions
    static_functions = generate_static_functions(range(1, 101))  # Example range

    # Convert back to source code
    transformed_code = astor.to_source(transformed_tree)

    # Combine with helper functions
    final_code = static_functions + "\n\n" + transformed_code

    print("Original Code:")
    print(original_code)
    print("\nObfuscated Code:")
    print(final_code)
