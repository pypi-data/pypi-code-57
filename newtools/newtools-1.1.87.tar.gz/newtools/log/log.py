import logging
import sys

###########################################
#                                         #
#             HERE BE DRAGONS             #
#                                         #
#                                         #
#     .     _///_,                        #
#   .      / ` ' '>                       #
#     )   o'  __/_'>                      #
#    (   /  _/  )_\'>                     #
#     ' "__/   /_/\_>                     #
#         ____/_/_/_/                     #
#        /,---, _/ /                      #
#       ""  /_/_/_/                       #
#          /_(_(_(_                 \     #
#         (   \_\_\\_               )\    #
#          \'__\_\_\_\__            ).\   #
#          //____|___\__)           )_/   #
#          |  _  \'___'_(           /'    #
#           \_ (-'\'___'_\      __,'_'    #
#           __) \  \\___(_   __/.__,'     #
#        ,((,-,__\  '", __\_/. __,'       #
#                     '"./_._._-'         #
#                                         #
# THIS FILE NEEDS TO HAVE AUTOMATED TESTS #
#                                         #
###########################################

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))


def clean_children(logger):  # pragma: nocover
    """
    Check the child handlers and remove our handler if it is set
    :param logger: the logger to check the children of
    """
    for l in [logging.getLogger(name) for name in logging.root.manager.loggerDict]:
        if l.name.startswith(logger.name):
            for h in l.handlers:
                if h == handler:
                    l.removeHandler(h)


def already_set(logger):  # pragma: nocover
    """
    Check all parent handlers to see if the handler is already set in the hierarchy
    :param logger: the logger to check the parents of
    :return: True if our handler is already set
    """
    for l in [logging.getLogger(name) for name in logging.root.manager.loggerDict]:
        if logger.name.startswith(l.name):
            for h in l.handlers:
                if h == handler:
                    return True


def log_to_stdout(logger_name="dativa", level=logging.INFO):  # pragma: nocover
    # set up logging
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    clean_children(logger)

    if not already_set(logger):
        logger.addHandler(handler)

    return logger
