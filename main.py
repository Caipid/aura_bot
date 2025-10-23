import toml

try:
    with open("pyproject.toml", "r") as f:
        data = toml.load(f)
    print("✓ Файл валиден")
except Exception as e:
    print(f"✗ Ошибка: {e}")