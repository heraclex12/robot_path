from CSTTNT.robot_path.robot import Robot
import copy

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
        with open("input.txt", "r") as file:
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
            p1, p2, p3, p4 = [int(i) for i in line.split(",")]
            self.robot = Robot(p2, p1, p4, p3)
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

            line = file.readline().strip("\s\n\r\t")
            if line is not None and line != "":
                tmp = [int(i) for i in line.split(",")]
                for j in range(0, len(tmp), 2):
                    self.area[tmp[j + 1]][tmp[j]] = "P"
                    self.stops.append((tmp[j + 1], tmp[j]))


    def eucliean_distance(self, x1, y1, x2, y2):
        return (((x2 - x1) ** 2) + ((y2 - y1) ** 2)) ** 0.5


    def drawing_polygan(self, polygan : list):
        def match_two_point(point_a : tuple, point_b : tuple):
            if point_a[0] == point_b[0]:
                for match in range(0, abs(point_a[1] - point_b[1]) + 1):
                    if point_b[1] > point_a[1]:
                        self.area[point_a[0]][point_a[1] + match] = "#"

                    else:
                        self.area[point_a[0]][point_b[1] + match] = "#"

            elif point_a[1] == point_b[1]:
                for match in range(0, abs(point_a[0] - point_b[0]) + 1):
                    if point_b[0] > point_a[0]:
                        self.area[point_a[0] + match][point_a[1]] = "#"

                    else:
                        self.area[point_b[0] + match][point_b[1]] = "#"

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

        self.area[polygan[0][0]][polygan[0][1]] = "#"
        for index in range(1, len(polygan)):
            curr = polygan[index]
            prev = polygan[index - 1]
            match_two_point(prev, curr)

        match_two_point(polygan[0], polygan[len(polygan) - 1])


    def greedy_search(self) -> list:
        robot_path = []
        positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
        start_point = self.robot.get_start_point()
        passing_points = []
        passing_points.extend(self.stops)
        passing_points.append(self.robot.get_end_point())
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
                self.area[x_next][y_next] = "+"

                start_point = end_point

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
            curr_point = queue_points.pop()
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
        for i in range(self.width - 1, -1, -1):
            for j in range(self.leng):
                print(self.area[i][j], end=" ")
            print()


world = World()
world.read_input()
for i in world.polygans:
    world.drawing_polygan(i)

# world.greedy_search()
world.dijkstra_search()
world.print_area()
