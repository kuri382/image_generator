# Generate images and output.csv(messages)
```
poetry run python generate_image.py
```

# Formating
install pysen
```
poetry add -D pysen -E lint
```
add settings in pyproject.toml
```
[tool.pysen]
version = "0.9"

[tool.pysen.lint]
enable_black = true
enable_flake8 = true
enable_isort = true
enable_mypy = false
line_length = 130
py_version = "py37"
[[tool.pysen.lint.mypy_targets]]
  paths = ["."]

```