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

    if p1[1] >= p2[1]:
        vertexAngle = math.radians(math.degrees(vertexAngle) + 180)

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

    pygame.draw.line(window, (55,55,55), p1, vertex, 10)
    pygame.draw.line(window, (55,55,55), vertex, drawEnd, 10)

    pygame.draw.circle(window, (45, 45, 45), vertex, 7.5)
    pygame.draw.circle(window, (45, 45, 45), p1, 7.5)
    pygame.draw.circle(window, (45, 45, 45), drawEnd, 7.5)

    return drawEnd

length1 = 100
length2 = 100

target = (320, 200)
base = (240, 240)

ikTarget = (320, 240)

targetIndicator = target

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill((15, 15, 15))

    if ikTarget[0] >= 319:
        target = (240, 200)
    if ikTarget[0] <= 241:
        target = (320, 240)

    tvec = calculateVector(ikTarget, target)
    ikTarget = (ikTarget[0] + tvec[0] / 3000, ikTarget[1] + tvec[1] / 3000)

    pygame.draw.rect(window, (10, 10, 10), (0, 240, 480, 240))

    solveIk(base, ikTarget, 50, 50)

    tvec = calculateVector(targetIndicator, target)
    targetIndicator = (targetIndicator[0] + tvec[0] / 1000, targetIndicator[1] + tvec[1] / 1000)

    pygame.draw.circle(window, (255, 0, 0), targetIndicator, 4)


    pygame.display.flip()