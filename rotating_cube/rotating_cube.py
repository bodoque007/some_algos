import numpy as np
import math
import pygame

points = []
for x in (-1, 1):
    for y in (-1, 1):
        for z in (-1, 1):
            points.append(np.array([[x], [y], [z]]))

currentAngle = 0

projectionMatrix3dTo2d = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])

## Simple pygame window

pygame.init()
width, height = 800, 800
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

while True:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    rotationMatrixZ = np.matrix([
        [math.cos(currentAngle), -math.sin(currentAngle), 0],
        [math.sin(currentAngle), math.cos(currentAngle), 0],
        [0, 0, 1]
    ])
    rotationMatrixX = np.matrix([
        [1, 0, 0],
        [0, math.cos(currentAngle), -math.sin(currentAngle)],
        [0, math.sin(currentAngle), math.cos(currentAngle)]
    ])
    rotationMatrixY = np.matrix([
        [math.cos(currentAngle), 0, math.sin(currentAngle)],
        [0, 1, 0],
        [-math.sin(currentAngle), 0, math.cos(currentAngle)]
    ])

    rotated_points = []
    for point in points:
        rotatedInY = rotationMatrixY @ point
        rotatedInX = rotationMatrixX @ rotatedInY
        rotatedInZ = rotationMatrixZ @ rotatedInX
        rotated_points.append(rotatedInZ)


    for i in range(1, len(rotated_points)):
        for j in range(i):
            projectedTo2d1 = projectionMatrix3dTo2d * rotated_points[i]
            x1 = int(projectedTo2d1[0, 0] * 100 + width / 2)
            y1 = int(projectedTo2d1[1, 0] * 100 + height / 2)

            projectedTo2d2 = projectionMatrix3dTo2d * rotated_points[j]
            x2 = int(projectedTo2d2[0, 0] * 100 + width / 2)
            y2 = int(projectedTo2d2[1, 0] * 100 + height / 2)
            pygame.draw.line(screen, BLUE, (x1, y1), (x2, y2), 2)
    currentAngle += 0.01
    pygame.display.update()
    clock.tick(60)
