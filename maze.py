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

import sys


def ReadMaze(file):
  """Reads a maze from a file.

  Args:
      file: str, A file name with a maze.
  Returns:
    2-D array with maze, (x, y) maze start, (x, y) maze exit
  """
  with open(file) as d:
    lines = [line.strip() for line in d.readlines()]
  maze = [[lines[y][x] for y in range(len(lines))]
          for x in range(len(lines[0]))]
  start = None
  end = None
  for x in range(len(maze)):
    for y in range(len(maze[0])):
      c = maze[x][y]
      if c == 'X':
        start = (x, y)
      if c == 'O':
        end = (x, y)
  return maze, start, end


def FindAdjs(maze, psrc):
  """Finds all adjacent points.

  Args:
    maze: 2-D array with maze.
    psrc: (x, y), A point in maze.
  Returns:
    list of adjacent points.
  """
  def check(p):
      x, y = p
      if x < 0 or y < 0 or y >= len(maze[0]) or x >= len(maze):
        return False
      if maze[x][y] in (' ', 'X', 'O'):
        return True

      if maze[x][y] == '#':
        return False

      raise Exception('Bad cell')

  x, y = psrc
  return  [p for p in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
             if check(p)]


def CollectPath(p, visited):
  """Collects a path from a point p to a starting point.

  Args:
    p: (x, y), A point.
    visited: {(x, y): (prevx, prevy)}, A dict of point to point links.
  Returns:
     A list of (x, y) points.
  """
  path = []
  while p != None:
    path.append(p)
    p = visited[p]
  path.reverse()
  return path


def FindPath(maze, start, end):
  """Finds a shortest path in a maze from a starting point to the end point.

  Args:
    maze: 2-D maze array,
    start: (x, y), A starting point.
    end: (x, y), An exit point.
  Returns:
    A list of (x, y) points, A shortest path from start to end.
  """
  visited = {start: None}
  lastVisited = visited.copy()

  while lastVisited:
    moreVisited = {}
    for p in lastVisited:
      for adjp in FindAdjs(maze, p):
        if adjp == end:
          return CollectPath(p, visited) + [end]
        if adjp not in visited:
          moreVisited[adjp] = p
    visited.update(moreVisited)
    lastVisited = moreVisited


def PrintMaze(maze, path):
  """Prints a solved maze with a path marked with +.

  Args:
    maze: 2-D maze array,
    path: A list of (x, y) points.
  """
  for (x, y) in path:
    if maze[x][y] == ' ':
      maze[x][y] = '+'
  lines = '\n'.join([
      ''.join([
          maze[x][y] for x in range(len(maze))])
      for y in range(len(maze[0]))])
  print lines


def Run(file):
  """Runs a maze solver for a maze in a file.

  Args:
    file: str, A file name with a maze.
  """
  maze, start, end = ReadMaze(file)
  path = FindPath(maze, start, end)
  PrintMaze(maze, path)


if len(sys.argv) == 2:
  Run(sys.argv[1])