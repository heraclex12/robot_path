from robot import Robot
import copy
from draw import *
from graphics import *
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
        self.robot = Robot(0,0,0,0)
        self.amount_stop = 0
        self.stops = []

    def read_input(self):
        with open("input_2.txt", "r") as file:
            line = file.readline().strip("\s\n\r\t")
            self.leng, self.width = [int(i) + 1 for i in line.split(",")]
            for i in range(self.width):
                row = []
                for j in range(self.leng):
                    if j == 0 or i == 0 or j == self.leng - 1 or i == self.width - 1:
                        row.append("*")
                    else:
                        row.append(0)

                self.area.append(row)

            line = file.readline().strip("\s\n\r\t")
            tmp = [int(i) for i in line.split(",")]
            self.robot = Robot(tmp[1], tmp[0], tmp[3], tmp[2])
            for j in range(4, len(tmp), 2):
                self.stops.append((tmp[j + 1], tmp[j]))

            self.amount_polygan = file.readline().strip("\s\n\r\t")
            if self.amount_polygan is not None and line != "":
                self.amount_polygan = int(self.amount_polygan)
                for i in range(self.amount_polygan):
                    polygan = []
                    line = file.readline().strip("\s\n\r\t")
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


    def greedy_search(self) -> list:
        def find_permutation(k: int, min_c: int, perm: list, cost: int):
            if k == 1:
                if min_c > cost:
                    min_c = cost
                return
            for i in range(k - 1):
                find_permutation(k - 1, min_c, perm, cost)
                if k % 2 == 0:
                    perm[i], perm[k - 1] = perm[k - 1], perm[i]
                    if i >= 1:
                        cost -= self.eucliean_distance(perm[k - 1][0], perm[k - 1][1], perm[i + 1][0], perm[i + 1][1])
                        cost -= self.eucliean_distance(perm[k - 1][0], perm[k - 1][1], perm[i - 1][0], perm[i - 1][1])
                        cost += self.eucliean_distance(perm[i][0], perm[i][1], perm[i + 1][0], perm[i + 1][1])
                        cost += self.eucliean_distance(perm[i][0], perm[i][1], perm[i - 1][0], perm[i - 1][1])
                    else:
                        cost -= self.eucliean_distance(perm[k - 1][0], perm[k - 1][1], perm[i + 1][0], perm[i + 1][1])
                        cost += self.eucliean_distance(perm[i][0], perm[i][1], perm[i + 1][0], perm[i + 1][1])

                    if k - 1 >= 1:
                        cost -= self.eucliean_distance(perm[i][0], perm[i][1], perm[k][0], perm[k][1])
                        cost += self.eucliean_distance(perm[k - 1][0], perm[k - 1][1], perm[k][0], perm[k][1])
                        cost -= self.eucliean_distance(perm[i][0], perm[i][1], perm[k - 2][0], perm[k - 2][1])
                        cost += self.eucliean_distance(perm[k - 1][0], perm[k - 1][1], perm[k - 2][0], perm[k - 2][1])
                    else:
                        cost -= self.eucliean_distance(perm[i][0], perm[i][1], perm[k][0], perm[k][1])
                        cost += self.eucliean_distance(perm[k - 1][0], perm[k - 1][1], perm[k][0], perm[k][1])

                else:
                    perm[0], perm[k - 1] = perm[k - 1], perm[0]
                    cost -= self.eucliean_distance(perm[k - 1][0], perm[k - 1][1], perm[1][0], perm[1][1])
                    cost += self.eucliean_distance(perm[0][0], perm[0][1], perm[1][0], perm[1][1])
                    if k - 1 >= 1:
                        cost -= self.eucliean_distance(perm[0][0], perm[0][1], perm[k][0], perm[k][1])
                        cost += self.eucliean_distance(perm[k - 1][0], perm[k - 1][1], perm[k][0], perm[k][1])
                        cost -= self.eucliean_distance(perm[0][0], perm[0][1], perm[k - 2][0], perm[k - 2][1])
                        cost += self.eucliean_distance(perm[k - 1][0], perm[k - 1][1], perm[k - 2][0], perm[k - 2][1])
                    else:
                        cost -= self.eucliean_distance(perm[0][0], perm[0][1], perm[k][0], perm[k][1])
                        cost += self.eucliean_distance(perm[k - 1][0], perm[k - 1][1], perm[k][0], perm[k][1])

            find_permutation(k - 1, min_c, perm, cost)


        robot_path = []
        positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
        start_point = self.robot.get_start_point()
        passing_points = []
        passing_points.extend(self.stops)
        if len(passing_points) >= 2:
            cost = self.eucliean_distance(start_point[0], start_point[1], passing_points[0][0], passing_points[0][1])
            for i in range(0, len(passing_points) - 1):
                cost += self.eucliean_distance(passing_points[i][0], passing_points[i][1], passing_points[i + 1][0], passing_points[i + 1][1])
            find_permutation(len(passing_points) - 1, cost, passing_points, cost)
        passing_points.append(self.robot.get_end_point())
        cnt = 1
        while passing_points:
            minimum = self.leng * self.width
            stop_index = 0
            for point_index in range(len(passing_points) - 1):
                path_weight = round(self.eucliean_distance(start_point[0], start_point[1], passing_points[point_index][0], passing_points[point_index][1]), 2)
                if path_weight < minimum:
                    minimum = path_weight
                    stop_index = point_index

            end_point = passing_points.pop(stop_index)
            x_next = start_point[0]
            y_next = start_point[1]
            while not (x_next == end_point[0] and y_next == end_point[1]):
                minimum = self.leng * self.width
                x_tmp = x_next
                y_tmp = y_next
                for position in positions:
                    if 0 < x_next + position[0] < self.width and 0 < y_next + position[1] < self.leng:
                        if self.area[x_next + position[0]][y_next + position[1]] == 0:
                            path_weight = round(
                                self.eucliean_distance(x_next + position[0], y_next + position[1], end_point[0], end_point[1]),
                                2)
                            if position[0] == 0 or position[1] == 0:
                                path_weight += 1

                            else:
                                if self.area[x_next][y_next + position[1]] != 0 and self.area[x_next + position[0]][y_next] != 0:
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

                x_next = x_tmp
                y_next = y_tmp
                robot_path.append((x_next, y_next))
                self.area[x_next][y_next] = "+" * cnt
                start_point = end_point
            cnt += 1

        return robot_path

    def dijkstra_search(self) -> list:
        robot_path = []
        positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
        queue_points = list()
        closed_points = {}
        for i in range(1, self.width):
            closed_points[i] = set()
        start_point = self.robot.get_start_point()
        end_point = self.robot.get_end_point()
        queue_points.append(start_point)
        area_with_weight = copy.deepcopy(self.area)
        while queue_points:
            curr_point = queue_points.pop(0)
            x_tmp = curr_point[0]
            y_tmp = curr_point[1]
            closed_points[x_tmp].add(y_tmp)
            for position in positions:
                if type(self.area[x_tmp + position[0]][y_tmp + position[1]]) != str:
                    if position[0] == 0 or position[1] == 0:
                        tmp_weight = area_with_weight[x_tmp][y_tmp] + 1
                    else:
                        if position[0] != 0 and position[1] != 0:
                            if self.area[x_tmp][y_tmp + position[1]] != 0 and self.area[x_tmp + position[0]][y_tmp] != 0:
                                continue

                        tmp_weight = area_with_weight[x_tmp][y_tmp] + 1.50

                    if area_with_weight[x_tmp + position[0]][y_tmp + position[1]] == 0 or area_with_weight[x_tmp + position[0]][y_tmp + position[1]] > tmp_weight:
                        area_with_weight[x_tmp + position[0]][y_tmp + position[1]] = tmp_weight

                    if 0 < x_tmp + position[0] < self.width and 0 < y_tmp + position[1] < self.leng:
                        if y_tmp + position[1] not in closed_points[x_tmp + position[0]]:
                            if position[0] != 0 and position[1] != 0:
                                if self.area[x_tmp][y_tmp + position[1]] != 0 and self.area[x_tmp + position[0]][y_tmp] != 0:
                                    continue

                            queue_points.append((x_tmp + position[0], y_tmp + position[1]))

            if x_tmp == end_point[0] and y_tmp == end_point[1]:
                # This print command is only for tests
                # for i in range(self.width - 1, -1, -1):
                #     for j in range(self.leng):
                #         if type(area_with_weight[i][j]) == float:
                #             if area_with_weight[i][j] >= 10.0:
                #                 print(area_with_weight[i][j], end = " ")
                #             else:
                #                 print(str(area_with_weight[i][j]) + "-", end=" ")
                #         else:
                #             print(str(area_with_weight[i][j]) + "---", end=" ")
                #     print()
                area_with_weight[start_point[0]][start_point[1]] = 0
                while not (end_point[0] == start_point[0] and end_point[1] == start_point[1]):
                    for position in positions:
                        if position[0] == 0 or position[1] == 0:
                            if area_with_weight[end_point[0]][end_point[1]] - 1 == area_with_weight[end_point[0] + position[0]][end_point[1] + position[1]]:
                                robot_path.insert(0, (end_point[0] + position[0],end_point[1] + position[1]))
                                end_point = (end_point[0] + position[0], end_point[1] + position[1])
                                break

                        else:
                            if area_with_weight[end_point[0]][end_point[1]] - 1.50 == area_with_weight[end_point[0] + position[0]][end_point[1] + position[1]]:
                                robot_path.insert(0, (end_point[0] + position[0],end_point[1] + position[1]))
                                end_point = (end_point[0] + position[0], end_point[1] + position[1])
                                break

                    self.area[end_point[0]][end_point[1]] = "+"

                break
        return robot_path

    def print_area(self):
        start_point = self.robot.get_start_point()
        self.area[start_point[0]][start_point[1]] = "S"
        end_point = self.robot.get_end_point()
        self.area[end_point[0]][end_point[1]] = "G"
        for i in self.stops:
            self.area[i[0]][i[1]] = "P"
        for i in range(self.width - 1, -1, -1):
            for j in range(self.leng):
                print(self.area[i][j], end=" ")
            print()


