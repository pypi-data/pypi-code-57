import unittest
from parameterized import parameterized
import os
import sys
import json

try:
    import mfa_problem.io_excel as io_excel
    import mfa_problem.mfa_problem_main as mfa_problem_main
except ImportError:
    sys.path.append(os.getcwd())
    from mfa_problem import io_excel as io_excel
    from mfa_problem import mfa_problem_main as mfa_problem_main

try:
    from .test_mfa_problem_expected_results import expected_results
except ImportError:
    sys.path.append('.')
    from test_mfa_problem_expected_results import expected_results


class MFAProblemsTests(unittest.TestCase):
    generate_results = False

    @classmethod
    def set_generate_results(cls):
        cls.generate_results = True
        cls.new_results = expected_results

    @parameterized.expand([(
        'pommes_poires no uncert',
        'pommes_poires.xlsx',
        expected_results['pommes_poires no uncert'][0],
        expected_results['pommes_poires no uncert'][1]
        ), (
        'simplified_example_fr no uncert',
        'simplified_example_fr.xlsx',
        expected_results['simplified_example_fr no uncert'][0],
        expected_results['simplified_example_fr no uncert'][1]
        )
    ])
    def test_reconciliation_no_uncert(self, name, file_name, expected_supply, expected_use):
        current_dir = os.getcwd()
        input_dir = os.path.join(current_dir, 'data/input')
        if not os.path.exists(input_dir):
            # in the package
            input_dir = os.path.join(current_dir, 'data')

        excel_file = os.path.join(input_dir, file_name)
        mfa_problem_input = io_excel.load_mfa_problem_from_excel(excel_file)

        mfa_problem_output = mfa_problem_main.optimisation(
            name,
            mfa_problem_input,
            uncertainty_analysis=False, nb_realisations=None,
            downscale=False,
            upper_level_index2name=None, upper_level_solved_vector=None,
            upper_level_classification=None, montecarlo_upper_level=None,
            record_simulations=False
        )
        if not self.generate_results:
            self.assertEqual(
                mfa_problem_output['result ter moy']['supply'], expected_supply
            )
            self.assertEqual(
                mfa_problem_output['result ter moy']['use'], expected_use
            )
        else:
            self.new_results[name][0] = mfa_problem_output['result ter moy']['supply']
            self.new_results[name][1] = mfa_problem_output['result ter moy']['use']

    @parameterized.expand([(
        'pommes_poires uncert',
        'pommes_poires.xlsx',
        [
            [45.06, 45.49, 45.14, 43.93, 44.22, 44.93, 46.52, 44.74, 45.29, 46.38],
            [30.06, 30.49, 30.14, 28.93, 29.22, 29.93, 31.52, 29.74, 30.29, 31.38],
            [15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0],
            [19.31, 20.5, 20.01, 20.52, 20.6, 19.86, 19.37, 19.84, 19.41, 19.36],
            [30.06, 30.49, 30.14, 28.93, 29.22, 29.93, 31.52, 29.74, 30.29, 31.38],
            [30.06, 30.49, 30.14, 28.93, 29.22, 29.93, 31.52, 29.74, 30.29, 31.38],
            [9.31, 10.5, 10.01, 10.52, 10.6, 9.86, 9.37, 9.84, 9.41, 9.36],
            [15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0],
            [15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0],
            [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
            [44.68, 45.49, 45.07, 44.73, 44.91, 44.9, 45.44, 44.79, 44.85, 45.37],
            [19.68, 20.49, 20.07, 19.73, 19.91, 19.9, 20.44, 19.79, 19.85, 20.37],
            [19.68, 20.49, 20.07, 19.73, 19.91, 19.9, 20.44, 19.79, 19.85, 20.37],
            [19.68, 20.49, 20.07, 19.73, 19.91, 19.9, 20.44, 19.79, 19.85, 20.37],
            [25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0]
        ]
        ), (
        'simplified_example_fr uncert',
        'simplified_example_fr.xlsx',
        [
            [98.46, 97.52, 98.98, 98.11, 98.9, 97.8, 97.33, 97.62, 98.85, 98.14],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [16.14, 17.21, 18.27, 17.56, 16.92, 18.36, 18.49, 19.07, 17.99, 19.0],
            [71.3, 69.76, 73.49, 70.98, 68.7, 70.69, 67.86, 70.28, 74.03, 69.33],
            [3.29, 3.47, 2.78, 3.29, 2.98, 2.93, 3.17, 3.37, 2.97, 3.12],
            [70.72, 71.72, 72.65, 69.95, 70.89, 70.23, 70.67, 73.75, 70.64, 72.48],
            [12.44, 11.99, 11.59, 13.38, 11.85, 13.23, 12.17, 11.52, 12.75, 12.05],
            [5.32, 5.47, 5.19, 5.2, 5.84, 5.51, 5.29, 5.08, 5.45, 4.93],
            [16.03, 16.25, 16.86, 16.7, 16.91, 16.39, 16.69, 16.11, 16.98, 17.17],
            [9.66, 9.58, 9.38, 9.43, 9.36, 9.54, 9.44, 9.63, 9.34, 9.28],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0],
            [36.46, 38.34, 36.79, 37.73, 40.05, 38.35, 40.73, 39.57, 35.59, 41.03],
            [6.84, 6.63, 6.97, 6.96, 7.07, 7.12, 7.23, 6.84, 7.21, 6.78],
            [34.26, 33.37, 35.86, 32.23, 30.84, 31.88, 29.94, 34.18, 35.05, 31.45],
            [28.48, 28.24, 28.45, 30.08, 28.77, 29.62, 28.86, 27.64, 29.74, 29.23],
            [11.84, 11.63, 11.97, 11.96, 12.07, 12.12, 12.23, 11.84, 12.21, 11.78],
            [78.99, 79.45, 79.62, 79.03, 79.05, 79.31, 78.75, 80.24, 79.23, 79.64],
            [9.49, 9.73, 9.81, 9.51, 9.53, 9.66, 9.37, 10.12, 9.61, 9.82],
            [15.34, 15.42, 15.62, 15.57, 15.64, 15.46, 15.56, 15.37, 15.66, 15.72],
            [10.34, 10.42, 10.62, 10.57, 10.64, 10.46, 10.56, 10.37, 10.66, 10.72]
        ]
        )
    ])
    def test_reconciliation_uncert(self, name, file_name, expected_simulations):
        current_dir = os.getcwd()
        input_dir = os.path.join(current_dir, 'data/input')
        if not os.path.exists(input_dir):
            # in the package
            input_dir = os.path.join(current_dir, 'data')

        excel_file = os.path.join(input_dir, file_name)
        mfa_problem_input = io_excel.load_mfa_problem_from_excel(excel_file)

        mfa_problem_output = mfa_problem_main.optimisation(
            name,
            mfa_problem_input,
            uncertainty_analysis=True, nb_realisations=10,
            downscale=False,
            upper_level_index2name=None, upper_level_solved_vector=None,
            upper_level_classification=None, montecarlo_upper_level=None,
            record_simulations=True
        )
        self.assertEqual(
            mfa_problem_output['Simulations'].tolist(), expected_simulations
        )

    @classmethod
    def tearDownClass(cls):
        if cls.generate_results:
            content = json.dumps(cls.new_results, indent=2)
            cwd = os.getcwd()
            file_name = os.path.join(cwd, 'tests', 'integration', 'expected_results_new.py')
            with open(file_name, "w") as outfile:
                outfile.write(content)


if __name__ == '__main__':
    b = len(sys.argv) > 1
    if len(sys.argv) > 1:
        MFAProblemsTests.set_generate_results()
    unittest.main(argv=['first-arg-is-ignored'])
