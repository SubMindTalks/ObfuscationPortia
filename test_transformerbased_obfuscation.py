# test_transformerbased_obfuscation.py
import unittest
from transformerbased_obfuscation import obfuscate_code


class TestObfuscation(unittest.TestCase):

    def test_obfuscation(self):
        input_code = "x = 10\nprint(x)"
        expected_output = "var_1 = 10\nprint(var_1)"

        # Use temporary files for testing
        with open("temp_input.py", "w") as f:
            f.write(input_code)

        obfuscate_code("temp_input.py", "temp_output.py")

        with open("temp_output.py", "r") as f:
            obfuscated_code = f.read()

        self.assertEqual(obfuscated_code, expected_output)


if __name__ == '__main__':
    unittest.main()
