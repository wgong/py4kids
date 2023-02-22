## How to "install" a .tar.gz file or .tar.bz2 file. .tar.gz files are gzip-compressed tarballs, compressed archives like .zip files. .bz2 files are compressed with bzip2. 


You can extract .tar.gz files using:
```
tar xzf file.tar.gz
```

Similarly you can extract .tar.bz2 files with

```
tar xjf file.tar.bz2
```

If you would like to see the files being extracted during unpacking, add v:

```
tar xzvf file.tar.gz
```
