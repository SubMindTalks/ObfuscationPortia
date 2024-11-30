import os
from transformerbased_obfuscation import CodeObfuscator

BASELINE_DIR = "Baseline"
OUTPUT_DIR = "Baseline_obfuscated"

def obfuscate_project():
    obfuscator = CodeObfuscator()

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for file_name in os.listdir(BASELINE_DIR):
        if file_name.endswith(".py"):
            input_path = os.path.join(BASELINE_DIR, file_name)
            output_path = os.path.join(OUTPUT_DIR, file_name)

            with open(input_path, "r") as f:
                code = f.read()

            obfuscated_code = obfuscator.obfuscate_code(code)

            with open(output_path, "w") as f:
                f.write(obfuscated_code)

if __name__ == "__main__":
    obfuscate_project()
