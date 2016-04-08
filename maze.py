# A simple maze solver.
# Given a file with a maze, prints a maze with a shortest path from start to
# end marked with +.
#
# An example of input and output (X is a start point, O is an exit point):
#   ##########    ##########
#   X  #     #    X++# +++ #
#   #  #  #  #    # +# +#++#
#   #     #  O    # ++++# +O
#   ##########    ##########

import collections
import sys


class Maze(object):

  def __init__(self, file):
    """Reads a maze from a file.

    Args:
        file: str, A file name with a maze.

    """
    self.maze = [line.strip() for line in open(file).readlines()]
    self.ylim = len(self.maze)
    self.xlim = len(self.maze[0])
    self.start = self.Find('X')
    self.end = self.Find('O')

  def Find(self, c):
    """Look up a starting and ending positions.
    Args:
      maze: 2-D maze array,
    Returns:
      (x, y) point
    Raise:
      LookupError
    """
    for y in range(self.ylim):
      for x in range(self.xlim):
        if c == self.maze[y][x]:
          return (y, x)
    raise LookupError("'%s' not found in maze" % c)

  def FindAdjs(self, psrc):
    """Finds all adjacent points.

    Args:
      psrc: (x, y), A point in maze.
    Returns:
      list of adjacent points.
    """
    def check(p):
        y, x = p
        if x < 0 or y < 0 or y >= self.ylim or x >= self.xlim:
          return False
        if self.maze[y][x] in (' ', 'X', 'O'):
          return True

        if self.maze[y][x] == '#':
          return False

        raise ValueError('Bad cell')

    y, x = psrc
    return  [p for p in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))
               if check(p)]


  def CollectPath(self, p, visited):
    """Collects a path from a point p to a starting point.

    Args:
      p: (y, x), A point.
      visited: {(y, x): (prevx, prevy)}, A dict of point to point links.
    Returns:
       A list of (y, x) points.
    """
    path = []
    while p != None:
      path.append(p)
      p = visited[p]
    path.reverse()
    return path


  def Solve(self):
    """Finds a shortest path in a maze from a starting point to the end point.

    Args:
      maze: 2-D maze array,
    Returns:
      A list of (y, x) points, A shortest path from start to end.
    """

    visited = {self.start: None}
    q = collections.deque([self.start])
    while q:
      p = q.popleft()
      for ap in self.FindAdjs(p):
        if ap not in visited:
          visited[ap] = p
          q.append(ap)
        if ap == self.end:
          return self.CollectPath(ap, visited)

  def Print(self, path):
    """Prints a maze with a path marked with +.

    Args:
      path: A list of (y, x) points.
    """
    maze = [[self.maze[y][x] for x in range(self.xlim)]
            for y in range(self.ylim)]
    for (y, x) in path:
      if maze[y][x] == ' ':
        maze[y][x] = '+'
    lines = '\n'.join([
        ''.join([
            maze[y][x] for x in range(self.xlim)])
        for y in range(self.ylim)])
    print lines


if len(sys.argv) == 2:
  maze = Maze(sys.argv[1])
  maze.Print(maze.Solve())
