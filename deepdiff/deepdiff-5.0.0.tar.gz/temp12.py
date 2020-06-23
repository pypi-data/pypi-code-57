from deepdiff import DeepDiff
t1 = [[1, 2, 2, 1, 3]]

t2 = [[1, 1, 2, 3]]

diff = DeepDiff(t1, t2, ignore_order=True, report_repetition=True)
print(diff)
