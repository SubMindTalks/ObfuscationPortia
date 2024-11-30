import subprocess
import os

BASELINE_DIR = "Baseline"
OBFUSCATED_DIR = "Baseline_obfuscated"
STATIC_RESOURCES_DIR = "static_resources"

def test_code_execution(file_name):
    original_path = os.path.join(BASELINE_DIR, file_name)
    obfuscated_path = os.path.join(OBFUSCATED_DIR, file_name)

    input_data = os.path.join(STATIC_RESOURCES_DIR, "test_input.txt")
    original_output = subprocess.check_output(["python", original_path, input_data])
    obfuscated_output = subprocess.check_output(["python", obfuscated_path, input_data])

    assert original_output == obfuscated_output, f"Outputs differ for {file_name}!"

def run_tests():
    for file_name in os.listdir(BASELINE_DIR):
        if file_name.endswith(".py"):
            test_code_execution(file_name)

if __name__ == "__main__":
    run_tests()
