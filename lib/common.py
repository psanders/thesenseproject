import os
import fcntl

DATA_FOLDER = '/home/pi/thesenseproject/data/'

def lockFile(lockfile):
    	fd = os.open(lockfile, os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
    	try:
    	    fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    	except IOError:
    	    return False

    	return True


def unlockFile(lockfile):
	fd = os.open(lockfile, os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
	try:
		fcntl.lockf(fd, fcntl.LOCK_UN)
	except IOError:
		return False
	return True
