import pygame

pygame.init()

# Screen settings
WIDTH , HEIGHT = 1000 , 1000
SCREEN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption('Triangle rasterizer')

def cross (vect2_1 , vect2_2):
    return vect2_1[0] * vect2_2[1] - vect2_1[1] * vect2_2[0]

def is_top_left(vect2):

    #works for anticlockwise triangles
    if vect2[1] == 0 and vect2[0] > 0:
        return 0
    if vect2[1] < 0:
        return 0
    return -1


class vert2_t:
    def __init__(self,v1,v2,v3,color1,color2,color3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3

        self.x_min = min(self.v1[0] , self.v2[0] , self.v3[0])
        self.x_max = max(self.v1[0] , self.v2[0] , self.v3[0])
        self.y_min = min(self.v1[1] , self.v2[1] , self.v3[1])
        self.y_max = max(self.v1[1] , self.v2[1] , self.v3[1])
        



    def contain (self, point):   # bool
        # vectors (anti-clockwise)
        vect_v1_v2 = [self.v2[0] - self.v1[0] , self.v2[1] - self.v1[1]]
        vect_v2_v3 = [self.v3[0] - self.v2[0] , self.v3[1] - self.v2[1]]
        vect_v3_v1 = [self.v1[0] - self.v3[0] , self.v1[1] - self.v3[1]]

        vector_v1_point= [point[0] - self.v1[0], point[1] - self.v1[1]]
        vector_v2_point = [point[0] - self.v2[0], point[1] - self.v2[1]]
        vector_v3_point = [point[0] - self.v3[0], point[1] - self.v3[1]]

        bias1 = is_top_left(vect_v1_v2)
        bias2 = is_top_left(vect_v2_v3)
        bias3 = is_top_left(vect_v3_v1)


        # interpolation
        tri_area_t_2 = cross(vect_v1_v2,vect_v2_v3)
        w1 = cross(vect_v2_v3,vector_v2_point)
        w2 = cross(vect_v3_v1,vector_v3_point)
        w3 = cross(vect_v1_v2,vector_v1_point)

        alpha = w1 / tri_area_t_2
        beta  = w2 / tri_area_t_2
        gamma = w3 / tri_area_t_2

        r = int(self.color1[0] * alpha + self.color2[0] * beta + self.color3[0] * gamma)
        g = int(self.color1[1] * alpha + self.color2[1] * beta + self.color3[1] * gamma)
        b = int(self.color1[2] * alpha + self.color2[2] * beta + self.color3[2] * gamma)

        # check if it is in the triangle
        if cross(vect_v1_v2 , vector_v1_point) + bias1 <= 0 and cross(vect_v2_v3 , vector_v2_point) + bias2 <= 0 and cross(vect_v3_v1 , vector_v3_point) +bias3 <= 0:
            return (r,g,b)
        return False
    






def main():
    clock = pygame.time.Clock()


    triangle1 = vert2_t(  [100,200],
                    [400,700],
                    [900,300],(255,0,0),(0,255,0),(0,0,255))

    # triangle2 = vert2_t(  [0,0],
    #                     [WIDTH,HEIGHT],
    #                     [WIDTH,0],(255,255,255),(0,0,0),(255,0,0))


    triangles = [triangle1]
        
    step = 0

    for triangle in triangles:
            for x in range(triangle.x_min , triangle.x_max):
                    for y in range(triangle.y_min , triangle.y_max):
                        step += 1
                        contain = triangle.contain((x,y))
                        if contain != False:
                            SCREEN.set_at((x,y),contain)
    pygame.display.update()
    print(step)

    running = True

    while running:
        clock.tick(60) # set time per frame

        SCREEN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                




main()
pygame.quit()