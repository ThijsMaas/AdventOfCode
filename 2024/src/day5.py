from collections import deque
import re
from sys import argv
from api import get_input, submit_answer
from utils import timing


EXAMPLE_INPUT = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def topological_sort_for_nodes(edges: list[list[str]], nodes: list[str]) -> list[str]:
    # Makes a graph based only on the nodes we are interested in.
    # This slice of the total graph makes a topological sort possible, while the total graph is cyclic.
    graph = {node: [] for node in nodes}
    in_degree = {node: 0 for node in nodes}
    for node_a, node_b in edges:
        if node_a in nodes and node_b in nodes:
            graph[node_a].append(node_b)
            in_degree[node_b] += 1

    # Topological sort
    start_nodes = [node for node, id in in_degree.items() if id == 0]
    sorted_nodes = []
    queue = deque(start_nodes)
    while queue:
        current = queue.pop()
        sorted_nodes.append(current)
        for n_node in graph[current]:
            in_degree[n_node] -= 1
            if in_degree[n_node] == 0:
                queue.append(n_node)
    assert len(sorted_nodes) == len(nodes)
    return sorted_nodes


@timing
def part1(input_data: str):
    answer = 0
    s1, s2 = input_data.split("\n\n")
    edges = [line.split("|") for line in s1.splitlines()]

    for line in s2.splitlines():
        updates = line.split(",")
        sorted_updates = topological_sort_for_nodes(edges, updates)
        if updates == sorted_updates:
            answer += int(updates[len(updates) // 2])

    return answer


@timing
def part2(input_data: str):
    answer = 0
    s1, s2 = input_data.split("\n\n")
    edges = [line.split("|") for line in s1.splitlines()]

    for line in s2.splitlines():
        updates = line.split(",")
        sorted_updates = topological_sort_for_nodes(edges, updates)
        if updates != sorted_updates:
            answer += int(sorted_updates[len(sorted_updates) // 2])

    return answer


if __name__ == "__main__":
    """Main script to run the solutions, use flag 'e' for the example input and 's' to submit"""
    year, day = list(map(int, re.search(r"(\d{4})/src/day(\d+).py", __file__).groups()))

    # Get input data
    if len(argv) == 2 and argv[1] == "e":
        input_data = EXAMPLE_INPUT
    else:
        input_data = get_input(year, day)

    # Get answers and submit
    answer1 = part1(input_data)
    print(f"Answer part 1: {answer1}")
    if len(argv) == 2 and argv[1] == "s" and answer1 is not None:
        assert submit_answer(year, day, 1, answer1)

    answer2 = part2(input_data)
    print(f"Answer part 2: {answer2}")
    if len(argv) == 2 and argv[1] == "s" and answer2 is not None:
        assert submit_answer(year, day, 2, answer2)
