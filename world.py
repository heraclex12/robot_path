import queue
from robot import Robot
import copy
from draw import *
import random
import time
import sys

# Quy ước:
#            # : hình đa giác
#            0 : vị trí trống
#            + : lộ trình đường đi
#            S : vị trí bắt đầu
#            G : vị trí kết thúc
#            P : vị trí các điểm đón
#            * : viền/khung/giới hạn/ranh giới

class World():
    def __init__(self):
        self.leng = 0
        self.width = 0
        self.amount_polygan = 0
        self.polygans = []
        self.area = []
        self.robot = Robot(0, 0, 0, 0)
        self.amount_stop = 0
        self.stops = []

    def getWidth(self):
        return self.width

    def getLeng(self):
        return self.leng

    def read_input(self, filename : str):
        with open(filename, "r") as file:
            line = file.readline().strip("\\ \n\r\t")
            self.leng, self.width = [int(i) + 1 for i in line.split(",")]
            for i in range(self.width):
                row = []
                for j in range(self.leng):
                    if j == 0 or i == 0 or j == self.leng - 1 or i == self.width - 1:
                        row.append("*")
                    else:
                        row.append(0)

                self.area.append(row)

            line = file.readline().strip("\\ \n\r\t")
            tmp = [int(i) for i in line.split(",")]
            self.robot = Robot(tmp[1], tmp[0], tmp[3], tmp[2])
            for j in range(4, len(tmp), 2):
                self.stops.append((tmp[j + 1], tmp[j]))
                self.amount_stop += 1

            self.amount_polygan = file.readline().strip("\\ \n\r\t")
            if self.amount_polygan is not None and line != "":
                self.amount_polygan = int(self.amount_polygan)
                for i in range(self.amount_polygan):
                    polygan = []
                    line = file.readline().strip("\\ \n\r\t")
                    tmp = [int(i) for i in line.split(",")]
                    for j in range(0, len(tmp), 2):
                        polygan.append((tmp[j + 1], tmp[j]))

                    self.polygans.append(polygan)


    def eucliean_distance(self, x1, y1, x2, y2):
        return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5


    def drawing_polygan(self, polygan : list) -> list:
        def match_two_point(point_a : tuple, point_b : tuple) -> list:
            polygan_path = []
            if point_a[0] == point_b[0]:
                for match in range(0, abs(point_a[1] - point_b[1]) + 1):
                    if point_b[1] > point_a[1]:
                        self.area[point_a[0]][point_a[1] + match] = "#"
                        polygan_path.append((point_a[0], point_a[1] + match))

                    else:
                        self.area[point_a[0]][point_b[1] + match] = "#"
                        polygan_path.append((point_a[0], point_b[1] + match))

            elif point_a[1] == point_b[1]:
                for match in range(0, abs(point_a[0] - point_b[0]) + 1):
                    if point_b[0] > point_a[0]:
                        self.area[point_a[0] + match][point_a[1]] = "#"
                        polygan_path.append((point_a[0] + match, point_a[1]))

                    else:
                        self.area[point_b[0] + match][point_b[1]] = "#"
                        polygan_path.append((point_b[0] + match, point_b[1]))

            else:
                positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
                x_next = point_a[0]
                y_next = point_a[1]
                while not (x_next == point_b[0] and y_next == point_b[1]):
                    minimum = self.leng * self.width
                    x_tmp = x_next
                    y_tmp = y_next
                    for position in positions:
                        if 0 < x_next + position[0] < self.width and 0 < y_next + position[1] < self.leng:
                            if x_next + position[0] == point_b[0] and y_next + position[1] == point_b[1]:
                                x_tmp = point_b[0]
                                y_tmp = point_b[1]
                                break

                            if self.area[x_next + position[0]][y_next + position[1]] == 0:
                                path_weight = round(self.eucliean_distance(x_next + position[0], y_next + position[1], point_b[0], point_b[1]), 2)
                                if position[0] == 0 or position[1] == 0:
                                    path_weight += 1

                                else:
                                    path_weight += 1.50

                                if path_weight < minimum:
                                    minimum = path_weight
                                    x_tmp = x_next + position[0]
                                    y_tmp = y_next + position[1]

                    x_next = x_tmp
                    y_next = y_tmp
                    self.area[x_next][y_next] = "#"
                    polygan_path.append((x_next, y_next))

            return polygan_path

        self.area[polygan[0][0]][polygan[0][1]] = "#"
        polygan_path = [(polygan[0][0], polygan[0][1])]
        for index in range(1, len(polygan)):
            curr = polygan[index]
            prev = polygan[index - 1]
            polygan_path.extend(match_two_point(prev, curr))

        polygan_path.extend(match_two_point(polygan[0], polygan[len(polygan) - 1]))
        return polygan_path

    def find_permutation(self, k, perm):
        if k == 1:
            path_weight = 0
            min_cost = 0
            prev_stops = [self.robot.get_start_point()]
            prev_stops.extend(self.stops[:])
            prev_stops.append(self.robot.get_end_point())
            for point_index in range(len(perm) - 1):
                min_cost += round(self.eucliean_distance(prev_stops[point_index][0], prev_stops[point_index][1], prev_stops[point_index + 1][0], prev_stops[point_index + 1][1]), 2)
                path_weight += round(self.eucliean_distance(perm[point_index][0], perm[point_index][1], perm[point_index + 1][0], perm[point_index + 1][1]), 2)

            if path_weight < min_cost:
                self.stops = perm[1: len(perm) - 1]

        else:
            for i in range(1, k):
                self.find_permutation(k - 1, perm)
                if k % 2 == 0:
                    perm[i], perm[k] = perm[k], perm[i]
                else:
                    perm[1], perm[k] = perm[k], perm[1]

            self.find_permutation(k - 1, perm)


    def greedy_search(self, win):
        positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
        start_point = self.robot.get_start_point()
        end_point = self.robot.get_end_point()
        passing_points = []
        if self.amount_stop > 1:
            tmp_stops = [start_point]
            tmp_stops.extend(self.stops[:])
            tmp_stops.append(end_point)
            self.find_permutation(self.amount_stop, tmp_stops)

        passing_points.extend(self.stops[:])
        passing_points.append(end_point)
        best_cost = 0
        area_copy = copy.deepcopy(self.area)
        while passing_points:
            queue_points = []
            queue_points.append(start_point)
            end_point = passing_points.pop(0)
            color_robot = random_color()
            closed_points = copy.deepcopy(area_copy)
            while queue_points:
                curr_point = queue_points.pop(0)
                self.area[curr_point[0]][curr_point[1]] = "+"
                drawPath(processMaxtrix([(curr_point[0], curr_point[1])]),
                         color_robot, win, self.width - 1)
                x_tmp = curr_point[0]
                y_tmp = curr_point[1]
                if x_tmp == end_point[0] and y_tmp == end_point[1]:
                    break

                tmp_queue = []
                curr_weight = self.width * self.leng
                for position in positions:
                    if 0 < x_tmp + position[0] < self.width and 0 < y_tmp + position[1] < self.leng:
                        if self.area[x_tmp + position[0]][y_tmp + position[1]] == 0:
                            h_weight = round(
                                self.eucliean_distance(x_tmp + position[0], y_tmp + position[1], end_point[0],
                                                       end_point[1]), 2)
                            if position[0] == 0 or position[1] == 0:
                                h_weight += 1
                                best_cost += 1

                            else:
                                if self.area[x_tmp][y_tmp + position[1]] != 0 and self.area[x_tmp + position[0]][
                                    y_tmp] != 0:
                                    continue

                                h_weight += 1.50
                                best_cost += 1.50

                            if h_weight <= curr_weight:
                                curr_weight = h_weight
                                if closed_points[x_tmp + position[0]][y_tmp + position[1]] == 0:
                                    closed_points[x_tmp + position[0]][y_tmp + position[1]] = 1
                                    tmp_queue.insert(0, (x_tmp + position[0], y_tmp + position[1]))
                            else:
                                if closed_points[x_tmp + position[0]][y_tmp + position[1]] == 0:
                                    closed_points[x_tmp + position[0]][y_tmp + position[1]] = 1
                                    tmp_queue.append((x_tmp + position[0], y_tmp + position[1]))

                for i in range(len(tmp_queue) - 1, -1, -1):
                    queue_points.insert(0, tmp_queue[i])

            if self.area[end_point[0]][end_point[1]] == 0:
                return -1

            start_point = (end_point[0], end_point[1])

        return best_cost


    def dijkstra_search(self, win):
        positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
        queue_points = queue.Queue()
        start_point = self.robot.get_start_point()
        end_point = self.robot.get_end_point()
        queue_points.put(start_point)
        area_with_weight = copy.deepcopy(self.area)
        closed_points = copy.deepcopy(self.area)
        color_robot = random_color()
        while not queue_points.empty():
            curr_point = queue_points.get()
            x_tmp = curr_point[0]
            y_tmp = curr_point[1]
            if x_tmp == end_point[0] and y_tmp == end_point[1]:
                area_with_weight[start_point[0]][start_point[1]] = 0
                while not (end_point[0] == start_point[0] and end_point[1] == start_point[1]):
                    for position in positions:
                        if position[0] == 0 or position[1] == 0:
                            if area_with_weight[end_point[0]][end_point[1]] - 1 == area_with_weight[end_point[0] + position[0]][end_point[1] + position[1]]:
                                drawPath(processMaxtrix([(end_point[0] + position[0],end_point[1] + position[1])]), color_robot, win, self.width - 1)
                                end_point = (end_point[0] + position[0], end_point[1] + position[1])
                                break

                        else:
                            if area_with_weight[end_point[0]][end_point[1]] - 1.50 == area_with_weight[end_point[0] + position[0]][end_point[1] + position[1]]:
                                drawPath(processMaxtrix([(end_point[0] + position[0],end_point[1] + position[1])]), color_robot, win, self.width - 1)
                                end_point = (end_point[0] + position[0], end_point[1] + position[1])
                                break

                    self.area[end_point[0]][end_point[1]] = "+"

                break

            for position in positions:
                if 0 < x_tmp + position[0] < self.width and 0 < y_tmp + position[1] < self.leng:
                    if self.area[x_tmp + position[0]][y_tmp + position[1]] == 0:
                        if position[0] == 0 or position[1] == 0:
                            tmp_weight = area_with_weight[x_tmp][y_tmp] + 1
                        else:
                            if self.area[x_tmp][y_tmp + position[1]] != 0 and self.area[x_tmp + position[0]][y_tmp] != 0:
                                continue

                            tmp_weight = area_with_weight[x_tmp][y_tmp] + 1.50

                        if area_with_weight[x_tmp + position[0]][y_tmp + position[1]] == 0 or area_with_weight[x_tmp + position[0]][y_tmp + position[1]] > tmp_weight:
                            area_with_weight[x_tmp + position[0]][y_tmp + position[1]] = tmp_weight

                        if closed_points[x_tmp + position[0]][y_tmp + position[1]] == 0:
                            queue_points.put((x_tmp + position[0], y_tmp + position[1]))
                            closed_points[x_tmp + position[0]][y_tmp + position[1]] = 1

        end_point = self.robot.get_end_point()
        if area_with_weight[end_point[0]][end_point[1]] == 0:
            return -1

        return area_with_weight[end_point[0]][end_point[1]]


    def astar_search(self, win):
        positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
        start_point = self.robot.get_start_point()
        end_point = self.robot.get_end_point()
        passing_points = []
        if self.amount_stop > 1:
            tmp_stops = [start_point]
            tmp_stops.extend(self.stops[:])
            tmp_stops.append(end_point)
            self.find_permutation(self.amount_stop, tmp_stops)

        passing_points.extend(self.stops[:])
        passing_points.append(end_point)
        best_cost = 0
        area_copy = copy.deepcopy(self.area)
        while passing_points:
            queue_points = queue.Queue()
            queue_points.put(start_point)
            end_point = passing_points.pop(0)
            color_robot = random_color()
            area_with_weight = copy.deepcopy(area_copy)
            closed_points = copy.deepcopy(area_copy)
            while not queue_points.empty():
                curr_point = queue_points.get()
                x_tmp = curr_point[0]
                y_tmp = curr_point[1]
                if x_tmp == end_point[0] and y_tmp == end_point[1]:
                    best_cost += area_with_weight[x_tmp][y_tmp]
                    drawPath(processMaxtrix([(end_point[0], end_point[1])]), color_robot,
                             win, self.width - 1)
                    area_with_weight[start_point[0]][start_point[1]] = 0
                    while not (end_point[0] == start_point[0] and end_point[1] == start_point[1]):
                        for position in positions:
                            if position[0] == 0 or position[1] == 0:
                                if area_with_weight[end_point[0]][end_point[1]] - 1 == area_with_weight[end_point[0] + position[0]][end_point[1] + position[1]]:
                                    drawPath(processMaxtrix([(end_point[0] + position[0],end_point[1] + position[1])]), color_robot, win, self.width - 1)
                                    end_point = (end_point[0] + position[0], end_point[1] + position[1])
                                    break

                            else:
                                if area_with_weight[end_point[0]][end_point[1]] - 1.50 == area_with_weight[end_point[0] + position[0]][end_point[1] + position[1]]:
                                    drawPath(processMaxtrix([(end_point[0] + position[0],end_point[1] + position[1])]), color_robot, win, self.width - 1)
                                    end_point = (end_point[0] + position[0], end_point[1] + position[1])
                                    break

                        self.area[end_point[0]][end_point[1]] = "+"

                    break

                tmp_queue = []
                curr_weight = self.width * self.leng
                for position in positions:
                    if 0 < x_tmp + position[0] < self.width and 0 < y_tmp + position[1] < self.leng:
                        if self.area[x_tmp + position[0]][y_tmp + position[1]] == 0:
                            h_weight = round(self.eucliean_distance(x_tmp + position[0], y_tmp + position[1], end_point[0], end_point[1]), 2)
                            if position[0] == 0 or position[1] == 0:
                                tmp_weight = area_with_weight[x_tmp][y_tmp] + 1
                            else:
                                if self.area[x_tmp][y_tmp + position[1]] != 0 and self.area[x_tmp + position[0]][y_tmp] != 0:
                                    continue

                                tmp_weight = area_with_weight[x_tmp][y_tmp] + 1.50

                            if tmp_weight + h_weight < curr_weight:
                                curr_weight = tmp_weight + h_weight
                                if closed_points[x_tmp + position[0]][y_tmp + position[1]] == 0:
                                    closed_points[x_tmp + position[0]][y_tmp + position[1]] = 1
                                    tmp_queue.insert(0, (x_tmp + position[0], y_tmp + position[1]))
                            else:
                                if closed_points[x_tmp + position[0]][y_tmp + position[1]] == 0:
                                    closed_points[x_tmp + position[0]][y_tmp + position[1]] = 1
                                    tmp_queue.append((x_tmp + position[0], y_tmp + position[1]))

                            if area_with_weight[x_tmp + position[0]][y_tmp + position[1]] == 0 or area_with_weight[x_tmp + position[0]][y_tmp + position[1]] >= tmp_weight:
                                area_with_weight[x_tmp + position[0]][y_tmp + position[1]] = tmp_weight

                for e in tmp_queue:
                    queue_points.put(e)

            if area_with_weight[end_point[0]][end_point[1]] == 0 and end_point != start_point:
                return -1

            start_point = (x_tmp, y_tmp)

            

        return best_cost


    def print_area(self, win):
        start_point = self.robot.get_start_point()
        #self.area[start_point[0]][start_point[1]] = "S"
        drawText(start_point[1], start_point[0], self.width-1, win, "S", 20)
        end_point = self.robot.get_end_point()
        #self.area[end_point[0]][end_point[1]] = "G"
        drawText(end_point[1], end_point[0], self.width - 1, win, "G", 20)

        for i in self.stops:
            #self.area[i[0]][i[1]] = "P"
            drawText(i[1], i[0], self.width-1, win, "P", 20)
       # for i in range(self.width - 1, -1, -1):
           #for j in range(self.leng):
                #print(self.area[i][j], end=" ")
           # print()

    def moving_polygan(self, polygan : list, step : tuple):
        polygan_path = polygan[:]
        point_amount = len(polygan_path)
        for i in range(point_amount):
            if 0 < polygan_path[i][0] + step[0] < self.width and 0 < polygan_path[i][1] + step[1] < self.leng:
                if self.area[polygan_path[i][0] + step[0]][polygan_path[i][1] + step[1]] == "#" \
                        or self.area[polygan_path[i][0] + step[0]][polygan_path[i][1] + step[1]] == "*":
                    return False, []

                polygan_path[i] = (polygan_path[i][0] + step[0], polygan_path[i][1] + step[1])

            else:
                return False, []

        return True, polygan_path

    def greedy_search_with_dynamic(self, polygan_borders, color_robot, win):
        robot_path = []
        positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
        start_point = self.robot.get_start_point()
        passing_points = []
        passing_points.append(self.robot.get_end_point())
        polygan_steps = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        best_weight = 0
        while passing_points:
            end_point = passing_points.pop()
            x_next = start_point[0]
            y_next = start_point[1]
            border_amount = len(polygan_borders)
            while not (x_next == end_point[0] and y_next == end_point[1]):
                minimum = self.leng * self.width
                x_tmp = x_next
                y_tmp = y_next
                # polygan move
                index_border = 0
                tmp_step = polygan_steps[:]
                while index_border < border_amount:
                    if tmp_step:
                        step = random.choice(tmp_step)
                        tmp_step.remove(step)
                        for point in polygan_borders[index_border]:
                            self.area[point[0]][point[1]] = 0
                        ok_step, tmp_border = world.moving_polygan(polygan_borders[index_border], step)
                        if ok_step:
                            drawPath(processMaxtrix(polygan_borders[index_border]), color_rgb(255, 255, 255), win,
                                     self.width - 1)
                            polygan_borders[index_border] = tmp_border
                            for point in polygan_borders[index_border]:
                                self.area[point[0]][point[1]] = "#"
                            drawPath(processMaxtrix(polygan_borders[index_border]), random_color(), win,
                                     self.width - 1)
                            index_border += 1
                        else:
                            for point in polygan_borders[index_border]:
                                self.area[point[0]][point[1]] = "#"
                    else:
                        index_border += 1

                for position in positions:
                    if 0 < x_next + position[0] < self.width and 0 < y_next + position[1] < self.leng:
                        if self.area[x_next + position[0]][y_next + position[1]] == 0 or self.area[x_next + position[0]][y_next + position[1]] == "+":
                            path_weight = round(
                                self.eucliean_distance(x_next + position[0], y_next + position[1], end_point[0],
                                                       end_point[1]),
                                2)
                            if self.area[x_next + position[0]][y_next + position[1]] == "+":
                                path_weight += 1

                            if position[0] == 0 or position[1] == 0:
                                path_weight += 1

                            else:
                                if self.area[x_next][y_next + position[1]] != 0 and self.area[x_next + position[0]][
                                    y_next] != 0:
                                    continue

                                path_weight += 1.50

                            if x_next + position[0] == end_point[0] and y_next + position[1] == end_point[1]:
                                x_tmp = end_point[0]
                                y_tmp = end_point[1]
                                break

                            if path_weight < minimum:
                                minimum = path_weight
                                x_tmp = x_next + position[0]
                                y_tmp = y_next + position[1]

                if x_tmp - x_next == 0 or y_tmp - y_next == 0:
                    best_weight += 1.0

                else:
                    best_weight += 1.50

                if best_weight > self.width * self.leng:
                    return -1

                if self.area[x_next][y_next] != "#":
                    drawPath(processMaxtrix([(x_next, y_next)]), color_rgb(255, 255, 255), win, self.width - 1)
                x_next = x_tmp
                y_next = y_tmp
                robot_path.append((x_next, y_next))
                self.area[x_next][y_next] = "+"
                drawPath(processMaxtrix([(x_next, y_next)]), color_robot, win, self.width - 1)
                world.print_area(win)
                time.sleep(0.5)

            start_point = end_point
        drawPath(processMaxtrix(robot_path), color_robot, win, self.width - 1)
        return best_weight

    def drawing_dynamic_polygan(self, polygan : list) -> list:
        def match_two_point(point_a : tuple, point_b : tuple) -> list:
            polygan_path = []
            if point_a[0] == point_b[0]:
                for match in range(0, abs(point_a[1] - point_b[1]) + 1):
                    if point_b[1] > point_a[1]:
                        self.area[point_a[0]][point_a[1] + match] = "#"
                        polygan_path.append((point_a[0], point_a[1] + match))

                    else:
                        self.area[point_a[0]][point_b[1] + match] = "#"
                        polygan_path.append((point_a[0], point_b[1] + match))

            elif point_a[1] == point_b[1]:
                for match in range(0, abs(point_a[0] - point_b[0]) + 1):
                    if point_b[0] > point_a[0]:
                        self.area[point_a[0] + match][point_a[1]] = "#"
                        polygan_path.append((point_a[0] + match, point_a[1]))

                    else:
                        self.area[point_b[0] + match][point_b[1]] = "#"
                        polygan_path.append((point_b[0] + match, point_b[1]))

            else:
                positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
                x_next = point_a[0]
                y_next = point_a[1]
                while not (x_next == point_b[0] and y_next == point_b[1]):
                    minimum = self.leng * self.width
                    x_tmp = x_next
                    y_tmp = y_next
                    for position in positions:
                        if 0 < x_next + position[0] < self.width and 0 < y_next + position[1] < self.leng:
                            if x_next + position[0] == point_b[0] and y_next + position[1] == point_b[1]:
                                x_tmp = point_b[0]
                                y_tmp = point_b[1]
                                break

                            if self.area[x_next + position[0]][y_next + position[1]] == 0:
                                path_weight = round(self.eucliean_distance(x_next + position[0], y_next + position[1], point_b[0], point_b[1]), 2)
                                if position[0] == 0 or position[1] == 0:
                                    path_weight += 1

                                else:
                                    path_weight += 1.50

                                if path_weight < minimum:
                                    minimum = path_weight
                                    x_tmp = x_next + position[0]
                                    y_tmp = y_next + position[1]

                    x_next = x_tmp
                    y_next = y_tmp
                    self.area[x_next][y_next] = "#"
                    polygan_path.append((x_next, y_next))

            return polygan_path

        self.area[polygan[0][0]][polygan[0][1]] = "#"
        polygan_path = [(polygan[0][0], polygan[0][1])]
        save_side = []
        for index in range(1, len(polygan)):
            curr = polygan[index]
            prev = polygan[index - 1]
            side = match_two_point(prev, curr)
            if prev[1] < curr[1]:
                save_side.extend(side)

            polygan_path.extend(side)

        side = match_two_point(polygan[0], polygan[len(polygan) - 1])
        polygan_path.extend(side)
        area_polygan = []
        for up_side in save_side:
            for point in polygan_path:
                if up_side[1] == point[1]:
                    for k in range(point[0] + 1, up_side[0]):
                        area_polygan.append((k, up_side[1]))
        polygan_path.extend(area_polygan)
        return polygan_path


