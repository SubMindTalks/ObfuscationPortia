# main.py
from transformerbased_obfuscation import obfuscate_code


def run_baseline_code(file_path):
    # Implement logic to run code in file_path
    # ... and return output. Replace this with your actual logic.
    with open(file_path, 'r') as f:
        exec(f.read())
        return "Baseline Output"  # Placeholder


def run_obfuscated_code(file_path):
    with open(file_path, 'r') as f:
        exec(f.read())
        return "Obfuscated Output"  # Placeholder


if __name__ == "__main__":
    baseline_file = "Baseline/data_structures/binary_tree/binary_search.py"  # Replace with actual path.
    obfuscated_file = "Baseline_obfuscated/data_structures/binary_tree/binary_search_tree.py"

    obfuscate_code(baseline_file, obfuscated_file)

    baseline_output = run_baseline_code(baseline_file)
    obfuscated_output = run_obfuscated_code(obfuscated_file)

    print(f"Baseline Output:\n{baseline_output}\n")
    print(f"Obfuscated Output:\n{obfuscated_output}\n")
    assert baseline_output == obfuscated_output, "Outputs don't match!"
