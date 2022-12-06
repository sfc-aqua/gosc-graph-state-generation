# Substrate Scheduler

## About The Project

`Substrate Scheduler` is a tool with core functionalities to efficiently create the input graph state fault-tolerantly using the rules given by Litinski’s "A Game of Surface Codes: Large-Scale Quantum Computing with Lattice Surgery" (GOSC) paper with the goal of minimizing the space-time volume cost.  The space-time volume cost is defined to be the space multiplied by the time where space is defined by the area of patches in units of square tiles and time in units of time step as defined in the GoSC paper or one round of syndrome measurement. 

Substrate Scheduler is a product of the [AQUA](https://aqua.sfc.wide.ad.jp/), [QTS](https://quantumts.org) and [Zapata](https://www.zapatacomputing.com) for the [Bench-Q](https://quantumts.org/bench-q/) project.

<!---
- core functionalities required to run experiments, such as the `Circuit` class.
- interfaces for implementing other Orquestra modules, such as quantum backends.
- basic data structures and functions for quantum computing.
--->

## Features

Substrate Scheduler create graph states using stabilizer formalism. In the current version, it provides 3 reduces the time steps required to create a graph state via stabilizer formalism (Note that the time step here is the total number of steps required to create the graph state considering the parallel measurement of the stabilizers) :

- pre_mapping_optimizer

    From the definition of graph state, we know that we can reduce the number of stabilizer generator to be measured by initializing the qubits in a way that they are already stabilized by some stabilizer generators. For example, initialize node a in X-basis (|+> state) while initializing neighbor nodes of a in Z basis (|0> state).  
    By converting the problem of finding the optimal reduction to maximum independent set problem, `pre_mapping_optimizer` reduce the maximum number of stabilizer generators.

- node_to_patch_mapper
    tbd

- stabilizer measurement scheduler

    Suppose we have already decided where each node in the graph is mapped to which patch, in order to measure a stabilizer generator in this configuration, we need an ancilla patch that covers all the nodes defined in the stabilizer generator. This means that any stabilizer generator which includes a node between the left-most and the right-most nodes of the stabilizer we are trying to measure cannot be measured at the same time. 

    By knowing the start and end positions of each stabilizer generator, `stabilizer_measurement_scheduler` will optimally schedule the stabilizer generators to be measured and reduce the time cost by parallelly measuring as many stabilizers as possible.


## Installation

<!---Even though it's intended to be used with Orquestra, `orquestra-quantum` can be also used as a standalone Python module.
To install it, you just need to run `pip install .` from the main directory.--->

To install `Substrate Scheduler`, you just need to run `git clone https://github.com/sfc-aqua/gosc-graph-state-generation.git` 
`Substrate Scheduler`is written is Python, except for a Python3 compiler, you will also need the networkx, matplotlib and numpy packages.

## Usage
<!---
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
--->
For an example of how to use methods from `Substrate Scheduler`, please run `usage_example.py` with the following command. 
```
python usage_example.py
```
The program optimized some graph examples with Substrate Scheduler and returns the following results:

```
pre-mapping optimization took - 0.00037109400000001624s
node to patch mapping took    - 3.106400000008058e-05s
measurement scheduler took    - 2.7704999999933477e-05s
reduce from 10 to 5
| 006 | 005 | 003 | 000 | 002 | 008 | 001 | 009 | 004 | 007 |
|  X  |  Z  |  Z  |  X  |  X  |  X  |  Z  |  Z  |  X  |  Z  |
|_____|_____|_____|_____|_____|_____|_____|_____|_____|_____|
                   |---------------------|
                   |---------------------------|
             |---------------------------------------|
 |---------------------------------------------------|
 |---------------------------------------------------------|
```
It contains:
- Time taken for each optimization process (here is the run time);
- Time step reduced by the optimization;
- An ASCII visualization of the layout (results of the mapping), as well as the starting and ending positions of the stabilizer generator for each step. 

## Development and Contribution

<!---To install the development version, run `pip install -e '.[dev]'` from the main directory. (if using MacOS, you will need single quotes around the []. If using windows, or Linux, you might not need the quotes).--->

We use [Google-style](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) docstring format. If you'd like to specify types please use [PEP 484](https://www.python.org/dev/peps/pep-0484/) type hints instead adding them to docstrings.

There are codestyle-related [Github Actions](.github/workflows/style.yml) running for PRs. 

- If you'd like to report a bug/issue please create a new issue in this repository.
- If you'd like to contribute, please create a pull request to `main`.

### Running tests

Unit tests for this project can be run using `make coverage` command from the main directory.
Alternatively you can also run `pytest .`.

### Style

We are using automatic tools for style and type checking. In order to make sure the code is compliant with them please run: `make style` from the main directory (this requires `dev` dependencies).

<!---## Explain visualization techniques

### ascii visualization

### pictures
--->

## In-progress work:

- [ ] The performance of node_to_patch_mapper needs further testing and improvement.
- [ ] Tests are still being polished.

See the [open issues](https://github.com/sfc-aqua/gosc-graph-state-generation/issues) for a full list of proposed features (and known issues).

## License
Distributed under the MIT License. See `LICENSE` for more information.
