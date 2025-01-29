import pygame
import sys
import math
from random import randint

pygame.init()

# Get size of screen
screen_width_height = pygame.display.Info()

# Define constants
SCREEN_WIDTH = screen_width_height.current_w 
SCREEN_HEIGHT = screen_width_height.current_h 

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boid simulation")

offscreen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
class Boid:
    def __init__(self, x, y):
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.position = [x,y]
        self.image = "Boid.png"
        self.image = pygame.transform.scale(pygame.image.load(self.image), (8, 8))

    def draw(self, surface):
        angle = math.atan2(self.velocity[1], self.velocity[0])
        image = pygame.transform.rotate(self.image, -math.degrees(angle))
        surface.blit(image, self.position)

    def separate(self, boids):
        ax = 0
        ay = 0
        count = 0
        x, y = pygame.mouse.get_pos()

        for other in boids:
            if other is self:
                continue
            if (self.position[0] - other.position[0])**2 + (self.position[1]- other.position[1])**2 < 15**2:
                ax += self.position[0] - other.position[0]
                ay += self.position[1] - other.position[1]
                count += 1
        if (self.position[0] - x)**2 + (self.position[1]- y)**2 < 50**2:
            ax += self.position[0] - x
            ay += self.position[1] - y



        if count > 0:
            ax /= count
            ay /= count

            norm_a = (ax**2 + ay**2)** 0.5

            if norm_a  > 0:
                ax /= norm_a
                ay /= norm_a

        self.acceleration = [ax * 1.2, ay * 1.2]

    def align(self, boids):
        x = 0
        y = 0
        count = 0

        for other in boids:
            if other is self:
                continue
            if (self.position[0] - other.position[0])**2 + (self.position[1]- other.position[1])**2 < 50**2:
                x += other.velocity[0]
                y += other.velocity[1]
                count += 1

        if count > 0:
            x /= count 
            y /= count

            dx = x - self.velocity[0]
            dy = y - self.velocity[1]

            mag = (dx**2 + dy**2) ** 0.5

            if mag > 0:
                dx /= mag
                dy /= mag

            self.acceleration[0] += dx * 0.2
            self.acceleration[1] += dy * 0.2

    def cohesion(self, boids):
        x = 0
        y = 0
        count = 0
        for other in boids:
            if other is self:
                continue
            if (self.position[0] - other.position[0])**2 + (self.position[1]- other.position[1])**2 < 200**2:
                x += other.position[0]
                y += other.position[1]
                count += 1

        if count > 0:
            x /= count
            y /= count

            dx = x - self.position[0]
            dy = y - self.position[1]

            mag = (dx**2 + dy**2) ** 0.5

            if mag > 0:
                dx /= mag
                dy /= mag

            self.acceleration[0] += dx * 0.07
            self.acceleration[1] += dy * 0.07


    def recalc(self):
        # Repel away from edge of screen, needs to be ran first so acceleration can be changed
        if self.position[0] < 50:
            self.acceleration[0] += 0.2
        elif self.position[0] > SCREEN_WIDTH - 50:
            self.acceleration[0] -= 0.2

        if self.position[1] < 50:
            self.acceleration[1] += 0.2
        elif self.position[1] > SCREEN_HEIGHT - 50:
            self.acceleration[1] -= 0.2

        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]


        max_speed = 7
        speed = (self.velocity[0]**2 + self.velocity[1]**2)**0.5
        if speed > max_speed:
            self.velocity[0] = (self.velocity[0]/speed) * max_speed
            self.velocity[1] = (self.velocity[1]/speed) * max_speed

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]


        self.acceleration[0] *= 0.02
        self.acceleration[1] *= 0.02
        

def main():
    num_of_boids = 100 # Highest Boids possible at 30 FPS is 80
    boids = []

    for i in range(num_of_boids):
        boid = Boid(randint(0, SCREEN_WIDTH), randint(0,SCREEN_HEIGHT))
        boids.append(boid)
        boid.draw(offscreen)

    while True:
        offscreen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        for boid in boids:
            boid.separate(boids)
            boid.align(boids)
            boid.cohesion(boids)
            boid.recalc()
            boid.draw(offscreen)

        screen.blit(offscreen, (0,0))
        pygame.display.update()

        clock.tick(60)

if __name__ == "__main__":
    main()