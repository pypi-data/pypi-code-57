import os.path
import glob
import august


class TestSamples:
    pass


def generate(filename):
    def _func(_1):
        with open(filename) as handle:
            actual = august.convert(handle.read())
        result_filename = os.path.splitext(filename)[0] + '.txt'
        with open(result_filename) as handle:
            expected = handle.read()
        assert expected == actual
    return _func


test_dir_name = os.path.dirname(os.path.realpath(__file__))

for glob_name in glob.glob('{}/samples/*.html'.format(test_dir_name)):
    base_name = os.path.splitext(os.path.basename(glob_name))[1].lower()
    func = generate(glob_name)
    setattr(TestSamples,  'test_{}'.format(base_name), func)
