mkdir mnt
kill -9 %
sleep 1.0

fusermount -u mnt
python -m dbfuse.dbfs mnt
