from os import O_RDWR, close, devnull, dup, dup2, open as os_open


class Suppress:
    """Context manager to suppress output."""
    def __enter__(self):
        self._stdout_fd = dup(1)
        self._stderr_fd = dup(2)

        self._devnull = os_open(devnull, O_RDWR)
        dup2(self._devnull, 1)
        dup2(self._devnull, 2)

    def __exit__(self, exc_type, exc_value, traceback):
        dup2(self._stdout_fd, 1)
        dup2(self._stderr_fd, 2)
        close(self._devnull)
        close(self._stdout_fd)
        close(self._stderr_fd)
