# Python Compatibility Matrix

`pycm` is a command-line tool for checking which versions of Python are supported by a given package.

## Installation

### Requirements

- [Python](https://www.python.org/) 3.11+

### Procedure

1. Run `python -m pip install git+https://github.com/DarkLight1337/pycm.git` to install the package from this repository.

## Usage

### Syntax

```
pycm <package> --python=<versions>
```

### Example

Show the versions of [TensorFlow](https://tensorflow.org/) that can be used with Python 3.11-3.14:

``` 
> pycm tensorflow --python=3.11,3.12,3.13,3.14
tensorflow (→) 2.12.1 2.13.1 2.14.1 2.15.1 2.16.2 2.17.1 2.18.1 2.19.1 2.20.0 2.21.0 2.22.0rc0
Python (↓)                                                                                    
3.11                Y      Y      Y      Y      Y      Y      Y      Y      Y      Y         Y
3.12                                            Y      Y      Y      Y      Y      Y         Y
3.13                                                                        Y      Y         Y
3.14                                                                                         Y
```

(You can cross-check this table against [the official compatibility matrix](https://www.tensorflow.org/install/source#tested_build_configurations).)

## Development

### Requirements

- [Python](https://www.python.org/) 3.11+
- [uv](https://docs.astral.sh/uv/) 0.13+

### Setup

1. Clone this repository to your machine.
2. Run `uv lock && uv sync` to setup the Python enviroment.

### Lint

1. [Setup](#setup) the development environment.
2. Run `uv run deptry . && uv run ruff check . && uv run pyright .` to lint the code.

### Test

1. [Setup](#setup) the development environment.
2. Run `uv run pytest` to test the code and output the coverage report.
