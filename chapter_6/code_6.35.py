import os


def acquire_lock(file_name):
    f = open(file_name, "a+")
    f.seek(0)
    # Windows
    if os.name.lower() == "nt":
        import win32con, win32file, pywintypes

        _overlapped = pywintypes.OVERLAPPED()
        f_handle = win32file._get_osfhandle(f.fileno())
        win32file.LockFileEx(f_handle, win32con.LOCKFILE_EXCLUSIVE_LOCK, 0, 0xFFFF0000, _overlapped)
    # Unix like
    elif os.name.lower() == "posix":
        import fcntl

        fcntl.flock(f, fcntl.LOCK_EX)
        return f


def release_lock(f):
    if f:
        f.close()


file_descr = acquire_lock("some-file.txt")

release_lock(file_descr)
