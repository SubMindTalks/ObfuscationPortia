import random
import ast
import astor


# Define a transformer class for obfuscation
class CodeTransformer(ast.NodeTransformer):
    def __init__(self, transformation):
        self.transformation = transformation

    def visit(self, node):
        node = self.transformation(node)
        return super().visit(node)


# Define a pool of simple transformations
def transform_replace_literals(node):
    """Replace numeric literals with equivalent expressions."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        replacement = ast.BinOp(
            left=ast.Constant(value=random.randint(1, 10)),
            op=ast.Add(),
            right=ast.Constant(value=node.value - random.randint(1, 10))
        )
        return replacement
    return node


def transform_flip_logic(node):
    """Flip logic operations like 'and' <-> 'or' while keeping equivalence."""
    if isinstance(node, ast.BoolOp):
        if isinstance(node.op, ast.And):
            return ast.BoolOp(op=ast.Or(), values=node.values)
        elif isinstance(node.op, ast.Or):
            return ast.BoolOp(op=ast.And(), values=node.values)
    return node


def transform_variable_names(node):
    """Randomly rename variables."""
    if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
        node.id = f"var_{random.randint(1000, 9999)}"
    return node


# Fitness function to ensure equivalence
def fitness_function(original_code, mutated_code, test_cases):
    try:
        exec(original_code, globals(), locals())
        original_func = locals().get("test_func")

        exec(mutated_code, globals(), locals())
        mutated_func = locals().get("test_func")

        for case in test_cases:
            if original_func(*case) != mutated_func(*case):
                return 0  # Penalize non-equivalence
        return 1  # Perfect fitness if all test cases pass
    except Exception:
        return 0  # Penalize broken code


# Obfuscation engine
def obfuscate_code(original_code, test_cases, generations=10, population_size=10):
    parsed_tree = ast.parse(original_code)
    transformations = [transform_replace_literals, transform_flip_logic, transform_variable_names]

    population = [parsed_tree]

    for generation in range(generations):
        new_population = []
        for _ in range(population_size):
            individual = random.choice(population)
            transformer = CodeTransformer(random.choice(transformations))
            new_tree = ast.fix_missing_locations(transformer.visit(individual))
            new_population.append(new_tree)

        # Evaluate fitness
        population = sorted(
            new_population,
            key=lambda ind: fitness_function(original_code, astor.to_source(ind), test_cases),
            reverse=True
        )[:population_size]  # Keep the best individuals

    # Return the best obfuscated code
    return astor.to_source(population[0])


# Example usage
if __name__ == "__main__":
    original_code = """
def test_func(x, y):
    return x + y
"""
    test_cases = [(1, 2), (3, 4), (5, 6)]
    obfuscated_code = obfuscate_code(original_code, test_cases)
    print("Original Code:")
    print(original_code)
    print("\nObfuscated Code:")
    print(obfuscated_code)
