import sys
import threading
import errno
import pprint

from fusell import FUSELL
from .path_tree import (PathTree, ReadableString)


import databroker


class FileSystem(FUSELL):
    def __init__(self, *args, **kwargs):
        self.lock = threading.RLock()
        super().__init__(*args, **kwargs)

    def create_ino(self):
        with self.lock:
            self.ino += 1
            return self.ino

    def create_ino_range(self, num):
        with self.lock:
            start_inode = self.ino
            self.ino += num
            end_inode = self.ino
            return start_inode + 1, end_inode + 1

    def init(self, userdata, conn):
        self.ino = 0
        self.trees = {}
        self.ino_owners = {}

        tree = PathTree(self, parent_inode=1)

        for relative_id in range(-100, -1):
            start = databroker.db[relative_id].start
            uid = str(start.uid)
            scanid = str(start.scan_id)

            obj = ReadableString(pprint.pformat(start))
            for entry in [tree.add_file(uid, obj=obj),
                          tree.add_file('scan{:05d}'.format(int(scanid)),
                                        obj=obj)]:
                entry.attr['st_ctime'] = start.time
                entry.attr['st_mtime'] = start.time
                entry.attr['st_atime'] = start.time

    forget = None

    def find_owner(self, inode):
        # TODO missing data structure
        if inode <= self.ino:
            for tree_inode, tree in self.trees.items():
                if inode in tree:
                    return tree

        raise ValueError('Unknown inode')

    def getattr(self, req, ino, fi):
        print('getattr:', ino)
        if ino in self.trees:
            tree = self.trees[ino]
            self.reply_attr(req, tree.attr, 1.0)
            return
        else:
            try:
                tree = self.find_owner(ino)
            except ValueError:
                pass
            else:
                entry = tree.inode_to_entry[ino]
                self.reply_attr(req, entry.attr, 1.0)
                return

        self.reply_err(req, errno.ENOENT)

    def lookup(self, req, parent_inode, name):
        parent = self.trees[parent_inode]
        try:
            entry = parent.entries[name.decode('utf-8')]
        except KeyError:
            self.reply_err(req, errno.ENOENT)
        except Exception as ex:
            self.reply_err(req, errno.ENOENT)
            print('unhandled lookup exception', ex, ':')
            try:
                print('\t', repr(name))
            except Exception:
                pass
        else:
            entry = dict(ino=entry.inode,
                         attr=entry.attr,
                         atttr_timeout=1.0,
                         entry_timeout=.0)
            self.reply_entry(req, entry)

    def readdir(self, req, ino, size, off, fi):
        entries = self.trees[ino].get_entries()
        self.reply_readdir(req, size, off, entries)

    def read(self, req, ino, size, offset, fi):
        print('read:', ino, size, offset)
        try:
            tree = self.find_owner(ino)
        except ValueError:
            self.reply_err(req, errno.EIO)
        else:
            self.reply_buf(req, tree.read(ino, size, offset))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: %s <mountpoint>' % sys.argv[0])
        sys.exit(1)
    fuse = FileSystem(sys.argv[1])
