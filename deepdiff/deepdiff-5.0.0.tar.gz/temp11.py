from deepdiff import DeepDiff

t1 = [1.0, 2.0, 3.0, 4.0, 5.0]
t2 = [5.0, 3.01, 1.2, 2.01, 4.0]

# With a low cutoff_intersection_for_pairs, the 2 iterables above will be considered too
# far off from each other to get the individual pairs of items.
# So numbers that are not only related to each other via their positions in the lists
# and not their values are paired together in the results.
DeepDiff(t1, t2, ignore_order=True, cutoff_intersection_for_pairs=0.1)

# With the cutoff_intersection_for_pairs of 0.7 (which is the default value),
# the 2 iterables will be considered close enough to get pairs of items between the 2.
# So 2.0 and 2.01 are paired together for example.
DeepDiff(t1, t2, ignore_order=True, cutoff_intersection_for_pairs=0.7)
