from . import file_operation, print_error, worked_issues, worked_time


def main():
    fo = file_operation.FileOperation()
    wt = worked_time.WorkedTime()
    wi = worked_issues.WorkedIssues()
    fo.build_report_content(wt.times_text, wi.issue_text)
    fo.make_report()


if __name__ == '__main__':
    main()
