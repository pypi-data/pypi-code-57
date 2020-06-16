from pandashape.enums import Columns
from pandashape.internal import ColumnResolver, listify
from pandashape.describers import Describer


class DescriberExecutor:
    def __init__(self):
        pass

    def describe(self, df, describers, columns):
        messageLines = []
        describers = listify(describers)

        assert len(describers) > 0, ".describe() requires one or more Describers"

        messageLines.append("")
        messageLines.append("#########################################")
        messageLines.append("###         PANDASHAPE REPORT         ###")
        messageLines.append("#########################################")

        # iterate all describers and append their messages
        for describer in describers:
            assert isinstance(describer, (Describer, type)
                              ), "describers passed to .describe() must be either an instance of a class that inherits Describer OR a type that inherits Describer."

            # if the argument is a type rather than an instance, construct it
            if not isinstance(describer, Describer):
                describer = describer()

            # run describer
            describer_messages = listify(describer.describe(df))

            # print results
            messageLines.append("")
            messageLines.append(f"### {describer.get_section_header()} ###")
            messageLines.append("-----------------------------------------")
            messageLines.extend(describer_messages)

        # print all messages
        for line in messageLines:
            print(line)
        print()
