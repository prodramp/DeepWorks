from src.ramputils import calc

assert calc('addition', 1, 2, 3, 5)[1] == 11
assert calc('subtraction', 30, 5)[1] == 25
assert calc('multiplication', 1, 2, 3, 5)[1] == 30
assert calc('division', 2, 5)[1] == 0.4
