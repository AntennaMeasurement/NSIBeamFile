#!/bin/bash

package_name="NSIBeamFile"
package_description="NSI2000 Antenna Measurement Software Far-Field Beam File Parser"
package_author="Hüseyin YİĞİT"
package_author_email="yigit.hsyn@gmail.com"
package_license="MIT"
package_repository_owner="AntennaMeasurement"
package_repository_name="NSIBeamFile"
package_repository_url="https://github.com/${package_repository_owner}/${package_repository_name}.git"

set -e
set -u
set -o pipefail

echo "Bootstrapping the project..."

# Creating project layout directories
mkdir -p src/${package_name}
mkdir -p tests

# Creating initial files
touch src/${package_name}/__init__.py
touch src/${package_name}/core.py
touch src/${package_name}/cli.py
touch tests/test_core.py

# Add hello function to core.py
cat <<EOL >> src/${package_name}/core.py
def hello() -> str:
    return "Hello from ${package_name}!"
EOL

# Add test for hello function in test_core.py
cat <<EOL >> tests/test_core.py

def test_hello():
  from ${package_name}.core import hello
  expected = "Hello from ${package_name}!"
  captured = hello()
  assert captured == expected
EOL

# Configure pyproject.toml for the project

echo "Configuring pyproject.toml..."

cat <<EOL > pyproject.toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "${package_name}"
version = "0.1.0"
description = "${package_description}"
authors = [{name = "${package_author}", email = "${package_author_email}"}]
license = { text = "${package_license}" }
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = []

[project.urls]
Repository = "${package_repository_url}"

[project.scripts]
${package_name}Cli = "${package_name}.cli:main"

[project.optional-dependencies]
test = ["pytest"]

[tool.setuptools.packages.find]
where = ["src"]
EOL

# Virtual environment setup
echo "Setting up virtual environment..."
python -m venv .venv
if [[ "$OSTYPE" == "msys" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi
pip install -e ".[test]"

# Run first test
echo "Running first test..."
pytest tests/test_core.py

# Initialize git repository
echo "Initializing git repository..."
# Fetch .gitignore if not exists 
if [ ! -f .gitignore ]; then
    curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/refs/heads/main/Python.gitignore
fi
git init
git add .
git commit -m "Initial commit"

# Create remote repository if it doesn't exist with gh CLI
if ! gh repo view "${package_repository_owner}/${package_repository_name}" > /dev/null 2>&1; then
    gh repo create "${package_repository_owner}/${package_repository_name}" --public --source=. --remote=origin
fi

git branch -M main
git remote add origin "${package_repository_url}"
git push -u origin main