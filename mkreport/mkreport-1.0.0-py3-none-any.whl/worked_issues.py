import os
from . import issue, print_error
from redminelib import Redmine

class WorkedIssues:
    REDMINE_URL = os.environ['REDMINE_URL']
    REDMINE_API_KEY = os.environ['REDMINE_API_KEY']

    def __init__(self):
        self.__redmine = Redmine(self.REDMINE_URL, key=self.REDMINE_API_KEY)
        self.__current_user = self.__redmine.user.get('current')
        self.__doing_issues = self.__redmine.issue.filter(assigned_to_id=self.__current_user.id)
        self.__redmine_statuses = self.__build_redmine_statuses()
        self.__issues = self.__input_worked_issues()
        self.__post_time_entry()
        self.__post_issue_status()
        self.__issue_text = self.__build_worked_issue_text()

    @property
    def issue_text(self):
        return self.__issue_text

    def __build_redmine_statuses(self):
        statuses = {}
        for status in self.__redmine.issue_status.all():
            statuses[status.name] = status.id
        return statuses

    def __build_worked_issue_text(self):
        worked_issue_text = "【作業内容】\n"
        for issue in self.__issues:
            if issue.id is not None:
                worked_issue_text += "#" + issue.id
            worked_issue_text += issue.name + "\n"
            worked_issue_text += "  " + issue.comment + "\n"
        return worked_issue_text

    def __confirm_redmine_subject(self, redmine_subject):
        dic = {'y': True, 'yes': True, 'n': False, 'no': False}
        while True:
            try:
                inp = input(redmine_subject + "でよろしいですか?(y/n)\n")
                confirm = dic[inp.lower()]
                break
            except:
                pass
            print_error.print_error('yかnを入力してください。')
        return confirm

    def __get_redmine_issue(self, inp):
        try:
            issue = self.__redmine.issue.get(str(inp))
            return issue
        except:
            print_error.print_error('チケットが存在しません')
            return False

    def __input_worked_issues(self):
        issues = []
        while True:
            print("担当者が自分のチケット一覧")
            for doing_issue in self.__doing_issues:
                print("  {}:{}".format(str(doing_issue.id).rjust(8), doing_issue.subject))
            prefix = '作業した' if len(issues) == 0 else '他にも作業したことがあれば'
            inp = input(prefix + 'チケットの番号か内容を入力してください(qを入力すると終了)\n')
            if inp == 'q':
                break
            elif inp.isdigit():
                redmine_issue = self.__get_redmine_issue(inp)
                if redmine_issue and self.__confirm_redmine_subject(redmine_issue.subject):
                    issues.append(issue.Issue(id=inp, name=redmine_issue.subject,
                                              status=redmine_issue.status, statuses=self.__redmine_statuses))
            else:
                issues.append(issue.Issue(name=inp))
        return issues

    def __post_issue_status(self):
        for issue in self.__issues:
            if issue.id is not None and issue.status_changed():
                try:
                    redmine_issue = self.__redmine.issue.get(issue.id)
                    redmine_issue.status_id = issue.new_status_id
                    redmine_issue.save()
                except:
                    print_error.print_error('ステータスの更新に失敗しました。')

    def __post_time_entry(self):
        for issue in self.__issues:
            if issue.id is not None:
                try:
                    self.__redmine.time_entry.create(
                        issue_id=issue.id,
                        hours=issue.time
                    )
                except:
                    print_error.print_error('作業時間の入力にエラーが発生しました')
