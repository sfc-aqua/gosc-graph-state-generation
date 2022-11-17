# gosc-graph-state-generation
Building compiler for generate graph state based on "A Game of Surface Codes: Large-Scale Quantum Computing with Lattice Surgery".

# Below I have provided a template to Work off of in this Readme

# orquestra-quantum

## What is it?

`orquestra-quantum` is a library with core functionalities for quantum computing developed by [Zapata](https://www.zapatacomputing.com) for our [Orquestra](https://www.zapatacomputing.com/orquestra/) platform.

`orquestra-quantum` provides:

- core functionalities required to run experiments, such as the `Circuit` class.
- interfaces for implementing other Orquestra modules, such as quantum backends.
- basic data structures and functions for quantum computing.

## Installation

Even though it's intended to be used with Orquestra, `orquestra-quantum` can be also used as a standalone Python module.
To install it, you just need to run `pip install .` from the main directory.


## Usage

Here's an example of how to use methods from `orquestra-quantum` to run a circuit locally. The program runs a circuit with a single Hadamard gate 100 times and returns the results:

```python
from orquestra.quantum.circuits import H, Circuit
from orquestra.quantum.symbolic_simulator import SymbolicSimulator

def orquestra_quantum_example_function()
    circ = Circuit([H(0)])
    sim = SymbolicSimulator()
    nsamples = 100
    measurements = sim.run_circuit_and_measure(circ, nsamples)
    return measurements.get_counts()
```


## Development and Contribution

To install the development version, run `pip install -e '.[dev]'` from the main directory. (if using MacOS, you will need single quotes around the []. If using windows, or Linux, you might not need the quotes).

We use [Google-style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstring format. If you'd like to specify types please use [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints instead adding them to docstrings.

There are codestyle-related [Github Actions](.github/workflows/style.yml) running for PRs. 

- If you'd like to report a bug/issue please create a new issue in this repository.
- If you'd like to contribute, please create a pull request to `main`.

### Running tests

Unit tests for this project can be run using `make coverage` command from the main directory.
Alternatively you can also run `pytest .`.

### Style

We are using automatic tools for style and type checking. In order to make sure the code is compliant with them please run: `make style` from the main directory (this requires `dev` dependencies).

## Explain visualization techniques

### ascii visualization

### pictures