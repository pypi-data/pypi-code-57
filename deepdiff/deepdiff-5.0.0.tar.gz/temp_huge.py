import json
from deepdiff import DeepDiff
from deepdiff.deephash import sha256hex

actual = json.load(open('temp_huge_actual.json'))
expected = json.load(open('temp_huge_expected.json'))

diff = DeepDiff(actual, expected, ignore_order=True, log_frequency_in_sec=1, max_passes=10000, max_diffs=50000, cache_size=20000)
