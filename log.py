#!/usr/bin/env python

"""
Logging util for JSONbox.

Expands on standard logging util by wrapping with colors and timestamps.

"""

import inspect

import logging

logger = logging.getLogger()
formatter = logging.Formatter(
    fmt='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

logging.basicConfig(format='\r[%(asctime)s] [%(levelname)s] %(message)s',
                   datefmt='%H:%M:%S',
                   level=logging.DEBUG,
                   filename='logfile.txt'
                   )

logging.addLevelName(logging.DEBUG,
                     "\033[1;90m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))  # Gray
logging.addLevelName(logging.INFO,
                     "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.INFO))  # Light Blue
logging.addLevelName(logging.WARNING,
                     "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))  # Yellow
logging.addLevelName(logging.ERROR,
                     "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))  # Red
logging.addLevelName(logging.CRITICAL,
                     "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))  # Invert red

DEBUG_APPLICATION = True
LOG_TRACES = True
QUIET = False

try:
    unicode
    _unicode = True
except NameError:
    _unicode = False


class bcolors:
    """Colors for general use. Done using terminal escape sequences."""

    PURPLE = '\033[35m'
    BRIGHT_PURPLE = '\033[95m'

    BLUE = '\033[34m'
    BRIGHT_BLUE = '\033[94m'

    GREEN = '\033[32m'
    BRIGHT_GREEN = '\033[92m'

    BLACK = '\033[30m'
    BRIGHT_BLACK = '\033[90m'
    GREY = BRIGHT_BLACK

    WHITE = '\033[37m'
    BRIGHT_WHITE = '\033[97m'

    YELLOW = '\033[33m'
    BRIGHT_YELLOW = '\033[93m'

    RED = '\033[31m'
    BRIGHT_RED = '\033[91m'  # High Red

    ENDC = '\033[0m'  # Reset
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class OutputHandler(logging.Handler):
    """Logging handler which calls function with log text."""

    def __init__(self, function):
        logging.Handler.__init__(self)
        self.function = function

    def emit(self, record):
        try:
            msg = self.format(record)
            self.function(msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def debug(message):
    """Only print if debugging is enabled."""
    message = str(message)
    if DEBUG_APPLICATION:
        logger.debug(prepend_caller(message))


# Multi-line debugging output
def trace(message):
    """Print a mutliline string, for things like tracebacks."""
    if DEBUG_APPLICATION and LOG_TRACES:
        for line in message.split("\n"):
            logger.debug(bcolors.GREY + "[TRACE] " + line + bcolors.ENDC)


def info(message):
    """Print generic information, hidden when in quiet mode."""
    if QUIET is False:
        message = str(message)
        logger.info(prepend_caller(message))


def warn(message):
    """Print for warning, but not error purposes."""
    message = str(message)
    logger.warning(prepend_caller(message))


warning = warn


def error(message):
    """Print information which caused the program not to operate as desired."""
    message = str(message)
    logger.error(prepend_caller(message))


def fatal(message):
    """Print errors which the program cannot possibly recover from."""
    message = str(message)
    logger.critical(prepend_caller(message))


def prepend_caller(message):
    """Get the common name for the caller."""
    caller = get_caller_name()
    if caller.startswith("__main__"):
        caller = caller.replace("__main__", bcolors.PURPLE + "Main" + bcolors.ENDC)
    elif "modules." in caller:
        caller = caller.replace("modules", bcolors.BLUE + "Modules" + bcolors.ENDC)
    elif caller.startswith("responder."):
        caller = bcolors.GREEN + caller.split("responder.", 1)[1] + bcolors.ENDC
    elif "JSONboxCmd" in caller:
        caller = bcolors.PURPLE + "User" + bcolors.ENDC

    message = "[" + caller + "]" + " " + message
    return message


# Code from gist: https://gist.github.com/techtonik/2151727
def get_caller_name(skip=3):
    """Get a name of a caller in the format module.class.method.

    `skip` specifies how many levels of stack to skip while getting caller
    name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

    An empty string is returned if skipped levels exceed stack height.
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append(codename)  # function or a method
    del parentframe
    return ".".join(name)

if __name__ == "__main__":
    stdoutlog = logging.StreamHandler()
    stdoutlog.setFormatter(formatter)
    logger.addHandler(stdoutlog)

    logger.setLevel(logging.DEBUG)

    logger.debug("Debug " + bcolors.BLUE + "info" + bcolors.ENDC)
    logger.info("Info info, with info")
    logger.warning("Warning info")
    logger.error("Error info")
    logger.critical("Critical info")
