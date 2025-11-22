
class 交互基类:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.z = 0

        self.edge_w = 0
        self.edge_l = 0
        self.edge_h = 0

    def pygame_rander(self):
        pass
    def move(x,y,z):
        self.x += x
        self.y += y
        self.z += z

class Robot(交互基类):
    def __init__(self, name, color, x, y, z, yaw):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
class 圆柱体(交互基类):
    def __init__(self, name, color, x, y, z, yaw):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw