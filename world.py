from CSTTNT.robot_path.robot import Robot

# Quy ước:
#            # : hình đa giác
#            0 : vị trí trống
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
            # self.robot = Robot(p1, p2, p3, p4)
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
            

        self.area[polygan[0][0]][polygan[0][1]] = "#"
        for index in range(1, len(polygan)):
            curr = polygan[index]
            prev = polygan[index - 1]
            match_two_point(curr, prev)

        match_two_point(polygan[len(polygan) - 1], polygan[0])



    def write_output(self):
        pass

    def print_area(self):
        for i in range(self.width - 1, -1, -1):
            for j in range(self.leng):
                print(self.area[i][j], end=" ")
            print()


world = World()
world.read_input()
world.drawing_polygan(world.polygans[2])
world.print_area()