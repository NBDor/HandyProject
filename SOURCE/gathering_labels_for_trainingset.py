import sys
import os
import pygame
import cv2
import matplotlib.pyplot as plt

x = 0
y = 400
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

pygame.init()

clk = pygame.time.Clock()

if pygame.joystick.get_count() == 0:
    raise IOError("No joystick detected")
joy = pygame.joystick.Joystick(0)
joy.init()

size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Joystick Tester")

frameRect = pygame.Rect((45, 45), (510, 510))

crosshair = pygame.surface.Surface((10, 10))
crosshair.fill(pygame.Color("magenta"))
pygame.draw.circle(crosshair, pygame.Color("blue"), (5, 5), 5, 0)
crosshair.set_colorkey(pygame.Color("magenta"), pygame.RLEACCEL)
crosshair = crosshair.convert()

writer = pygame.font.Font(pygame.font.get_default_font(), 15)
buttons = {}
for b in range(joy.get_numbuttons()):
    buttons[b] = [
        writer.render(
            hex(b)[2:].upper(),
            1,
            pygame.Color("red"),
            pygame.Color("black")
        ).convert(),
        ((15 * b) + 45, 560)
    ]

cap = cv2.VideoCapture(1)
count = 1
while True:
    ret, frame = cap.read()
    pygame.event.pump()
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    screen.fill(pygame.Color("black"))

    x = joy.get_axis(0)
    y = joy.get_axis(1)

    screen.blit(crosshair, ((x * 250) + 300 - 5, (y * 250) + 300 - 5))
    pygame.draw.rect(screen, pygame.Color("red"), frameRect, 1)

    plt.imsave(f'C:/Users/Nir Ben Dor/Documents/Afeka/Convert/colors/test_Color_frame#{count}({x},{y}).png', img)
    for b in range(joy.get_numbuttons()):
        if joy.get_button(b):
            screen.blit(buttons[b][0], buttons[b][1])

    pygame.display.flip()
    count += 1
    clk.tick(30)  # Limit to <=30 FPS

cap.release()
cv2.destroyAllWindows()


