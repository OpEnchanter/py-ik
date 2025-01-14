import pygame, sys, math

window = pygame.display.set_mode((480, 480))

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
    p1ToMid = (p1ToMid[0] / magnitude(p1ToMid), p1ToMid[1] / magnitude(p1ToMid))

    newDist = p1ToMidPoint * l1 / l2

    if newDist > l1:
        newDist = l1

    vertexBase = (p1[0] + p1ToMid[0] * newDist, p1[1] + p1ToMid[1] * newDist)

    pygame.draw.circle(window, (255, 0, 0), vertexBase, 5)

    vertexBaseToP1 = calculateVector(vertexBase, p1)
    vertexBaseToP2 = calculateVector(vertexBase, p2)

    vertexAngle = (vecToAngle(vertexBaseToP1) + vecToAngle(vertexBaseToP2)) / 2

    vertexDist = math.sqrt(abs(l1**2 - newDist ** 2))

    vertex = (vertexBase[0] + math.cos(vertexAngle) * vertexDist, vertexBase[1] + math.sin(vertexAngle) * vertexDist)

    return vertex

length1 = 30
length2 = 50

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill((255, 255, 255))
    
    endPoint = pygame.mouse.get_pos()

    if calculateDist(endPoint, (240, 240)) > length1 + length2:
        vec = calculateVector((240, 240), endPoint)
        vec = (vec[0] / magnitude(vec), vec[1] / magnitude(vec))

        endPoint = (240 + vec[0] * (length1 + length2), 240 + vec[1] * (length1 + length2))

    vertex = calculateVertex((240, 240), pygame.mouse.get_pos(), length1, length2)


    drawEnd = calculateVector(vertex, endPoint)
    f = length2 / length1

    totalDist = magnitude(drawEnd) * f

    print(magnitude(drawEnd))

    drawEnd = (drawEnd[0] / magnitude(drawEnd), drawEnd[1] / magnitude(drawEnd))

    drawEnd = (240 + drawEnd[0] * totalDist, 240 + drawEnd[1] * totalDist)

    pygame.draw.circle(window, (255, 0, 0), vertex, 5)
    pygame.draw.circle(window, (255, 0, 0), (240, 240), 5)
    pygame.draw.circle(window, (255, 0, 0), endPoint, 5)

    pygame.draw.line(window, (0,0,0), (240, 240), vertex, 5)
    pygame.draw.line(window, (0,0,0), vertex, drawEnd, 5)

    pygame.display.flip()
