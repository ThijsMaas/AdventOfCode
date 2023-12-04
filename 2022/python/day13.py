from itertools import zip_longest


def correct(left, right):
    if left < right:
        return True
    if right < left:
        return False
    return None


def main():
    input_file = "data/day13.txt"
    with open(input_file) as f:
        lines = f.read()

    pairs = []

    for pair in lines.split("\n\n"):
        (l1, l2) = pair.split("\n")
        left = eval(l1)
        right = eval(l2)
        print("original:", left, right)
        result = test_pair(left, right)
        print(result)
        pairs.append(result)

    print(pairs)
    print("Part1: ", sum(i + 1 for i, result in enumerate(pairs) if result))


def test_pair(left, right):
    for l, r in zip_longest(left, right):
        if type(l) == list and len(l) == 0:
            return True
        if type(r) == list and len(r) == 0:
            return False

        l = 0 if l == None else l
        r = 0 if r == None else r
        to_compare = []
        to_compare.append((l, r))
        while to_compare:
            print("queue", to_compare)
            (compare_l, compare_r) = to_compare.pop(0)
            print("compare:", compare_l, compare_r)
            if type(compare_l) == int and type(compare_r) == int:
                pair_result = correct(compare_l, compare_r)
                if pair_result == None:
                    continue
                else:
                    return pair_result
            else:
                compare_l = [compare_l] if type(compare_l) == int else compare_l
                compare_r = [compare_r] if type(compare_r) == int else compare_r
                if len(compare_l) == 0:
                    return True
                if len(compare_r) == 0:
                    return False
                for l_inner, r_inner in zip_longest(compare_l, compare_r):
                    l_inner = 0 if l_inner == None else l_inner
                    r_inner = 0 if r_inner == None else r_inner
                    to_compare.append((l_inner, r_inner))
    return False


if __name__ == "__main__":
    main()
