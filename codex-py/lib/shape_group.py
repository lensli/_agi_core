import time,random
class Ponit:
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.color = color
        self.life_time = random.randint(0,100)/100
        self.life_start_time = time.time()

def ponits_update(all_point,mouse_pose):
    while len(all_point) < 1000:
        point_x = mouse_pose[0] + random.randint(-50,50)
        point_y = mouse_pose[1] + random.randint(-50,50)
        point_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
         
        all_point.append(Ponit(point_x,point_y,point_color))
    for p in all_point:
        if time.time() - p.life_start_time > p.life_time:
            all_point.remove(p)
        p.x = mouse_pose[0] - p.x - 1
        p.y = mouse_pose[1] - p.y - 1
            
    return all_point