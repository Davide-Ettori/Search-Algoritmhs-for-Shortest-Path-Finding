import sys
import pygame
from time import sleep
from random import randint
#from min_heap import Min_heap

class Min_heap():
    def __init__(self, items=list()):
        self.heap = [None]

        for i in items:
            self.heap.append(i)
            self.float_up(len(self.heap) - 1)

    def print(self):
        print(self.heap[1:])

    def push(self, data):
        self.heap.append(data)
        self.float_up(len(self.heap) - 1)

    def peek(self):
        if len(self.heap) > 1:
            return self.heap[1]
        else:
            return False
    def pop(self):
        if len(self.heap) > 1:
            self.heap[1], self.heap[len(
                self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[1]
            minVal = self.heap.pop()
            self.heapify(1)
        else:
            minVal = False

        return minVal

    def float_up(self, index):
        parent = index // 2
        if index <= 1:
            return None
        elif self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self.float_up(parent)

    def heapify(self, index):
        left = index * 2
        right = left + 1
        smallest = index
        if len(self.heap) > left and self.heap[smallest] > self.heap[left]:
            smallest = left
        if len(self.heap) > right and self.heap[smallest] > self.heap[right]:
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.heapify(smallest)

step = 15
w = 810
h = 604

car = pygame.image.load('imgs/car_1.png')
wall = pygame.image.load('imgs/wall_1.jpg')
arr = pygame.image.load('imgs/arr_1.png')
sema = pygame.image.load('imgs/sema_1.jpg')

colors = [(0, 0, 150), (0, 150, 0), (150, 0, 150), (150, 0, 150), (0, 150, 150), (150, 150, 0)]
multi_ends = True

def init():
    pygame.init()

    global win
    win = pygame.display.set_mode((w, h + 50))

    global finish_arr
    finish_arr = list()

    global prev_col
    prev_col = (255, 255, 255)

    global prev_col_2
    prev_col_2 = (255, 255, 255)

    global algo
    algo = None

    global labirinto
    labirinto = True

    pygame.display.set_caption('Path Finding Algorithms')
class Pixel():
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos

    def draw(self):
        pygame.draw.rect(win, self.color, self.pos)

    def is_over(self, mouse):
        return mouse == (self.pos[0], self.pos[1])

class Grid():
    def __init__(self):
        self.mat = list()
        c = 0

        for i in range(0, w, step):
            self.mat.append(list())
            c += 1
            for y in range(0, h, step):
                self.mat[c - 1].append(Pixel((255, 255, 255),
                                             (i, y, step, step)))

        x_1 = 20
        y_1 = 20
        x_2 = 35
        y_2 = 20

        self.mat[x_1][y_1].color = (0, 255, 0)
        self.mat[x_2][y_2].color = (255, 0, 0)

        global ends_list
        ends_list = list([(35, 20)])

    def draw(self):
        for i in range(w // step):
            for y in range(h // step):
                if self.mat[i][y].color == (255, 0, 0):
                    continue

                self.mat[i][y].draw()

        for i in range(w // step):
            for y in range(h // step):
                pos = (self.mat[i][y].pos[0] - 6, self.mat[i][y].pos[1] - 6)
                pos_wall = self.mat[i][y].pos

                if self.mat[i][y].color == (0, 255, 0):
                    win.blit(pygame.transform.scale(car, (25, 25)), pos)

                if self.mat[i][y].color == (0, 0, 0):
                    win.blit(pygame.transform.scale(wall, (13, 13)), pos_wall)

                if self.mat[i][y].color == (255, 0, 0):
                    win.blit(pygame.transform.scale(arr, (25, 25)), pos)

                if self.mat[i][y].color == (255, 0, 255):
                    win.blit(pygame.transform.scale(sema, (18, 18)), pos_wall)

class Button():
    def __init__(self, color, pos, text=''):
        self.color = color
        self.pos = pos
        self.text = text

    def is_over(self, val):
        if val[0] > self.pos[0] and val[0] < self.pos[0] + self.pos[2]:
            if val[1] > self.pos[1] and val[1] < self.pos[1] + self.pos[3]:
                return True

        return False

    def draw(self):
        self.color = (122, 122, 122)
        self.pos = (380, 615, 120, 30)
        pygame.draw.rect(win, self.color, self.pos)

        if self.text != '':
            size = 15
            font = pygame.font.SysFont('comicsans', size)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (390, 618))
def drawGrid():
    for i in range(0, h, step):
        pass

    pygame.draw.line(win, (122, 122, 122), (0, i), (w, i))
    return None
def random_walls():
    global labirinto
    if not labirinto:
        return
    labirinto = False
    global grid

    for i in range(len(grid.mat)):
        for y in range(len(grid.mat[i])):
            if grid.mat[i][y].color == (255, 255, 255) and randint(1, 6) <= 2:
                grid.mat[i][y].color = (0, 0, 0)
                if randint(1, 4) == 1:
                    redraw(grid, Button(
                        (0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))

def redraw(grid, submit):
    win.fill((255, 255, 255))

    grid.draw()
    drawGrid()
    submit.draw()
    pygame.display.update()
def main():
    init()

    global grid
    global algo
    grid = Grid()
    clock = pygame.time.Clock()
    global submit
    global prev_col_2
    global ends_list

    submit = Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path')

    while True:
        clock.tick(30)
        pygame.event.pump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            random_walls()
            continue
        if keys[pygame.K_BACKSPACE]:
            grid = Grid()
            sleep(0.2)
            continue
        try:

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                pos = [pos[0] // step, pos[1] // step]

                if multi_ends and grid.mat[pos[0]][pos[1]].color == (255, 255, 255):
                    grid.mat[pos[0]][pos[1]].color = (255, 0, 0)
                    ends_list.append((pos[0], pos[1]))
                    sleep(0.1)
                elif grid.mat[pos[0]][pos[1]].color == (255, 0, 0) and len(get_ends()) > 1:
                    grid.mat[pos[0]][pos[1]].color = (255, 255, 255)
                    ends_list.remove((pos[0], pos[1]))
                    sleep(0.15)
                elif grid.mat[pos[0]][pos[1]].color == (0, 0, 0) or grid.mat[pos[0]][pos[1]].color == (255, 0, 255):
                    grid.mat[pos[0]][pos[1]].color = (255, 255, 255)
                    redraw(grid, submit)
                    while True:
                        val = False
                        pos = pygame.mouse.get_pos()
                        pos = [pos[0] // step, pos[1] // step]
                        if grid.mat[pos[0]][pos[1]].color == (0, 0, 0) or grid.mat[pos[0]][pos[1]].color == (255, 0, 255):
                            val = True
                            grid.mat[pos[0]][pos[1]].color = (255, 255, 255)

                        if val:
                            redraw(grid, submit)

                        try:
                            event = pygame.event.poll()

                            if event.type == pygame.MOUSEBUTTONUP:
                                break
                        except:
                            pass
        except:
            pass

        if event.type == pygame.MOUSEBUTTONDOWN and submit.is_over(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_u]:
                algo = 'Uniform'
                exec(algo + '()')
            elif keys[pygame.K_b]:
                algo = 'BFS'
                exec(algo + '()')
            elif keys[pygame.K_a]:
                algo = 'A_star'
                exec(algo + '()')
            elif keys[pygame.K_g]:
                algo = 'Greedy'
                exec(algo + '()')
            elif keys[pygame.K_d]:
                algo = 'DFS'
                exec(algo + '()')
            elif keys[pygame.K_r]:
                for i, coord in enumerate(ends_list):
                    if i == 0:
                        continue
                    grid.mat[coord[0]][coord[1]].color = (255, 255, 255)
                redraw(grid, Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))
                algo = "Reverse"
                exec(algo + '()')
            elif keys[pygame.K_w]:
                algo = "Weighted"
                exec(algo + '()')
            continue

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if pos[1] >= 600:
                continue
            pos = [pos[0] // step, pos[1] // step]

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] and grid.mat[pos[0]][pos[1]].color != (0, 0, 0) and grid.mat[pos[0]][pos[1]].color != (255, 0, 0) and grid.mat[pos[0]][pos[1]].color != (0, 0, 255):
                grid.mat[pos[0]][pos[1]].color = (255, 0, 255)
                while keys[pygame.K_LSHIFT]:
                    pos = pygame.mouse.get_pos()
                    pos = [pos[0] // step, pos[1] // step]
                    try:
                        val = grid.mat[pos[0]][pos[1]].color
                    except:
                        break
                    if grid.mat[pos[0]][pos[1]].color != (0, 0, 0) and grid.mat[pos[0]][pos[1]].color != (255, 0, 0) and grid.mat[pos[0]][pos[1]].color != (0, 255, 0):
                        grid.mat[pos[0]][pos[1]].color = (255, 0, 255)
                        redraw(grid, Button(
                            (0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))
                    pygame.event.pump()
                    keys = pygame.key.get_pressed()
                    event = pygame.event.poll()
                    if event.type == pygame.MOUSEBUTTONUP:
                        break
                continue

            if grid.mat[pos[0]][pos[1]].color == (255, 255, 255):
                grid.mat[pos[0]][pos[1]].color = (0, 0, 0)

            col = grid.mat[pos[0]][pos[1]].color

            if col == (255, 0, 0):
                try:
                    index = ends_list.index((pos[0], pos[1]))
                    ends_list.remove((pos[0], pos[1]))
                except:
                    pass

            while True:
                if pygame.mouse.get_pos()[1] >= 592:
                    break
                try:
                    event = pygame.event.poll()

                    if event.type == pygame.MOUSEBUTTONUP:
                        new_pos = pygame.mouse.get_pos()
                        new_pos = [new_pos[0] // step, new_pos[1] // step]
                        if col == (255, 0, 0):
                            ends_list.insert(index, tuple(new_pos))
                        break

                    new_pos = pygame.mouse.get_pos()
                    new_pos = [new_pos[0] // step, new_pos[1] // step]

                    if new_pos != pos:
                        if col == (255, 0, 0) or col == (0, 255, 0):
                            try:
                                val = grid.mat[new_pos[0]][new_pos[1]].color
                                if val == (255, 0, 0) or val == (0, 255, 0):
                                    if col == (255, 0, 0):
                                        ends_list.insert(index, tuple(pos))
                                    break
                            except:
                                if col == (255, 0, 0):
                                    ends_list.insert(index, tuple(pos))
                                break

                            grid.mat[pos[0]][pos[1]].color = prev_col_2
                            prev_col_2 = grid.mat[new_pos[0]][new_pos[1]].color
                            grid.mat[new_pos[0]][new_pos[1]].color = col

                        else:
                            try:
                                val = grid.mat[new_pos[0]][new_pos[1]].color
                            except:
                                break
                            if grid.mat[new_pos[0]][new_pos[1]].color != (255, 0, 0) and grid.mat[new_pos[0]][new_pos[1]].color != (0, 255, 0) and grid.mat[new_pos[0]][new_pos[1]].color != (255, 0, 255):
                                grid.mat[new_pos[0]][new_pos[1]
                                                     ].color = (0, 0, 0)
                        pos = new_pos

                    redraw(grid, submit)
                except Exception as e:
                    raise e

        redraw(grid, submit)
def finish(draw):
    global grid
    global submit
    global finish_arr
    global weigth

    for i in range(1, len(finish_arr) - 1):
        try:
            if grid.mat[finish_arr[i][0]][finish_arr[i][1]].color != (255, 0, 0):
                if grid.mat[finish_arr[i][0]][finish_arr[i][1]].color != (0, 255, 0):
                    grid.mat[finish_arr[i][0]][finish_arr[i]
                                               [1]].color = (255, 255, 0)
                    if draw and randint(1, 4) < 4:
                        redraw(grid, Button(
                            (0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))
        except:
            pass

    redraw(grid, Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))

    for i in range(len(grid.mat)):
        for y in range(len(grid.mat[i])):

            if (i, y) in weigth:
                grid.mat[i][y].color = (255, 0, 255)
def wait_for_click():
    global algo
    global grid
    global submit
    global prev_col
    global ends_list
    global colors
    global labirinto

    run = True

    while run:
        run = True

        event = pygame.event.poll()
        pygame.event.pump()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            grid = Grid()
            sleep(0.2)
            run = False
            labirinto = True

        try:

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                pos = [pos[0] // step, pos[1] // step]

                if algo == 'Reverse' and (grid.mat[pos[0]][pos[1]].color in colors or grid.mat[pos[0]][pos[1]].color == (255, 255, 255)):
                    continue

                if multi_ends and grid.mat[pos[0]][pos[1]].color == (255, 255, 255) or grid.mat[pos[0]][pos[1]].color == (0, 0, 255) or grid.mat[pos[0]][pos[1]].color == (255, 255, 0) or grid.mat[pos[0]][pos[1]].color in colors:
                    grid.mat[pos[0]][pos[1]].color = (255, 0, 0)
                    ends_list.append((pos[0], pos[1]))
                    delete_yellow_blue()

                    exec(algo + '(False)')
                elif grid.mat[pos[0]][pos[1]].color == (255, 0, 0) and len(get_ends()) > 1:
                    grid.mat[pos[0]][pos[1]].color = (255, 255, 255)
                    ends_list.remove((pos[0], pos[1]))
                    delete_yellow_blue()

                    exec(algo + '(False)')
                elif grid.mat[pos[0]][pos[1]].color == (0, 0, 0) or grid.mat[pos[0]][pos[1]].color == (255, 0, 255):
                    grid.mat[pos[0]][pos[1]].color = (255, 255, 255)
                    delete_yellow_blue()
                    exec(algo + '(False)')
                    while True:
                        if pygame.mouse.get_pos()[1] >= 592:
                            break
                        val = False
                        pos = pygame.mouse.get_pos()
                        pos = [pos[0] // step, pos[1] // step]
                        if grid.mat[pos[0]][pos[1]].color == (0, 0, 0) or grid.mat[pos[0]][pos[1]].color == (255, 0, 255):
                            val = True

                        if grid.mat[pos[0]][pos[1]].color != (255, 0, 0) and grid.mat[pos[0]][pos[1]].color != (0, 255, 0):
                            grid.mat[pos[0]][pos[1]].color = (255, 255, 255)

                        if val:
                            delete_yellow_blue()
                            exec(algo + '(False)')

                        try:
                            event = pygame.event.poll()

                            if event.type == pygame.MOUSEBUTTONUP:
                                break
                        except:
                            pass
                #continue
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                pos = [pos[0] // step, pos[1] // step]
                if grid.mat[pos[0]][pos[1]].color != (255, 0, 0) and grid.mat[pos[0]][pos[1]].color != (0, 255, 0):

                    pos = pygame.mouse.get_pos()
                    pos = [pos[0] // step, pos[1] // step]

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LSHIFT] and grid.mat[pos[0]][pos[1]].color != (0, 0, 0):
                        if grid.mat[pos[0]][pos[1]].color == (255, 255, 255) or grid.mat[pos[0]][pos[1]].color == (255, 255, 0) or grid.mat[pos[0]][pos[1]].color in colors:
                            grid.mat[pos[0]][pos[1]].color = (255, 0, 255)
                            delete_yellow_blue()

                            exec(algo + '(False)')

                        col = grid.mat[pos[0]][pos[1]].color

                        while keys[pygame.K_LSHIFT]:

                            event = pygame.event.poll()
                            pygame.event.pump()

                            if event.type == pygame.MOUSEBUTTONUP:
                                break

                            new_pos = pygame.mouse.get_pos()
                            new_pos = [new_pos[0] // step, new_pos[1] // step]

                            if new_pos != pos:
                                try:
                                    val = grid.mat[new_pos[0]
                                                   ][new_pos[1]].color
                                except:
                                    break
                                if grid.mat[new_pos[0]][new_pos[1]].color == (255, 255, 255) or grid.mat[new_pos[0]][new_pos[1]].color == (255, 255, 0) or grid.mat[new_pos[0]][new_pos[1]].color in colors:
                                    grid.mat[new_pos[0]][new_pos[1]
                                                         ].color = (255, 0, 255)
                                    delete_yellow_blue()
                                    exec(algo + '(False)')

                                pos = new_pos

                            if event.type == pygame.MOUSEBUTTONUP:
                                break

                        continue
                    if grid.mat[pos[0]][pos[1]].color == (255, 255, 255) or grid.mat[pos[0]][pos[1]].color == (255, 255, 0) or grid.mat[pos[0]][pos[1]].color in colors:
                        grid.mat[pos[0]][pos[1]].color = (0, 0, 0)
                        delete_yellow_blue()

                        exec(algo + '(False)')

                    col = grid.mat[pos[0]][pos[1]].color

                    while True:
                        if pygame.mouse.get_pos()[1] >= 592:
                            break
                        event = pygame.event.poll()

                        if event.type == pygame.MOUSEBUTTONUP:
                            break

                        new_pos = pygame.mouse.get_pos()
                        new_pos = [new_pos[0] // step, new_pos[1] // step]

                        if new_pos != pos:
                            try:
                                val = grid.mat[new_pos[0]][new_pos[1]].color
                            except:
                                break
                            if grid.mat[new_pos[0]][new_pos[1]].color == (255, 255, 255) or grid.mat[new_pos[0]][new_pos[1]].color == (255, 255, 0) or grid.mat[new_pos[0]][new_pos[1]].color in colors:
                                grid.mat[new_pos[0]][new_pos[1]
                                                     ].color = (0, 0, 0)
                                delete_yellow_blue()
                                exec(algo + '(False)')

                            pos = new_pos
                elif grid.mat[pos[0]][pos[1]].color == (255, 0, 0) or grid.mat[pos[0]][pos[1]].color == (0, 255, 0):
                    prev_pos = pos
                    colore = grid.mat[pos[0]][pos[1]].color

                    while True:
                        if pygame.mouse.get_pos()[1] >= 592:
                            break
                        pos = pygame.mouse.get_pos()
                        new_pos = [pos[0] // step, pos[1] // step]

                        if prev_pos != new_pos:
                            try:
                                val = grid.mat[new_pos[0]][new_pos[1]].color
                                if val == (255, 0, 0) or val == (0, 255, 0):
                                    break
                            except:
                                break
                            if colore == (255, 0, 0):
                                index = ends_list.index(tuple(prev_pos))
                                try:
                                    ends_list[index] = tuple(new_pos)
                                except:
                                    ends_list.append(tuple(new_pos))

                            grid.mat[prev_pos[0]][prev_pos[1]].color = prev_col
                            prev_col = grid.mat[new_pos[0]][new_pos[1]].color
                            grid.mat[new_pos[0]][new_pos[1]].color = colore
                            prev_pos = new_pos
                            delete_yellow_blue()
                            exec(algo + '(False)')

                        try:
                            event = pygame.event.poll()

                            if event.type == pygame.MOUSEBUTTONUP:
                                prev_col = (255, 255, 255)
                                break
                        except:
                            pass
        except:
            pass
def get_ends():
    global grid
    res = list()

    for i in range(len(grid.mat)):
        for y in range(len(grid.mat[i])):

            if grid.mat[i][y].color == (255, 0, 0):
                res.append((i, y))
    return res

def get_pos_mat():
    global grid

    for i in range(len(grid.mat)):
        for y in range(len(grid.mat[i])):

            if grid.mat[i][y].color == (0, 255, 0):
                return i, y

def check(data, ends):
    mem = set(data)

    for i in ends:
        if i in mem:
            ends.remove(i)
            return ends if len(ends) > 0 else 'END'
    return False
def get_weight():
    global grid
    res = set()

    for i in range(len(grid.mat)):
        for y in range(len(grid.mat[i])):

            if grid.mat[i][y].color == (255, 0, 255):
                res.add((i, y))
    return res

def A_star(draw=True, color=0):
    global grid
    global finish_arr
    global ends_list
    global weigth
    global colors

    weigth = get_weight()
    start = get_pos_mat()
    ends = ends_list[:]

    end = ends.pop(0)

    heap = Min_heap()
    store = dict()
    visited = set()
    num = 0

    cost = abs(end[0] - start[0]) + abs(end[1] - start[1]) + num
    store[cost] = [[start]]
    heap.push(cost)

    while heap.heap:
        num = heap.pop()

        try:
            path = store[num].pop()
        except:
            break

        if len(store[num]) == 0:
            del store[num]
        x, y = path[-1]
        if (x, y) in visited or y == 40:
            continue

        if end == (x, y):
            color += 1
            if color == 5:
                color = 0
            for item in path:
                finish_arr.append(item)
            if ends:
                start = end
                end = ends.pop(0)

                heap = Min_heap()
                store = dict()
                visited = set()

                cost = abs(end[0] - start[0]) + abs(end[1] - start[1])
                store[cost] = [[start]]
                heap.push(cost)
                continue

            else:
                if draw:
                    finish(draw)
                    finish_arr = list()
                    wait_for_click()

                    return None
                else:
                    finish(draw)
                    finish_arr = list()

                    return None

        visited.add((x, y))

        if grid.mat[x][y].color != (0, 255, 0) and grid.mat[x][y].color != (255, 0, 0) and grid.mat[x][y].pos[1] < 600 and grid.mat[x][y].color != (255, 0, 255):
            grid.mat[x][y].color = colors[color]

        if draw:
            grid.mat[x][y].draw()
            pygame.display.update()

        if x + 1 < len(grid.mat) and grid.mat[x + 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x + 1, y))

            if (x+1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = abs(end[0] - (x + 1)) + abs(end[1] - y) + num + w - (abs(end[0] - x) + abs(end[1] - y))
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y + 1 < len(grid.mat[x]) and grid.mat[x][y + 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y + 1))

            if (x, y+1) in weigth:
                w = 15
            else:
                w = 1

            cost = abs(end[0] - x) + abs(end[1] - (y + 1)) + num + w - (abs(end[0] - x) + abs(end[1] - y))
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if x - 1 > -1 and grid.mat[x - 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x - 1, y))

            if (x-1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = abs(end[0] - (x - 1)) + abs(end[1] - y) + num + w - (abs(end[0] - x) + abs(end[1] - y))
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y - 1 > -1 and grid.mat[x][y - 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y - 1))

            if (x, y-1) in weigth:
                w = 15
            else:
                w = 1

            cost = abs(end[0] - x) + abs(end[1] - (y - 1)) + num + w - (abs(end[0] - x) + abs(end[1] - y))
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

    redraw(grid, Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))

    if draw:
        wait_for_click()

def Weighted(draw=True, color=0):
    global grid
    global finish_arr
    global ends_list
    global weigth
    global colors

    weigth = get_weight()
    start = get_pos_mat()
    ends = ends_list[:]

    end = ends.pop(0)

    heap = Min_heap()
    store = dict()
    visited = set()
    num = 0

    cost = 2*abs(end[0] - start[0]) + 2*abs(end[1] - start[1]) + num
    store[cost] = [[start]]
    heap.push(cost)

    while heap.heap:
        num = heap.pop()

        try:
            path = store[num].pop()
        except:
            break

        if len(store[num]) == 0:
            del store[num]
        x, y = path[-1]
        if (x, y) in visited or y == 40:
            continue

        if end == (x, y):
            color += 1
            if color == 5:
                color = 0
            for item in path:
                finish_arr.append(item)
            if ends:
                start = end
                end = ends.pop(0)

                heap = Min_heap()
                store = dict()
                visited = set()

                cost = 2*abs(end[0] - start[0]) + 2*abs(end[1] - start[1])
                store[cost] = [[start]]
                heap.push(cost)
                continue

            else:
                if draw:
                    finish(draw)
                    finish_arr = list()
                    wait_for_click()

                    return None
                else:
                    finish(draw)
                    finish_arr = list()

                    return None

        visited.add((x, y))

        if grid.mat[x][y].color != (0, 255, 0) and grid.mat[x][y].color != (255, 0, 0) and grid.mat[x][y].pos[1] < 600 and grid.mat[x][y].color != (255, 0, 255):
            grid.mat[x][y].color = colors[color]

        if draw:
            grid.mat[x][y].draw()
            pygame.display.update()

        if x + 1 < len(grid.mat) and grid.mat[x + 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x + 1, y))

            if (x+1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = 2*abs(end[0] - (x + 1)) + 2*abs(end[1] - y) + num + w - 2*(abs(end[0] - x) + abs(end[1] - y))
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y + 1 < len(grid.mat[x]) and grid.mat[x][y + 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y + 1))

            if (x, y+1) in weigth:
                w = 15
            else:
                w = 1

            cost = 2*abs(end[0] - x) + 2*abs(end[1] - (y + 1)) + num + w - 2*(abs(end[0] - x) + abs(end[1] - y))
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if x - 1 > -1 and grid.mat[x - 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x - 1, y))

            if (x-1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = 2*abs(end[0] - (x - 1)) + 2*abs(end[1] - y) + num + w - 2*(abs(end[0] - x) + abs(end[1] - y))
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y - 1 > -1 and grid.mat[x][y - 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y - 1))

            if (x, y-1) in weigth:
                w = 15
            else:
                w = 1

            cost = 2*abs(end[0] - x) + 2*abs(end[1] - (y - 1)) + num + w - 2*(abs(end[0] - x) + abs(end[1] - y))
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

    redraw(grid, Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))

    if draw:
        wait_for_click()
def BFS(draw=True, color=0):
    global grid
    global finish_arr
    global ends_list
    global weigth
    global colors

    weigth = get_weight()
    start = get_pos_mat()
    ends = ends_list[:]

    end = ends.pop(0)

    heap = Min_heap()
    store = dict()
    visited = set()
    num = 0

    cost = -1
    store[cost] = [[start]]
    heap.push(cost)

    while heap.heap:
        num = heap.pop()

        try:
            path = store[num].pop()
        except:
            break

        if len(store[num]) == 0:
            del store[num]
        x, y = path[-1]
        if (x, y) in visited or y == 40:
            continue

        if end == (x, y):
            color += 1
            if color == 5:
                color = 0
            for item in path:
                finish_arr.append(item)
            if ends:
                start = end
                end = ends.pop(0)

                heap = Min_heap()
                store = dict()
                visited = set()

                cost = 0
                store[cost] = [[start]]
                heap.push(cost)
                continue

            else:
                if draw:
                    finish(draw)
                    finish_arr = list()
                    wait_for_click()

                    return None
                else:
                    finish(draw)
                    finish_arr = list()

                    return None

        visited.add((x, y))

        if grid.mat[x][y].color != (0, 255, 0) and grid.mat[x][y].color != (255, 0, 0) and grid.mat[x][y].pos[1] < 600 and grid.mat[x][y].color != (255, 0, 255):
            grid.mat[x][y].color = colors[color]

        if draw:
            grid.mat[x][y].draw()
            pygame.display.update()

        if x + 1 < len(grid.mat) and grid.mat[x + 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x + 1, y))

            if (x+1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = num + 1
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y + 1 < len(grid.mat[x]) and grid.mat[x][y + 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y + 1))

            if (x, y+1) in weigth:
                w = 15
            else:
                w = 1

            cost = num + 1
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if x - 1 > -1 and grid.mat[x - 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x - 1, y))

            if (x-1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = num + 1
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y - 1 > -1 and grid.mat[x][y - 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y - 1))

            if (x, y-1) in weigth:
                w = 15
            else:
                w = 1

            cost = num + 1
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

    redraw(grid, Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))

    if draw:
        wait_for_click()

def Reverse(draw=True, start=None, ends=None, color=0):
    if color == 5:
        color = 0
    global grid
    global finish_arr
    global weigth

    weigth = get_weight()

    submit = Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path')

    if not start:
        x, y = get_pos_mat()
        x_end, y_end = get_ends()[0]
        arr = [[(x_end, y_end)]]
        start = (x_end, y_end)
        ends = [(x, y)]
    else:
        arr = [[start]]

    store = set()

    while arr:

        i = arr.pop(0)

        x, y = i[-1][0], i[-1][1]

        if str(x) + ',' + str(y) in store or y == 40:
            continue

        store.add(str(x) + ',' + str(y))
        value = check(i, ends)

        if value != False:
            if value == 'END':
                if draw:
                    for item in i:
                        finish_arr.append(item)
                    finish(draw)
                    finish_arr = list()
                    wait_for_click()

                    return None
                else:
                    for item in i:
                        finish_arr.append(item)
                    finish(draw)
                    finish_arr = list()
                    redraw(grid, Button(
                        (0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))

                    return None

            else:
                for item in i:
                    finish_arr.append(item)
                BFS(draw, (x, y), value, color + 1)

                return None

        if grid.mat[x][y].color != (0, 255, 0) and grid.mat[x][y].color != (255, 0, 0) and grid.mat[x][y].pos[1] < 600:
            global colors
            grid.mat[x][y].color = colors[color]

        if draw:
            grid.mat[x][y].draw()
            pygame.display.update()

        if x + 1 < len(grid.mat) and grid.mat[x + 1][y].color != (0, 0, 0):
            val = i[:]
            val.append((x + 1, y))
            arr.append(val)

        if y + 1 < len(grid.mat[x]) and grid.mat[x][y + 1].color != (0, 0, 0):
            val = i[:]
            val.append((x, y + 1))
            arr.append(val)

        if x - 1 > -1 and grid.mat[x - 1][y].color != (0, 0, 0):
            val = i[:]
            val.append((x - 1, y))
            arr.append(val)

        if y - 1 > -1 and grid.mat[x][y - 1].color != (0, 0, 0):
            val = i[:]
            val.append((x, y - 1))
            arr.append(val)

    redraw(grid, Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))

    if draw:
        wait_for_click()

def Uniform(draw=True, color=0):
    global grid
    global finish_arr
    global ends_list
    global weigth
    global colors

    weigth = get_weight()
    start = get_pos_mat()
    ends = ends_list[:]

    end = ends.pop(0)

    heap = Min_heap()
    store = dict()
    visited = set()
    num = 0

    cost = num
    store[cost] = [[start]]
    heap.push(cost)

    while heap.heap:
        num = heap.pop()

        try:
            path = store[num].pop()
        except:
            break

        if len(store[num]) == 0:
            del store[num]
        x, y = path[-1]
        if (x, y) in visited or y == 40:
            continue

        if end == (x, y):
            color += 1
            if color == 5:
                color = 0
            for item in path:
                finish_arr.append(item)
            if ends:
                start = end
                end = ends.pop(0)

                heap = Min_heap()
                store = dict()
                visited = set()

                cost = 0
                store[cost] = [[start]]
                heap.push(cost)
                continue

            else:
                if draw:
                    finish(draw)
                    finish_arr = list()
                    wait_for_click()

                    return None
                else:
                    finish(draw)
                    finish_arr = list()

                    return None

        visited.add((x, y))

        if grid.mat[x][y].color != (0, 255, 0) and grid.mat[x][y].color != (255, 0, 0) and grid.mat[x][y].pos[1] < 600 and grid.mat[x][y].color != (255, 0, 255):
            grid.mat[x][y].color = colors[color]

        if draw:
            grid.mat[x][y].draw()
            pygame.display.update()

        if x + 1 < len(grid.mat) and grid.mat[x + 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x + 1, y))

            if (x+1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = num + w
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y + 1 < len(grid.mat[x]) and grid.mat[x][y + 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y + 1))

            if (x, y+1) in weigth:
                w = 15
            else:
                w = 1

            cost = num + w
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if x - 1 > -1 and grid.mat[x - 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x - 1, y))

            if (x-1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = num + w
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y - 1 > -1 and grid.mat[x][y - 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y - 1))

            if (x, y-1) in weigth:
                w = 15
            else:
                w = 1

            cost = num + w
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

    redraw(grid, Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))

    if draw:
        wait_for_click()

def Greedy(draw=True, color=0):
    global grid
    global finish_arr
    global ends_list
    global weigth
    global colors

    weigth = get_weight()
    start = get_pos_mat()
    ends = ends_list[:]

    end = ends.pop(0)

    heap = Min_heap()
    store = dict()
    visited = set()
    num = 0

    cost = abs(end[0] - start[0]) + abs(end[1] - start[1])
    store[cost] = [[start]]
    heap.push(cost)

    while heap.heap:
        num = heap.pop()

        try:
            path = store[num].pop()
        except:
            break

        if len(store[num]) == 0:
            del store[num]
        x, y = path[-1]
        if (x, y) in visited or y == 40:
            continue

        if end == (x, y):
            color += 1
            if color == 5:
                color = 0
            for item in path:
                finish_arr.append(item)
            if ends:
                start = end
                end = ends.pop(0)

                heap = Min_heap()
                store = dict()
                visited = set()

                cost = abs(end[0] - start[0]) + abs(end[1] - start[1])
                store[cost] = [[start]]
                heap.push(cost)
                continue

            else:
                if draw:
                    finish(draw)
                    finish_arr = list()
                    wait_for_click()

                    return None
                else:
                    finish(draw)
                    finish_arr = list()

                    return None

        visited.add((x, y))

        if grid.mat[x][y].color != (0, 255, 0) and grid.mat[x][y].color != (255, 0, 0) and grid.mat[x][y].pos[1] < 600 and grid.mat[x][y].color != (255, 0, 255):
            grid.mat[x][y].color = colors[color]

        if draw:
            grid.mat[x][y].draw()
            pygame.display.update()

        if x + 1 < len(grid.mat) and grid.mat[x + 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x + 1, y))

            if (x+1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = abs(end[0] - (x + 1)) + abs(end[1] - y)
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y + 1 < len(grid.mat[x]) and grid.mat[x][y + 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y + 1))

            if (x, y+1) in weigth:
                w = 15
            else:
                w = 1

            cost = abs(end[0] - x) + abs(end[1] - (y + 1))
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if x - 1 > -1 and grid.mat[x - 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x - 1, y))

            if (x-1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = abs(end[0] - (x - 1)) + abs(end[1] - y)
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y - 1 > -1 and grid.mat[x][y - 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y - 1))

            if (x, y-1) in weigth:
                w = 15
            else:
                w = 1

            cost = abs(end[0] - x) + abs(end[1] - (y - 1))
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

    redraw(grid, Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))

    if draw:
        wait_for_click()

def DFS(draw=True, color=0):
    global grid
    global finish_arr
    global ends_list
    global weigth
    global colors

    weigth = get_weight()
    start = get_pos_mat()
    ends = ends_list[:]

    end = ends.pop(0)

    heap = Min_heap()
    store = dict()
    visited = set()
    num = 0

    cost = -1
    store[cost] = [[start]]
    heap.push(cost)

    while heap.heap:
        num = heap.pop()

        try:
            path = store[num].pop()
        except:
            break

        if len(store[num]) == 0:
            del store[num]
        x, y = path[-1]
        if (x, y) in visited or y == 40:
            continue

        if end == (x, y):
            color += 1
            if color == 5:
                color = 0
            for item in path:
                finish_arr.append(item)
            if ends:
                start = end
                end = ends.pop(0)

                heap = Min_heap()
                store = dict()
                visited = set()

                cost = 0
                store[cost] = [[start]]
                heap.push(cost)
                continue

            else:
                if draw:
                    finish(draw)
                    finish_arr = list()
                    wait_for_click()

                    return None
                else:
                    finish(draw)
                    finish_arr = list()

                    return None

        visited.add((x, y))

        if grid.mat[x][y].color != (0, 255, 0) and grid.mat[x][y].color != (255, 0, 0) and grid.mat[x][y].pos[1] < 600 and grid.mat[x][y].color != (255, 0, 255):
            grid.mat[x][y].color = colors[color]

        if draw:
            grid.mat[x][y].draw()
            pygame.display.update()

        if x + 1 < len(grid.mat) and grid.mat[x + 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x + 1, y))

            if (x+1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = num - 1
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y + 1 < len(grid.mat[x]) and grid.mat[x][y + 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y + 1))

            if (x, y+1) in weigth:
                w = 15
            else:
                w = 1

            cost = num - 1
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if x - 1 > -1 and grid.mat[x - 1][y].color != (0, 0, 0):
            temp = path[:]
            temp.append((x - 1, y))

            if (x-1, y) in weigth:
                w = 15
            else:
                w = 1

            cost = num - 1
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

        if y - 1 > -1 and grid.mat[x][y - 1].color != (0, 0, 0):
            temp = path[:]
            temp.append((x, y - 1))

            if (x, y-1) in weigth:
                w = 15
            else:
                w = 1

            cost = num - 1
            if cost not in store:
                store[cost] = [temp]
            else:
                store[cost] += [temp]

            heap.push(cost)

    redraw(grid, Button((0, 0, 0), (180, 515, 113, 20), 'Find Best Path'))

    if draw:
        wait_for_click()
def delete_yellow_blue():
    global grid
    global colors
    global labirinto
    labirinto = True

    for i in range(len(grid.mat)):
        for y in range(len(grid.mat[i])):
            if grid.mat[i][y].color == (255, 255, 0) or grid.mat[i][y].color in colors:
                grid.mat[i][y].color = (255, 255, 255)

main()