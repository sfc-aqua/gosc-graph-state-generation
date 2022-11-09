from collections import deque
from typing import List, Tuple


def greedy_stabilizer_measurement_scheduler(
    stabilizer_to_measure: List[Tuple[int, Tuple[int, int]]]
) -> List[List[Tuple[int, Tuple[int, int]]]]:
    """Optimal stabilizer measurement scheduler given that labelling is fixed. Proof to be written."""

    # stabilizer_to_measure is [(S_i, (min_i, max_i))]
    stabilizer_to_measure = stabilizer_to_measure
    stabilizer_to_measure.sort(key=lambda x: x[1][1])
    time_step = deque()  # stores list of (S_i, (min_i, max_i))
    time_step.append([stabilizer_to_measure[0]])
    for st in stabilizer_to_measure[1:]:
        if st[1][0] > time_step[0][-1][1][1]:
            time_step[0].append(st)
            time_step.append(time_step.popleft())
        else:
            time_step.append([st])

    return list(time_step)
