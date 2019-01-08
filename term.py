#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Fonctions permettant de styliser l'affichage dans le terminal"""

import sys

OFF = '\033[0m\033[27m'
BOLD = '\033[1m'
DIM = '\033[2m'
UNDERSCORE = '\033[4m'
BLINK = '\033[5m'
REVERSE = ' \033[7m'
HIDE = '\033[8m'

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

BGBLACK = '\033[40m'
BGRED = '\033[41m'
BGGREEN = '\033[42m'
BGYELLOW = '\033[43m'
BGBLUE = '\033[44m'
BGMAGENTA = '\033[45m'
BGCYAN = '\033[46m'
BGWHITE = '\033[47m'


def send(cmd):
    sys.stdout.write(cmd)
    sys.stdout.flush()


def up(value=1):
    send('\033[%sA' % value)


def down(value=1):
    send('\033[%sB' % value)


def right(value=1):
    send('\033[%sC' % value)


def left(value=1):
    send('\033[%sD' % value)


def clear():
    send('\033[2J')


def clear_line_from_pos():
    send('\033[K')


def clear_line_to_pos():
    send('\033[1K')


def clear_line():
    send('\033[2K')


def clear_previous_line():
    up(1)
    clear_line()


def bold(txt):
    return str(BOLD) + str(txt) + str(OFF)


def underscore(txt):
    return str(UNDERSCORE) + str(txt) + str(OFF)


def black(txt):
    return str(BLACK) + str(txt) + str(OFF)


def red(txt):
    return str(RED) + str(txt) + str(OFF)


def green(txt):
    return str(GREEN) + str(txt) + str(OFF)


def yellow(txt):
    return str(YELLOW) + str(txt) + str(OFF)


def blue(txt):
    return str(BLUE) + str(txt) + str(OFF)


def magenta(txt):
    return str(MAGENTA) + str(txt) + str(OFF)


def cyan(txt):
    return str(CYAN) + str(txt) + str(OFF)


def white(txt):
    return str(WHITE) + str(txt) + str(OFF)


def print_separator(c):
    send(c * get_size()[1]+'\n')


def get_size():
    import platform
    os_sys = platform.system()
    if (os_sys in ['Linux', 'Darwin'] or os_sys.startswith('CYGWIN')):
        try:
            def __get_unix_terminal_size(fd):
                import fcntl, termios, struct
                return struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                       'rene'))

            cr = __get_unix_terminal_size(0) or __get_unix_terminal_size(
                1) or __get_unix_terminal_size(2)
            if (not cr):
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = __get_unix_terminal_size(fd)
                os.close(fd)
            return cr
        except:
            pass
    else:
        raise Exception('operating system not supported')
