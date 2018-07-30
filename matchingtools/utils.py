from functools import reduce
from operator import mul


class Permutation(object):
    def __init__(self, indices_transformation):
        self.indices_transformation = indices_transformation

    def __eq__(self, other):
        return self.indices_transformation == other.indices_transformation

    @staticmethod
    def compare(original, transformed):
        if len(original) != len(transformed):
            raise ValueError(
                "Unable to build permutation: samples have different sizes"
            )

        try:
            new_positions = [transformed.index(item) for item in original]
        except ValueError as e:
            raise ValueError(
                "Unable to build permutation: elements do not match"
            ) from e

        return Permutation(new_positions)

    @property
    def parity(self):
        return reduce(
            mul,
            [cycle.parity for cycle in self.get_cycles()],
            1
        )

    def get_cycles(self):
        cycles = [[]]
        current_cycle = cycles[-1]
        current_index = 0
        used = [False] * len(self.indices_transformation)

        while not all(used):
            next_ = self.indices_transformation[current_index]

            if next_ in current_cycle:  # cycled
                try:
                    current_index = used.index(False)
                except ValueError:  # no more unused
                    break

                current_cycle = []
                cycles.append(current_cycle)
            else:
                used[next_] = True
                current_cycle.append(next_)
                current_index = next_

        return [Cycle(cycle) for cycle in cycles if len(cycle) > 1]


class Cycle(object):
    def __init__(self, cycle):
        if len(cycle) == 1:
            raise ValueError("Unable to build cycle from a singleton list")

        self.cycle = cycle

    def __eq__(self, other):
        if len(self.cycle) != len(other.cycle):
            return False

        try:
            offset = other.cycle.index(self.cycle[0])
        except ValueError:
            return False

        length = len(self.cycle)
        for i, x in enumerate(self.cycle):
            if other.cycle[(offset + i) % length] != x:
                return False

        return True

    def __str__(self):
        return str(self.cycle)

    __repr__ = __str__

    @property
    def parity(self):
        if not self.cycle:  # identity
            return 1

        def odd(x):
            return (x % 2) == 1

        return 1 if odd(len(self.cycle)) else -1