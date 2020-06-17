import os, sys
from aos.util import aos_input
from aos.constant import AOS_INVESTIGATION_FILE

def check_and_report():
    from aos.constant import AOS_INVESTIGATION_FILE
    from aos.usertrace.do_report import init_op, do_report

    init_op()

    if not os.path.isfile(AOS_INVESTIGATION_FILE):
        # ask for user's willing of participating in investigation
        try:
            from aos.util import aos_input

            err, choice = aos_input(
            "***Attention***:\n"
            "==============================================================\n"
            "  In order to improve the user experience of this tool,\n"
            "  we want to collect some of your personal information\n"
            "  including but not limited to the following items:\n\n"
            "    (0) The Operating System and version on your computer..\n"
            "    (1) the MAC and public IP address of your computer.\n"
            "    (2) Your city location information.\n"
            "    (3) The command line terminal used.\n"
            "    (4) The most frequently used aos-cube functionalities.\n\n"
            "  All collected information will be limited to be used in the\n"
            "  user-experience improve plan, and will be carefully and\n"
            "  restrictly secured.\n"
            "==============================================================\n"
            "Do you want to participate in the activity?\n"
            "Please type 'Y[es]' or 'N[o]': ")
            if err == 0:
                choice = choice.strip()
                towrite = 'participate: '
                if choice == "Yes" or choice == "Y":
                    towrite += 'Yes'
                    sys.stdout.write("Thanks for your willing to participate "
                                     "in the improve plan!\n")
                else:
                    towrite += 'No'

                dir = os.path.dirname(AOS_INVESTIGATION_FILE)
                if not os.path.isdir(dir):
                    os.makedirs(dir)

                with open(AOS_INVESTIGATION_FILE, 'w') as f:
                    f.write(towrite)

                if choice == "Yes" or choice == "Y":
                    do_report()

            sys.stdout.write("\n")
        except Exception as e:
            pass

check_and_report()
