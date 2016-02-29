dbfuse
======

nsls-ii databroker in a filesystem? ... what a terrible idea.

requires
========

1. fusepy (some py3k fixes [here](https://github.com/klauer/fusepy))
2. python 3.4
3. linux-based system with fuse (maybe osxfuse would work, too?)
4. your user in the fuse group


go
==

```sh
$ ./go.sh
```

```
$ ls -laht mnt
-r-xr-xr-x 1 klauer klauer  23K Feb 29 10:08 d64f7b03-237b-4688-a19b-c9830ae2b633
-r-xr-xr-x 1 klauer klauer  23K Feb 29 10:08 scan05739
-r-xr-xr-x 1 klauer klauer  22K Feb 29 10:07 d4591759-6967-4808-978e-b28b25d38c43
-r-xr-xr-x 1 klauer klauer  22K Feb 29 10:07 scan05738
-r-xr-xr-x 1 klauer klauer 3.4K Feb 29 10:07 3cf84af8-199c-49a0-94be-d564eadc1063
-r-xr-xr-x 1 klauer klauer 3.4K Feb 29 10:07 scan05737
-r-xr-xr-x 1 klauer klauer 3.4K Feb 29 10:05 d46267e5-4db5-45bd-9fe7-3b11c0015c3a
-r-xr-xr-x 1 klauer klauer 3.4K Feb 29 10:05 scan05736
...
```
