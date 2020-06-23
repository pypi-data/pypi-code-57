from deepdiff import DeepDiff

# t1 = [
#     {
#         'key3': [[[[[1, 2, 4, 5, 5, 5]]]]],
#         'key4': [7, 8],
#     },
#     {
#         'key5': 'val5',
#         'key6': 'val6',
#     },
# ]

# t2 = [
#     {
#         'key5': 'CHANGE',
#         'key6': 'val6',
#     },
#     {
#         'key3': [[[[[5, 5, 1, 3, 5, 4]]]]],
#         'key4': [7, 8],
#     },
# ]


t1 = [
    {
        'key3': [[[[[1, 2, 4, 5]]]]],
        'key4': [7, 8],
    },
    {
        'key5': 'val5',
        'key6': 'val6',
    },
]

t2 = [
    {
        'key5': 'CHANGE',
        'key6': 'val6',
    },
    {
        'key3': [[[[[1, 3, 5, 4]]]]],
        'key4': [7, 8],
    },
]


# t1 = [
#     [1, 2, 3, 9], [9, 8, 5, 9]
# ]

# t2 = [
#     [1, 2, 4, 10], [4, 2, 5]
# ]

prev_diff = None
for i in range(0, 64):
    # diff = DeepDiff(t1, t2, ignore_order=True, max_diffs=i, verbose_level=2)
    diff = DeepDiff(t1, t2, ignore_order=True, max_passes=i, verbose_level=2)
    if prev_diff != diff:
        print(f"------------- max item={i} ----------")
        print(diff)
        prev_diff = diff

print(diff.get_stats())

# diff = DeepDiff(t1, t2, ignore_order=True, report_repetition=False, max_passes=600)
# print(diff)
# dist = diff.get_deep_distance()
# print(f'distance: {dist}')


# t1 = [[[1, 2, 4, 5, 5, 5]]]
# t2 = [[[5, 5, 1, 3, 5, 4]]]
# diff = DeepDiff(t1, t2, ignore_order=True)
# print(diff)
# dist = diff.get_deep_distance()
# print(f'distance: {dist}')
