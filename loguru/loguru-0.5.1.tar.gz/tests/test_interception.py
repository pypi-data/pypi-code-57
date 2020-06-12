import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def test_formatting(writer, make_logging_logger):
    fmt = "{name} - {file.name} - {function} - {level.name} - {level.no} - {line} - {module} - {message}"
    expected = "tests.test_interception - test_interception.py - test_formatting - DEBUG - 10 - 31 - test_interception - This is the message\n"

    logging_logger = make_logging_logger("tests", InterceptHandler())

    logger.add(writer, format=fmt)

    logging_logger.debug("This is the %s", "message")

    result = writer.read()
    assert result == expected


def test_intercept(writer, make_logging_logger):
    logging_logger = make_logging_logger(None, InterceptHandler())

    logging_logger.info("Nope")

    logger.add(writer, format="{message}")

    logging_logger.info("Test")

    result = writer.read()
    assert result == "Test\n"


def test_add_before_intercept(writer, make_logging_logger):
    logger.add(writer, format="{message}")
    logging_logger = make_logging_logger(None, InterceptHandler())

    logging_logger.info("Test")

    result = writer.read()
    assert result == "Test\n"


def test_remove_interception(writer, make_logging_logger):
    h = InterceptHandler()
    logging_logger = make_logging_logger("foobar", h)
    logger.add(writer, format="{message}")
    logging_logger.debug("1")
    logging_logger.removeHandler(h)
    logging_logger.debug("2")

    result = writer.read()
    assert result == "1\n"


def test_intercept_too_low(writer, make_logging_logger):
    make_logging_logger("tests.test_interception", InterceptHandler())
    logger.add(writer, format="{message}")
    logging.getLogger("tests").error("Nope 1")
    logging.getLogger("foobar").error("Nope 2")
    result = writer.read()
    assert result == ""


def test_multiple_intercept(writer, make_logging_logger):
    logging_logger_1 = make_logging_logger("test_1", InterceptHandler())
    logging_logger_2 = make_logging_logger("test_2", InterceptHandler())

    logger.add(writer, format="{message}")

    logging_logger_1.info("1")
    logging_logger_2.info("2")

    result = writer.read()
    assert result == "1\n2\n"


def test_exception(writer, make_logging_logger):
    logging_logger = make_logging_logger("tests.test_interception", InterceptHandler())
    logger.add(writer, format="{message}")

    try:
        1 / 0
    except:
        logging_logger.exception("Oops...")

    lines = writer.read().strip().splitlines()
    assert lines[0] == "Oops..."
    assert lines[-1] == "ZeroDivisionError: division by zero"
    assert sum(line.startswith("> ") for line in lines) == 1


def test_level_is_no(writer, make_logging_logger):
    logging_logger = make_logging_logger("tests", InterceptHandler())
    logger.add(writer, format="<lvl>{level.no} - {level.name} - {message}</lvl>", colorize=True)

    logging_logger.log(12, "Hop")

    result = writer.read()
    assert result == "12 - Level 12 - Hop\x1b[0m\n"


def test_level_does_not_exist(writer, make_logging_logger):
    logging.addLevelName(152, "FANCY_LEVEL")
    logging_logger = make_logging_logger("tests", InterceptHandler())
    logger.add(writer, format="<lvl>{level.no} - {level.name} - {message}</lvl>", colorize=True)

    logging_logger.log(152, "Nop")

    result = writer.read()
    assert result == "152 - Level 152 - Nop\x1b[0m\n"


def test_level_exist_builtin(writer, make_logging_logger):
    logging_logger = make_logging_logger("tests", InterceptHandler())
    logger.add(writer, format="<lvl>{level.no} - {level.name} - {message}</lvl>", colorize=True)

    logging_logger.error("Error...")

    result = writer.read()
    assert result == "\x1b[31m\x1b[1m40 - ERROR - Error...\x1b[0m\n"


def test_level_exists_custom(writer, make_logging_logger):
    logging.addLevelName(99, "ANOTHER_FANCY_LEVEL")
    logger.level("ANOTHER_FANCY_LEVEL", no=99, color="<green>", icon="")
    logging_logger = make_logging_logger("tests", InterceptHandler())

    logger.add(writer, format="<lvl>{level.no} - {level.name} - {message}</lvl>", colorize=True)

    logging_logger.log(99, "Yep!")

    result = writer.read()
    assert result == "\x1b[32m99 - ANOTHER_FANCY_LEVEL - Yep!\x1b[0m\n"


def test_using_logging_function(writer):
    logging.getLogger(None).addHandler(InterceptHandler())
    logger.add(writer, format="{function} {line} {module} {file.name} {message}")
    logging.warning("ABC")
    result = writer.read()
    assert result == "test_using_logging_function 156 test_interception test_interception.py ABC\n"
