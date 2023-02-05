import sys
from pathlib import Path

print(sys.path[0])
path = str(Path(__file__).parent.parent.absolute())

print(path)