from io import TextIOWrapper

Node = tuple[int, int]

Graph = dict[Node, tuple[Node, Node]]


def build_graph(input: TextIOWrapper) -> tuple[Graph, Node]:
    nodes: Graph = {}
    start: Node = (0, 0)

    for y, line in enumerate(input.readlines()):
        for x, char in enumerate(line.strip()):
            if char == ".":
                continue
            if char == "-":
                nodes[(x, y)] = ((x - 1, y), (x + 1, y))
            elif char == "|":
                nodes[(x, y)] = ((x, y - 1), (x, y + 1))
            elif char == "J":
                nodes[(x, y)] = ((x, y - 1), (x - 1, y))
            elif char == "L":
                nodes[(x, y)] = ((x, y - 1), (x + 1, y))
            elif char == "F":
                nodes[(x, y)] = ((x, y + 1), (x + 1, y))
            elif char == "7":
                nodes[(x, y)] = ((x, y + 1), (x - 1, y))
            elif char == "S":
                start = (x, y)
            else:
                raise ValueError(f"Invalid character: {char}")

    # Add the start node
    connecting_nodes = []
    for node in nodes:
        if start in nodes[node]:
            connecting_nodes.append(node)
    nodes[start] = connecting_nodes

    return nodes, start


def find_circular_path(graph: Graph, start: Node) -> list[Node]:
    path = [start]
    previous_node = start
    current_node = graph[start][0]
    while current_node != start:
        if current_node not in graph:
            raise ValueError(f"Invalid node: {current_node}")

        next_node = graph[current_node][0] if graph[current_node][0] != previous_node else graph[current_node][1]
        path.append(current_node)
        previous_node = current_node
        current_node = next_node

    return path


def part_1(input: TextIOWrapper):
    print("Part 1")
    graph, start = build_graph(input)
    path = find_circular_path(graph, start)
    print(len(path) / 2)


def is_inside_path(path: list[Node], position: Node) -> bool:
    if position in path:
        return False

    # Count the direction changes of the path that the ray crosses
    direction = 0
    for i, path_node in enumerate(path):
        # If path_node is on the same x axis, on the right of the position
        # These are all the path nodes the ray to the right crosses when going from the position to the right
        if path_node[1] == position[1] and path_node[0] > position[0]:
            previous_path_node = path[i - 1] if i > 0 else path[-1]
            next_path_node = path[(i + 1)] if i < len(path) - 1 else path[0]
            # Find the direction of the 3 node path
            if previous_path_node[1] > path_node[1]:
                direction += 1
            elif previous_path_node[1] < path_node[1]:
                direction -= 1
            if next_path_node[1] > path_node[1]:
                direction -= 1
            elif next_path_node[1] < path_node[1]:
                direction += 1

    # If the final direction changes is not 0, then the position is inside the path
    return direction != 0


def part_2(input: TextIOWrapper):
    print("Part 2")

    graph, start = build_graph(input)

    path = find_circular_path(graph, start)

    height = max(node[0] for node in graph.keys())
    min_height = min(node[0] for node in graph.keys())
    width = max(node[1] for node in graph.keys())
    min_width = min(node[1] for node in graph.keys())

    # For each position within the path bounds, check if it is enclosed by the path
    inside_positions = []
    for x in range(min_height, height):
        for y in range(min_width, width):
            if is_inside_path(path, (x, y)):
                inside_positions.append((x, y))
    print(len(inside_positions))


def solution(input: TextIOWrapper, part_number: int):
    if part_number == 1:
        part_1(input)
    elif part_number == 2:
        part_2(input)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
