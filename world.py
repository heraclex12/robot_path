from CSTTNT.robot_path.robot import Robot

# Quy ước:
#            # : hình đa giác
#            0 : vị trí trống
#            + : lộ trình đường đi
#            S : vị trí bắt đầu
#            G : vị trí kết thúc
#            * : viền/khung/giới hạn/ranh giới

class World():
    def __init__(self):
        self.leng = 0
        self.width = 0
        self.amount_polygan = 0
        self.polygans = []
        self.area = []
        self.robot = Robot(0,0,0,0)

    def read_input(self):
        with open("input.txt", "r") as file:
            line = file.readline()
            self.leng, self.width = [int(i) + 1 for i in line.split(",")]
            for i in range(self.width):
                row = []
                for j in range(self.leng):
                    if j == 0 or i == 0 or j == self.leng - 1 or i == self.width - 1:
                        row.append("*")
                    else:
                        row.append(0)

                self.area.append(row)

            line = file.readline()
            p1, p2, p3, p4 = [int(i) for i in line.split(",")]
            self.robot = Robot(p2, p1, p4, p3)
            self.area[p2][p1] = "S"
            self.area[p4][p3] = "G"
            self.amount_polygan = int(file.readline())
            for i in range(self.amount_polygan):
                polygan = []
                line = file.readline()
                tmp = [int(i) for i in line.split(",")]
                for j in range(0, len(tmp), 2):
                    polygan.append((tmp[j + 1], tmp[j]))

                self.polygans.append(polygan)


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
            match_two_point(curr, prev)

        match_two_point(polygan[0], polygan[len(polygan) - 1])


    def a_star_search(self):
        positions = [(1, -1), (-1, 0), (-1, -1), (0, -1), (-1, 1), (1, 0), (0, 1), (1, 1)]
        start_point = self.robot.get_start_point()
        end_point = self.robot.get_end_point()
        x_next = start_point[0]
        y_next = start_point[1]
        while not (x_next == end_point[0] and y_next == end_point[1]):
            minimum = self.leng * self.width
            x_tmp = x_next
            y_tmp = y_next
            for position in positions:
                if 0 < x_next + position[0] < self.width and 0 < y_next + position[1] < self.leng:
                    if x_next + position[0] == end_point[0] and y_next + position[1] == end_point[1]:
                        x_tmp = end_point[0]
                        y_tmp = end_point[1]
                        break

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

                        if path_weight < minimum:
                            minimum = path_weight
                            x_tmp = x_next + position[0]
                            y_tmp = y_next + position[1]

            x_next = x_tmp
            y_next = y_tmp
            if self.area[x_next][y_next] != "G":
                self.area[x_next][y_next] = "+"

    def write_output(self):
        pass

    def print_area(self):
        for i in range(self.width - 1, -1, -1):
            for j in range(self.leng):
                print(self.area[i][j], end=" ")
            print()


world = World()
world.read_input()
for i in world.polygans:
    world.drawing_polygan(i)

world.a_star_search()
world.print_area()