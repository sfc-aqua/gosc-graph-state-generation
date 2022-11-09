from graph_state_generation.optimizers.stabilizer_measurement_scheduler import (
    greedy_stabilizer_measurement_scheduler,
)


def test_greedy_scheduler_0():
    stabilizers_set_0 = [(0, (0, 5)), (1, (1, 2)), (2, (1, 10))]
    assert len(greedy_stabilizer_measurement_scheduler(stabilizers_set_0)) == 3


def test_greedy_scheduler_1():
    stabilizers_set_1 = [(0, (0, 5)), (1, (1, 2)), (2, (6, 10))]
    assert len(greedy_stabilizer_measurement_scheduler(stabilizers_set_1)) == 2
