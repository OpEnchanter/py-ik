import pygame, sys, math

window = pygame.display.set_mode((480, 480))
pygame.display.set_caption("Pygame Inverse Kinematics")

def calculateVector(p1, p2) -> tuple:
    return (p2[0] - p1[0], p2[1] - p1[1])

def calculateDist(p1, p2) -> float:
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def magnitude(vec) -> float:
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)

def vecToAngle(vec) -> float:
    return math.atan2(vec[1], vec[0])

def calculateVertex(p1, p2, l1, l2) -> tuple:
    midPoint = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    p1ToMidPoint = calculateDist(p1, midPoint)

    p1ToMid = calculateVector(p1, midPoint)
    if magnitude(p1ToMid) < 1:
        p1ToMid = (1, 1)
    p1ToMid = (p1ToMid[0] / magnitude(p1ToMid), p1ToMid[1] / magnitude(p1ToMid))

    newDist = p1ToMidPoint * l1 / l2

    if newDist > l1:
        newDist = l1

    vertexBase = (p1[0] + p1ToMid[0] * newDist, p1[1] + p1ToMid[1] * newDist)

    vertexBaseToP1 = calculateVector(vertexBase, p1)
    vertexBaseToP2 = calculateVector(vertexBase, p2)

    vertexAngle = (vecToAngle(vertexBaseToP1) + vecToAngle(vertexBaseToP2)) / 2

    vertexDist = math.sqrt(abs(l1**2 - newDist ** 2))

    vertex = (vertexBase[0] + math.cos(vertexAngle) * vertexDist, vertexBase[1] + math.sin(vertexAngle) * vertexDist)

    return vertex

def solveIk(p1, p2, l1, l2) -> tuple:
    endPoint = p2

    if calculateDist(endPoint, p1) > l1 + l2:
        vec = calculateVector(p1, endPoint)
        vec = (vec[0] / magnitude(vec), vec[1] / magnitude(vec))

        endPoint = (p1[0] + vec[0] * (l1 + l2), p1[1] + vec[1] * (l1 + l2))

    vertex = calculateVertex(p1, p2, l1, l2)


    drawEnd = calculateVector(vertex, endPoint)

    drawEnd = (drawEnd[0] / magnitude(drawEnd), drawEnd[1] / magnitude(drawEnd))

    drawEnd = (vertex[0] + drawEnd[0] * l2, vertex[1] + drawEnd[1] * l2)

    pygame.draw.line(window, (0,0,0), p1, vertex, 5)
    pygame.draw.line(window, (0,0,0), vertex, drawEnd, 5)

    pygame.draw.circle(window, (255, 0, 0), vertex, 5)
    pygame.draw.circle(window, (0, 255, 0), p1, 5)
    pygame.draw.circle(window, (0, 0, 255), drawEnd, 5)

    return drawEnd

length1 = 100
length2 = 100

target = pygame.mouse.get_pos()
base = (240, 240)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill((255, 255, 255))
    
    target = (target[0] + calculateVector(target, pygame.mouse.get_pos())[0] / 1, target[1] + calculateVector(target, pygame.mouse.get_pos())[1] / 1)
    
    if pygame.key.get_pressed()[pygame.K_w]:
        base = (base[0], base[1] - 0.1)
    if pygame.key.get_pressed()[pygame.K_s]:
        base = (base[0], base[1] + 0.1)

    if pygame.key.get_pressed()[pygame.K_a]:
        base = (base[0] - 0.1, base[1])
    if pygame.key.get_pressed()[pygame.K_d]:
        base = (base[0] + 0.1, base[1])

    firstEnd = solveIk(base, target, 50, 50)


    pygame.display.flip()