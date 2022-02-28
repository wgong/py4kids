from dirsync import sync
sourcedir = "C:/HD_BACKUP"
targetdir = "E:/HD_BACKUP"
sync(sourcedir, targetdir, "sync", purge=True, verbose=False, force=False)