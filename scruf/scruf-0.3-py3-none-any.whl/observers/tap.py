import sys

from scruf import observe, run


class TapObserver(observe.Observer):
    def notify_before_testing_file(self, filename):
        print(self._tap_comment_line("Testing: {}".format(filename)))

    def notify_before_tests_run(self, tests):
        print("1..{}".format(len(tests)))

    def notify_test_error(self, test, test_number, error):
        print(self._tap_failure(self._build_output_line(test, test_number)))
        print(self._tap_error_line(error), file=sys.stderr)

    def notify_test_success(self, test, test_number):
        print(self._tap_success(self._build_output_line(test, test_number)))

    def notify_test_failure(self, test, test_number, failed_comparisons):
        print(self._tap_failure(self._build_output_line(test, test_number)))
        for test in failed_comparisons:
            failure_lines = [
                self._tap_comment_line("\t" + line)
                for line in run.get_printable_failures(test)
            ]
            print("\n".join(failure_lines), file=sys.stderr)

    ######################
    # TAP specific methods
    ######################
    @staticmethod
    def _tap_success(content):
        return "ok " + content

    @staticmethod
    def _tap_failure(content):
        return "not ok " + content

    @staticmethod
    def _tap_comment_line(content):
        return "# " + content

    @classmethod
    def _tap_error_line(cls, error):
        error_lines = []
        for line in str(error).splitlines():
            error_lines.append(cls._tap_comment_line("\t" + line))
        return "\n".join(error_lines)

    @staticmethod
    def _build_output_line(test, test_number):
        output_line = str(test_number)
        if test.description:
            output_line += " - {}".format(test.description.rstrip())
        return output_line
