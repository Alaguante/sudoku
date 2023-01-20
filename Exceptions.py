class NotAValidSudokuNumberException(Exception):
    """
    Raised when the given number is not in the range of 1 to 9.
    """
    pass


class NotInPosRangeException(Exception):
    """
    Raised when the given position is not in the range of 1 to 9.
    """
    pass


class PathNotFoundException(Exception):
    """
    Raised when the given path is not found.
    """
    pass


class NotAFileException(Exception):
    """
    Raised when the given path is not a file.
    """
    pass