if __name__ == '__main__':
    task = None
    input_file = None
    if len(sys.argv) == 5:
        for i in range(len(sys.argv) - 1):
            if sys.argv[i] == "--input" or sys.argv[i] == "-i":
                input_file = sys.argv[i + 1]
            elif sys.argv[i] == "--search" or sys.argv[i] == "-s":
                task = sys.argv[i + 1]

        if input_file is None or input_file == "":
            print("No filename found!!!")
            exit(0)

        if task is None or task == "":
            print("No search algorithm found!!!")
            exit(0)

        world = World()
        world.read_input(input_file)
        width = world.getLeng()
        height = world.getWidth()
        ratio = 30
        win = GraphWin("robot_path", (width) * ratio, (height) * ratio)
        drawGrid(width - 1, height - 1, win)
        if task == "fuzzy":
            for polygan in world.polygans:
                drawPath(processMaxtrix(world.drawing_polygan(polygan)), random_color(), win, height - 1)
            s = world.dijkstra_search(win)
            if s == -1:
                world.print_area(win)
                drawText(width // 2, height - 1, height - 1, win, "Can't find away!!!", 20)
            else:
                world.print_area(win)
                drawText(width//2, height-1, height - 1, win,"Cost: "+str(s), 20)

        elif task == "greedy":
            for polygan in world.polygans:
                drawPath(processMaxtrix(world.drawing_polygan(polygan)), random_color(), win, height - 1)
            s = world.greedy_search(win)
            if s == -1:
                world.print_area(win)
                drawText(width // 2, height - 1, height - 1, win, "Can't find away!!!", 20)
            else:
                world.print_area(win)
                drawText(width//2, height-1, height - 1, win,"Cost: "+str(s), 20)


        elif task == "astar":
            for polygan in world.polygans:
                drawPath(processMaxtrix(world.drawing_polygan(polygan)), random_color(), win, height - 1)
            s = world.astar_search(win)
            if s == -1:
                world.print_area(win)
                drawText(width // 2, height - 1, height - 1, win, "Can't find away!!!", 20)
            else:
                world.print_area(win)
                drawText(width//2, height-1, height - 1, win,"Cost: "+str(s), 20)

        elif task == "moving":
            polygan_borders = []
            for polygan in world.polygans:
                border = world.drawing_dynamic_polygan(polygan)
                polygan_borders.append(border)
                drawPath(processMaxtrix(border), random_color(), win, height - 1)

            color_robot = random_color()
            s = world.greedy_search_with_dynamic(polygan_borders, color_robot, win)
            world.print_area(win)
            if s == -1:
                drawText(width // 2, height - 1, height - 1, win, "Can't find away!!!", 20)
            else:
                drawText(width//2, height-1, height - 1, win, "Cost: "+str(s), 20)


        else:
            print("Wrong search name!!!")

        win.getMouse()
        win.close()

    else:
        print("Missing argument values.")
