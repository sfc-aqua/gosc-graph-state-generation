from typing import List, Tuple

from ..utility.constant import Basis


def ascii_instruction_visualization(
    node_to_patch_mapping: List[int],
    patch_initialized_state: List[Basis],
    measurement_steps: List[List[Tuple[int, Tuple[int, int]]]],
):
    n = len(node_to_patch_mapping)
    if n > 1000:
        raise NotImplementedError("cannot handle nodes more than 1000 at the moment.")
    inverse_map = [0] * n
    for i in node_to_patch_mapping:
        inverse_map[node_to_patch_mapping[i]] = i

    inverse_map_str = [f"{i:03}" for i in inverse_map]

    # printing
    label_line = "| " + " | ".join(inverse_map_str) + " |"
    patch_state_line = "| " + " | ".join([f" {i.name} " for i in patch_initialized_state]) + " |"
    label_border = "|_" + "_|_".join(["___" for _ in inverse_map_str]) + "_|"

    print(label_line)
    print(patch_state_line)
    print(label_border)
    for step in measurement_steps:
        curend = 0
        line = ""
        for (_, (left, right)) in step:
            if left > curend:
                line = line + ("      ") * (left - curend)
            line += " |----"
            line += "------" * (right - left - 1)
            line += "-----|"
            curend = right + 1
        print(line)
