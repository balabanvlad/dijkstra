import pygame as pg
from heapq import *
import dijkstra_conf
from random import randint


class App:
    def __init__(self):
        self.cols, self.rows = 30, 20
        self.TITLE = 30
        self.sc = pg.display.set_mode([self.cols * self.TITLE, self.rows * self.TITLE])
        grid = dijkstra_conf.grid
        self.grid = [[int(char) for char in string] for string in grid]
        self.pondere = 2

    def get_click_mouse_pos(self):
        x, y = pg.mouse.get_pos()
        grid_x, grid_y = x // self.TITLE, y // self.TITLE
        # pg.draw.rect(self.sc, pg.Color('darkorange'), self.get_rect(grid_x, grid_y))
        if self.pondere == 1:  # drumul
            self.draw_road(grid_x, grid_y)
        if self.pondere == 8:  # apa
            self.draw_water(grid_x, grid_y)
        if self.pondere == 9:  # piatra
            self.draw_rock(grid_x, grid_y)
        if self.pondere == 3:  # iarba
            self.draw_grass(grid_x, grid_y)
        click = pg.mouse.get_pressed()
        return (grid_x, grid_y) if click[0] else False

    def get_click_mouse_pos_right(self):
        x, y = pg.mouse.get_pos()
        grid_x, grid_y = x // self.TITLE, y // self.TITLE
        # pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))
        click = pg.mouse.get_pressed()
        return (grid_x, grid_y) if click[2] else False

    def get_circle(self, x, y):
        return (x * self.TITLE + self.TITLE // 2, y * self.TITLE + self.TITLE // 2), self.TITLE // 4

    def get_rect(self, x, y):
        return x * self.TITLE + 1, y * self.TITLE + 1, self.TITLE - 2, self.TITLE - 2

    def draw_rock(self, x, y):
        IMAGE = pg.image.load('img/rock.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)
        # pg.draw.rect(self.sc, (145, 124, 111), self.get_rect(x, y), border_radius=self.TITLE // 8)

    def draw_water(self, x, y):
        IMAGE = pg.image.load('img/water.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)
        # pg.draw.rect(self.sc, (18, 173, 130), self.get_rect(x, y), border_radius=self.TITLE // 8)

    def draw_road(self, x, y):
        IMAGE = pg.image.load('img/road.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def draw_grass(self, x, y):
        IMAGE = pg.image.load('img/grass.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def draw_word(self, x, y):
        IMAGE = pg.image.load('img/alege2.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def get_next_nodes(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(self.grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def Draw_Map(self):
        pg.init()
        clock = pg.time.Clock()
        while True:
            # fill screen
            self.sc.fill((143, 173, 18))
            # click stang i click drept
            mouse_pos_l = self.get_click_mouse_pos()
            mouse_pos_r = self.get_click_mouse_pos_right()
            if mouse_pos_l == (29, 0):
                self.Draw_Path()
            if mouse_pos_l == (28, 0):
                self.pondere = 9

            if mouse_pos_l == (27, 0):
                self.pondere = 8
            if mouse_pos_l == (26, 0):
                self.pondere = 3
            if mouse_pos_l == (25, 0):
                self.pondere = 1

            if mouse_pos_l:
                self.grid[mouse_pos_l[1]][mouse_pos_l[0]] = self.pondere
                pg.draw.rect(self.sc, pg.Color('forestgreen'), self.get_rect(*mouse_pos_l),
                             border_radius=self.TITLE // 8)

            if mouse_pos_r:
                self.grid[mouse_pos_r[1]][mouse_pos_r[0]] = 2
                pg.draw.rect(self.sc, pg.Color('red'), self.get_rect(*mouse_pos_r), border_radius=self.TITLE // 8)

            for y, row in enumerate(self.grid):
                for x, col in enumerate(row):
                    if col == 1:  # drumul
                        self.draw_road(x, y)
                    if col == 8:  # apa
                        self.draw_water(x, y)
                    if col == 9:  # piatra
                        self.draw_rock(x, y)
                    if col == 3:  # iarba
                        self.draw_grass(x, y)

            pg.draw.rect(self.sc, pg.Color('yellow'), self.get_rect(29, 0), border_radius=self.TITLE // 100)
            self.draw_word(24, 0)
            self.draw_road(25, 0)
            self.draw_grass(26, 0)
            self.draw_water(27,0)
            self.draw_rock(28,0)
            # pygame necessary lines
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            clock.tick(30)

    def Draw_Path(self):
        pg.init()
        clock = pg.time.Clock()
        for i in range(25,30):
            self.grid[0][i] = 2
        # mouse_pos_l = self.get_click_mouse_pos()
        # pg.draw.rect(self.sc, pg.Color('yellow'), self.get_rect(29, 0), border_radius=self.TITLE // 100)
        # if mouse_pos_l == (29, 0):
        #     self.Draw_Map()

        # dict of adjacency lists
        graph = {}
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                graph[(x, y)] = graph.get((x, y), []) + self.get_next_nodes(x, y)

        start = (0, 9)
        goal = (29, 9)
        queue = []
        heappush(queue, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        while True:
            # fill screen
            self.sc.fill((143, 173, 18))
            # [pg.draw.rect(sc, pg.Color('forestgreen'), self.get_rect(x, y), 1) for x, y in visited] # arata drumul vizitat
            # pg.draw.circle(self.sc, pg.Color('red'), *self.get_circle(*goal))

            for y, row in enumerate(self.grid):
                for x, col in enumerate(row):
                    if col == 1:  # drumul
                        self.draw_road(x, y)
                    if col == 8:  # apa
                        self.draw_water(x, y)
                    if col == 9:  # piatra
                        self.draw_rock(x, y)
                    if col == 3:  # iarba
                        self.draw_grass(x, y)

            # Dijkstra logic
            if queue:
                cur_cost, cur_node = heappop(queue)
                if cur_node == goal:
                    queue = []
                    continue

                next_nodes = graph[cur_node]
                for next_node in next_nodes:
                    neigh_cost, neigh_node = next_node
                    new_cost = cost_visited[cur_node] + neigh_cost
                    if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                        heappush(queue, (new_cost, neigh_node))
                        cost_visited[neigh_node] = new_cost
                        visited[neigh_node] = cur_node

            # draw path
            path_head, path_segment = cur_node, cur_node
            while path_segment:
                pg.draw.circle(self.sc, pg.Color('yellow'), *self.get_circle(*path_segment))
                path_segment = visited[path_segment]
            pg.draw.circle(self.sc, pg.Color('blue'), *self.get_circle(*start))
            pg.draw.circle(self.sc, pg.Color('red'), *self.get_circle(*path_head))
            # pygame necessary lines
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            clock.tick(30)


if __name__ == '__main__':
    draw = App()
    draw.Draw_Path()
