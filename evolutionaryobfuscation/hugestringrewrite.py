import random
import ast
import astor
import subprocess
import tempfile


# Transformation rules
def transform_add_dummy_variable(node):
    """Add a dummy variable assignment."""
    if isinstance(node, ast.FunctionDef):
        new_node = ast.Assign(
            targets=[ast.Name(id=f"dummy_var_{random.randint(1000, 9999)}", ctx=ast.Store())],
            value=ast.Constant(value=42)
        )
        node.body.insert(0, new_node)
    return node


def transform_replace_constants(node):
    """Replace numeric constants with equivalent arithmetic."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        value = node.value
        return ast.BinOp(
            left=ast.Constant(value=value - 1),
            op=ast.Add(),
            right=ast.Constant(value=1)
        )
    return node


def transform_shuffle_order(node):
    """Shuffle the order of statements in a function."""
    if isinstance(node, ast.FunctionDef):
        random.shuffle(node.body)
    return node


# Custom NodeTransformer
class RewritingSystem(ast.NodeTransformer):
    def __init__(self, transformations):
        self.transformations = transformations

    def visit(self, node):
        for transform in self.transformations:
            node = transform(node)
        return super().visit(node)


# Apply rewriting system and test
def apply_and_test_rewriting_system(original_code, rewriting_system):
    try:
        # Parse the original code
        tree = ast.parse(original_code)

        # Apply the rewriting system
        transformer = RewritingSystem(rewriting_system)
        transformed_tree = transformer.visit(tree)
        ast.fix_missing_locations(transformed_tree)

        # Convert back to source code
        transformed_code = astor.to_source(transformed_tree)

        # Test the transformed code using the Python interpreter
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
            temp_file.write(transformed_code)
            temp_file_path = temp_file.name

        result = subprocess.run(["python", temp_file_path], capture_output=True, text=True)

        # Clean up temporary file
        temp_file.close()

        # Check if the code ran successfully
        if result.returncode == 0:
            return True, transformed_code
        else:
            return False, None
    except Exception as e:
        return False, None


# Generate random rewriting systems
def generate_random_rewriting_systems(num_variants):
    transformations = [transform_add_dummy_variable, transform_replace_constants, transform_shuffle_order]
    rewriting_systems = []
    for _ in range(num_variants):
        random_subset = random.sample(transformations, k=random.randint(1, len(transformations)))
        rewriting_systems.append(random_subset)
    return rewriting_systems


# Main process
def main():
    original_code = """
def test_func(x, y):
    result = x + y
    if result > 10:
        return result
    else:
        return result - 1
print(test_func(5, 6))
"""

    num_variants = 16000
    successful_rewrites = []

    print("Generating and testing rewriting systems...")
    rewriting_systems = generate_random_rewriting_systems(num_variants)

    for system in rewriting_systems:
        success, transformed_code = apply_and_test_rewriting_system(original_code, system)
        if success:
            successful_rewrites.append((system, transformed_code))

    if successful_rewrites:
        print(f"Successfully found {len(successful_rewrites)} valid rewrites.")
        for idx, (system, code) in enumerate(successful_rewrites):
            with open(f"successful_rewrite_{idx + 1}.py", "w") as file:
                file.write(code)
        print("Saved all successful rewrites to disk.")
    else:
        print("No valid rewriting systems found. Try increasing the number of variants or iterations.")


if __name__ == "__main__":
    main()
