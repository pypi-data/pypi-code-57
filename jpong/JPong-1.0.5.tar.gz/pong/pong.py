#!/usr/bin/env python3

import pygame
import argparse

pygame.init()


DIMENSIONS = WIDTH, HEIGHT = 1200, 750
BG_COLOR = pygame.Color("black")


class Border:
    thickness = 15
    def __init__(self, surface, dimensions):
        width, height = dimensions
        self.walls = [
            Wall(surface, (0, 0, width, self.thickness)),
            Wall(surface, (0, 0, self.thickness, height)),
            Wall(surface, (0, height - self.thickness, width, self.thickness)),
            ]

    def draw(self):
        for wall in self.walls:
            wall.draw()


class Wall:
    def __init__(self, surface, rect, *, color=pygame.Color("gray")):
        self.surface = surface
        self.color = color
        self.rect = rect

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)


class Ball:
    radius = 15
    color = pygame.Color("gray")

    def __init__(self, surface, location, velocity):
        self.surface = surface
        self.x, self.y = location
        self.vel_x, self.vel_y = velocity
    
    def update(self):
        if self.x - self.radius <= Border.thickness:
            self.reverse_x()
        elif self.y - self.radius <= Border.thickness:
            self.reverse_y()
        elif self.y + self.radius >= HEIGHT - Border.thickness:
            self.reverse_y()
        elif self.x >= WIDTH:
            raise OutOfBoundsError

        self.x += self.vel_x
        self.y += self.vel_y
        self._draw()

    def reverse_x(self):
        self.vel_x = -self.vel_x

    def reverse_y(self):
        self.vel_y = -self.vel_y
    
    def _draw(self):
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius)


class Paddle:
    width = 20
    height = 140
    x = WIDTH - width
    color = pygame.Color("gray")

    def __init__(self, surface, location, velocity):
        """
        In this case, because the paddle has no motion in the x direction,
        location and velocity are integers, not tuples
        """
        self.surface = surface
        self.y = location
        self.vel_y = velocity

    def move_up(self):
        if self.y <= Border.thickness:
            pass
        else:
            self.y -= self.vel_y

    def move_down(self):
        if self.y + self.height >= HEIGHT - Border.thickness:
            pass
        else:
            self.y += self.vel_y
    
    def update(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))


class OutOfBoundsError(Exception):
    pass


def check_collisions(paddle, ball):
    if ball.x + Ball.radius > WIDTH - Paddle.width:
        if paddle.y < ball.y - Ball.radius < paddle.y + Paddle.height:
            ball.reverse_x()
            return True
        else:
            return False
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", "-m", default="medium", choices=["easy", "medium", "hard", "impossible"])
    args = parser.parse_args()

    mode = args.mode

    screen = pygame.display.set_mode(DIMENSIONS)
    screen.fill(BG_COLOR)
    border = Border(screen, DIMENSIONS)

    ball_location = (WIDTH - 4*Ball.radius, HEIGHT // 2)
    if mode == "easy":
        ball_velocity = (-10, -10)
    elif mode == "medium":
        ball_velocity = (-15, -15)
    elif mode == "hard":
        ball_velocity = (-20, -20)
    elif mode == "impossible":
        ball_velocity = (-25, -25)

    ball = Ball(screen, ball_location, ball_velocity)

    paddle_location = HEIGHT - Paddle.height
    paddle_velocity = 10
    paddle = Paddle(screen, paddle_location, paddle_velocity)

    clock = pygame.time.Clock()

    ACTIVE, PAUSE, GAMEOVER = 0, 1, 2
    state = ACTIVE

    score = 0

    pause_text = pygame.font.SysFont('Consolas', 23).render('Pause', True, pygame.Color("gray"))
    lose_text = pygame.font.SysFont('Consolas', 48).render('You lost! Press R to play again.', True, pygame.Color("gray"))


    # Create an event loop
    while True:
        e = pygame.event.poll()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            break
        elif keys[pygame.K_DOWN]:
            paddle.move_down()
        elif keys[pygame.K_UP]:
            paddle.move_up()
        elif keys[pygame.K_p]:
            state = PAUSE
        elif keys[pygame.K_r]:
            if state == GAMEOVER:
                ball.x, ball.y = (WIDTH - 4*Ball.radius, HEIGHT // 2)
                ball.reverse_x()
                paddle.y = HEIGHT - Paddle.height
                score = 0
                state = ACTIVE
            else:
                continue
        elif keys[pygame.K_s]:
            state = ACTIVE

        if e.type == pygame.QUIT:
            break
            
        clock.tick(40)

        if state == ACTIVE:
            screen.fill(BG_COLOR)

            if check_collisions(paddle, ball):
                score += 1

            score_text = pygame.font.SysFont("Consolas", 48).render(str(score), True, pygame.Color("gray"))
            screen.blit(score_text, (Border.thickness + 5, Border.thickness + 5))

            try:
                ball.update()
            except OutOfBoundsError:
                state = GAMEOVER
                screen.blit(lose_text, ((WIDTH // 2) - (lose_text.get_rect().width // 2), (HEIGHT // 2) - (lose_text.get_rect().height // 2)))

            paddle.update()
            border.draw()  # Redraw border to erase ball hits

        elif state == PAUSE:
            screen.blit(pause_text, ((WIDTH // 2) - (pause_text.get_rect().width // 2), (HEIGHT // 2) - (pause_text.get_rect().height // 2)))

        pygame.display.flip()

    exit()


if __name__ == "__main__":
    main()

