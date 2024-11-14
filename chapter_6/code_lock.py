import fcntl


def lock(self, cmd, owner, **kw):
    # The code here is much rather just a demonstration of the locking
    # API than something which actually was seen to be useful.

    # Advisory file locking is pretty messy in Unix, and the Python
    # interface to this doesn't make it better.
    # We can't do fcntl(2)/F_GETLK from Python in a platfrom independent
    # way. The following implementation *might* work under Linux.
    #
    # if cmd == fcntl.F_GETLK:
    #     import struct
    #
    #     lockdata = struct.pack('hhQQi', kw['l_type'], os.SEEK_SET,
    #                            kw['l_start'], kw['l_len'], kw['l_pid'])
    #     ld2 = fcntl.fcntl(self.fd, fcntl.F_GETLK, lockdata)
    #     flockfields = ('l_type', 'l_whence', 'l_start', 'l_len', 'l_pid')
    #     uld2 = struct.unpack('hhQQi', ld2)
    #     res = {}
    #     for i in xrange(len(uld2)):
    #          res[flockfields[i]] = uld2[i]
    #
    #     return fuse.Flock(**res)

    # Convert fcntl-ish lock parameters to Python's weird
    # lockf(3)/flock(2) medley locking API...
    op = {fcntl.F_UNLCK: fcntl.LOCK_UN, fcntl.F_RDLCK: fcntl.LOCK_SH, fcntl.F_WRLCK: fcntl.LOCK_EX}[kw["l_type"]]
    if cmd == fcntl.F_GETLK:
        return -errno.EOPNOTSUPP
    elif cmd == fcntl.F_SETLK:
        if op != fcntl.LOCK_UN:
            op |= fcntl.LOCK_NB
    elif cmd == fcntl.F_SETLKW:
        pass
    else:
        return -errno.EINVAL

    fcntl.lockf(self.fd, op, kw["l_start"], kw["l_len"])
