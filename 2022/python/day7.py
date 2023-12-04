import itertools

part2 = False


def accumulate(iterable, *, initial=None):
    "Return running totals"
    # accumulate([1,2,3,4,5]) --> 1 3 6 10 15
    # accumulate([1,2,3,4,5], initial=100) --> 100 101 103 106 110 115
    # accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
    it = iter(iterable)
    total = initial
    if initial is None:
        try:
            total = next(it)
        except StopIteration:
            return
    yield total
    for element in it:
        total += element
        yield total


def accu(iterable):
    ac = []
    total = iterable[0]
    ac.append(total)
    for i in iterable[1:]:
        total += i
        ac.append(total)
    return ac


with open("data/example.txt") as f:
    stack, sizes = [], []
    for line in f.readlines():
        if line.startswith("$ cd .."):
            size = stack.pop()
            sizes.append(size)
            stack[-1] += size
        elif line.startswith("$ cd "):
            stack.append(0)
        elif line[0].isdigit():
            stack[-1] += int(line.split()[0])
    print(stack)
    s = list(accumulate(stack[::-1]))
    # s = accu(stack[::-1])
    print(s)
    sizes.extend(s)
    # total = stack.
    # for i in stack[::-1]:

    print(
        sum(s for s in sizes if s <= 100_000)
        if not part2
        else min(s for s in sizes if s >= max(sizes) - 40_000_000)
    )
