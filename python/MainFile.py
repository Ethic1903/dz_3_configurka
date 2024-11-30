import toml
import re
import sys
import os

class ConfigSyntaxError(Exception):
    """Класс для обработки синтаксических ошибок."""
    pass

class ConfigConverter:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.constants = {}

    def parse_toml(self):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input file '{self.input_path}' not found.")
        try:
            with open(self.input_path, 'r', encoding='utf-8') as file:
                return toml.load(file)
        except toml.TomlDecodeError as e:
            raise ConfigSyntaxError(f"Invalid TOML syntax: {e}")

    def parse_constants(self, data):
        """Рекурсивное извлечение всех констант."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (int, float, str)):
                    self.constants[key] = value
                elif isinstance(value, dict) or isinstance(value, list):
                    self.parse_constants(value)

    def resolve_constants(self, data):
        """Замена конструкций вида `.["имя"].` на соответствующие значения."""
        if isinstance(data, dict):
            return {k: self.resolve_constants(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.resolve_constants(v) for v in data]
        elif isinstance(data, str):
            match = re.fullmatch(r"\.\[(\w+)\]\.", data)
            if match:
                const_name = match.group(1)
                if const_name in self.constants:
                    return self.constants[const_name]
                else:
                    # Добавление исключения при отсутствии константы
                    raise ConfigSyntaxError(f"Undefined constant: '{const_name}'")
            return data
        else:
            return data

    def transform_to_custom_format(self, data):
        """Конвертация данных TOML в учебный конфигурационный язык."""
        def transform_value(value):
            if isinstance(value, dict):
                return "{\n" + "\n".join(f" {k} : {transform_value(v)}" for k, v in value.items()) + "\n}"
            elif isinstance(value, (int, float)):
                return str(value)
            elif isinstance(value, str):
                return value
            else:
                raise ConfigSyntaxError(f"Unsupported value type: {type(value)}")

        result = []
        for key, value in data.items():
            if isinstance(value, dict):
                result.append(f"{key} is {transform_value(value)}")
            elif isinstance(value, (int, float)):
                result.append(f"{key} is {value}")
            elif isinstance(value, str):
                self.constants[key] = value
                result.append(f"{key} is {value}")
            else:
                raise ConfigSyntaxError(f"Unsupported top-level value type for key '{key}': {type(value)}")
        return "\n".join(result)

    def save_to_file(self, output_data):
        """Сохранение преобразованных данных в файл."""
        with open(self.output_path, 'w', encoding='utf-8') as file:
            file.write(output_data)

    def run(self):
        """Основной процесс конвертации."""
        try:
            data = self.parse_toml()
            self.parse_constants(data)
            resolved_data = self.resolve_constants(data)
            output = self.transform_to_custom_format(resolved_data)
            self.save_to_file(output)
            print("Conversion completed successfully.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_path> <output_path>")
        sys.exit(1)

    converter = ConfigConverter(sys.argv[1], sys.argv[2])
    converter.run()