if __name__ == '__main__':
    world = World()
    world.read_input()
    for i in world.polygans:
        world.drawing_polygan(i)

<<<<<<< HEAD
# world.greedy_search()
path=world.dijkstra_search()
world.print_area()

motchieu=rvto1d(path)
oldpath=[2,2,3,3,4,3,5,3,6,3,7,3,8,3,9,4,10,5,10,6,10,7,11,8,12,9,13,10,14,11,15,12,16,13,17,14,18,15,19,16]
plg1=[4,4,4,5,4,6,4,7,4,8,5,9,6,9,7,10,8,10,9,9,9,8,9,7,9,6,9,5,8,5,8,5,7,4,6,4,5,4,8,4]
plg2=[11,1,11,2,11,3,11,4,11,5,11,6,11,6,12,6,13,6,14,6,14,5,14,4,14,3,14,2,14,1,13,1,12,1]
plg3=[8,12,8,13,8,14,8,15,8,16,8,17,9,16,10,15,11,14,12,13,13,12,12,12,11,12,10,12,9,12,8,12]

width=22
height=18
ratio=30

win=GraphWin("robot_path",(width+1)*ratio,(height+1)*ratio)
drawGrid(width,height,win)
drawPath(oldpath,color_rgb(150,150,150),win,height)
drawPath(plg1,color_rgb(255,0,0),win,height)
drawPath(plg2,color_rgb(0,255,0),win,height)
drawPath(plg3,color_rgb(220,116,0),win,height)
drawPath(motchieu,color_rgb(100,100,100),win,height)
drawText(2,2,height,win,"S",20)
drawText(19,16,height,win,"G",20)
win.getMouse()
win.close()
=======
    world.greedy_search()
    # world.dijkstra_search()
    world.print_area()
>>>>>>> 9da5c1a7cfc7993619e9ef01b99160fd9812430d
