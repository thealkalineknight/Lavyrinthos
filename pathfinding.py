from collections import deque
import pygame as pg  # remove later

# Notes:
# parent not used really, but keep
# Pop current off open list line 58 not
# h variable lol


class Node:
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0


class Pathfinding:
    def __init__(self, game):
        self.game = game
        self.brac_map = game.map.num_map
        self.par_map = game.map.cor_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.visited = None
        self.graph = {}
        self.get_graph()

    def get_path(self, start, goal):
        self.visited = self.astar(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        key = pg.key.get_pressed()
        if key[pg.K_m]:
            print(path[::-1])
            print('-------------------------------')
        return path[-1]

    def astar(self, start, goal, graph):
        start_node = Node(None, start)
        end_node = Node(None, goal)
        start_node.g = start_node.h = start_node.f = 0
        end_node.g = end_node.h = end_node.f = 0

        queue = deque([start_node])
        visited = {start: None}

        while queue:

            cur_node = queue.popleft()
            # cur_index = 0
            for index, item in enumerate(queue):
                if item.f < cur_node.f:
                    cur_node = item
                    # cur_index = index
                    print('.f compared')

            if cur_node == end_node:
                break
            next_nodes = graph[cur_node.pos]

            # main
            for next_node in next_nodes:
                if next_node in visited:
                    continue
                test = Node(cur_node, next_node)
                test.g = cur_node.g + 1
                # h var looooool
                test.f = test.g + test.h
                for open_node in queue:
                    if test == open_node and test.g > open_node.g:
                        print('.g compared')  # flag
                        continue
                queue.append(test)
                visited[next_node] = cur_node.pos

        return visited

    def get_next_nodes(self, x, y):
        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.par_map]

    def get_graph(self):
        for y, row in enumerate(self.brac_map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)
