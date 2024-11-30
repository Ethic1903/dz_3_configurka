import unittest
from MainFile import ConfigConverter, ConfigSyntaxError


class TestConfigConverter(unittest.TestCase):

    def setUp(self):
        self.file_path = 'example.toml'
        self.output_path = 'output.txt'
        self.converter = ConfigConverter(self.file_path, self.output_path)

        self.data = self.converter.parse_toml()

    def test_successful_conversion(self):
        expected_output = "my_const is 42"
        output_str = self.converter.transform_to_custom_format(self.data)

        print(f"Output: {output_str}")
        self.assertTrue(output_str.strip().startswith(expected_output))

    def test_transform_to_custom_format(self):
        expected_output = "my_const is 42"
        output_str = self.converter.transform_to_custom_format(self.data)

        print(f"Output: {output_str}")
        self.assertTrue(output_str.startswith(expected_output))




if __name__ == '__main__':
    unittest.main()
