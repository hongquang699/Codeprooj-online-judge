import sys
d = sys.stdin.read().split()
if d:
    print(max(int(d[0]), int(d[1])))
