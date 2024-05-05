# Python Compatibility Matrix

`pycm` is a command-line tool for checking which versions of Python are supported by a given package.

## Installation

### Requirements

- [Python](https://www.python.org/) 3.8+

### Procedure

1. Run `python -m pip install git+https://github.com/DarkLight1337/pycm.git` to install the package from this repository.

## Usage

### Syntax

```
pycm <package> --python=<versions>
```

### Example

Show the versions of [TensorFlow](https://tensorflow.org/) that can be used with Python 3.8-3.11:

``` 
> pycm tensorflow --python=3.8,3.9,3.10,3.11
tensorflow (→) 2.2.3 2.3.4 2.4.4 2.5.3 2.6.5 2.7.4 2.8.4 2.9.3 2.10.1 2.11.1 2.12.1 2.13.1 2.14.1 2.15.1 2.16.1
Python (↓)
3.8                Y     Y     Y     Y     Y     Y     Y     Y      Y      Y      Y      Y
3.9                                  Y     Y     Y     Y     Y      Y      Y      Y      Y      Y      Y      Y
3.10                                                   Y     Y      Y      Y      Y      Y      Y      Y      Y
3.11                                                                              Y      Y      Y      Y      Y
```

(You can cross-check this table against [the official compatibility matrix](https://www.tensorflow.org/install/source#tested_build_configurations).)

## Development

### Requirements

- [Python](https://www.python.org/) 3.8+
- [Poetry](https://python-poetry.org/) 1.4+

### Setup

1. Clone this repository to your machine.
2. Run `poetry lock --no-update && poetry install --with dev` to setup the Python enviroment.

### Lint

1. [Setup](#setup) the development environment.
2. Run `poetry run deptry . && poetry run ruff check . && poetry run pyright .` to lint the code.

### Test

1. [Setup](#setup) the development environment.
2. Run `poetry run -- pytest` to test the code and output the coverage report.
