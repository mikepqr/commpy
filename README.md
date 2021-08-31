# comm.py

Python implementation of the POSIX utility `comm`: select or reject lines common to two files

# Usage

    $ cat f1
    a
    b
    c

    $ cat f2
    b
    c
    d

    $ commpy f1 f2
    a
                    b
                    c
            d

    $ commpy --help
    Usage: commpy [OPTIONS] FILE1 FILE2

    Arguments:
      FILE1  [required]
      FILE2  [required]

    Options:
      -1                              Suppress printing of column 1
      -2                              Suppress printing of column 2
      -3                              Suppress printing of column 3
      -i                              Case insensitive comparison of lines (not
                                      implemented)
