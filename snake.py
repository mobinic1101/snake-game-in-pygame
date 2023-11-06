import pygame
import random
pygame.init()

class GameInformation:
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    GRAY = 128,128,128
    GREEN = 0,255,40
    RED = 255,0,0
    BACKGROUND_COLOR = BLACK
    HEAD_COLOR = 0,255,40

    BIG_FONT = pygame.font.SysFont("arial", 70)
    FONT = pygame.font.SysFont("comicsans", 40)

    def __init__(self, real_width=600, hight=600):
        self.real_width = real_width
        self.width = real_width - (real_width - hight)
        self.hight = hight
        self.snake_width = (self.width // 50)
        self.snake_hight = self.snake_width
        self.center = self.width // 2, hight // 2
        self.snake_step = 15
        self.SNAKE_VEL = 3
        self.snake_head = pygame.Rect(
            self.width // 2, self.hight // 2, self.snake_width, self.snake_hight) 
        self.set_bodies()
        self.food = pygame.Rect(
            random.randrange(0, self.width - self.snake_width, self.snake_step), random.randrange(0, self.hight - self.snake_hight, self.snake_step),
            self.snake_width, self.snake_hight) # food
        self.screen = pygame.display.set_mode(B)
        pygame.display.set_caption('Crazy Snake')

    def update_food(self):
        x, y = random.randrange(
            0, self.width - self.snake_width, self.snake_step), random.randrange(0, self.hight - self.snake_hight, self.snake_step
            )
        self.food.x, self.food.y = x, y

    def reset_snake(self):
        self.snake_head.x, self.snake_head.y = self.center[0], self.center[1]

    def set_bodies(self):
        self.snake_bodies = []


def draw(game_info, direction, score, eat_food=False):
    screen = game_info.screen
    snake_vel = game_info.SNAKE_VEL
    bodies = game_info.snake_bodies
    head = game_info.snake_head
    new_body = pygame.Rect(0, 0, game_info.snake_width, game_info.snake_hight) # result of eating food

    screen.fill(game_info.BACKGROUND_COLOR)

    if direction == 'up':
        head.y -= game_info.snake_step
    elif direction == 'down':
        head.y += game_info.snake_step
    elif direction == 'left':
        head.x -= game_info.snake_step
    elif direction == 'right':
        head.x += game_info.snake_step
    if eat_food:
        bodies.insert(0, new_body)
    # adjusting bodies
    bodies.append(head)
    for i in range(len(bodies) - 1):
        bodies[i].x, bodies[i].y = bodies[i+1].x, bodies[i+1].y
    # drawing score food and body
    screen.blit(game_info.FONT.render(f"score: {str(score)}", True, game_info.WHITE), (10, 10))
    pygame.draw.rect(screen, game_info.WHITE, game_info.food)
    for body in bodies:
        pygame.draw.rect(screen, game_info.GREEN, body)
    pygame.display.update()


def check_collision(game_info, directions):
    head = game_info.snake_head
    bodies = game_info.snake_bodies
    food = game_info.food
    width, hight = game_info.real_width, game_info.hight

    collisions = {'wall':False, 'body':False, 'food':False}
    collisions['wall'] = True if not head.x < width or head.x < 0 or not head.y < hight or head.y < 0 else False
    collisions['food'] = True if head.x == food.x and head.y == food.y else False
    # for i in range(len(bodies) - 2):
    #     if head.x == bodies[i].x and head.y == bodies[i].y:
    #         collisions['body'] = True
    return collisions
            

def main():
    FPS = 5
    GAME_OVER = 'YOU DEAD!'
    clock = pygame.time.Clock()

    game_info = GameInformation()

    direction = 'right'
    change_to = direction

    mini_step = 0
    score = 0
    update_body = False
    game_running = True
    while game_running:
        clock.tick(int(FPS))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                break
            elif event.type != pygame.KEYDOWN:
                continue
            elif event.key == pygame.K_UP:
                change_to = 'up'
            elif event.key == pygame.K_DOWN:
                change_to = 'down'
            elif event.key == pygame.K_LEFT:
                change_to = 'left'
            elif event.key == pygame.K_RIGHT:
                change_to = 'right'
        # if mini_step == game_info.snake_step:
        direction = (change_to if change_to == 'up' and direction != 'down' or
        change_to == 'down' and direction != 'up' or
        change_to == 'left' and direction != 'right' or
        change_to == 'right' and direction != 'left' else direction)
        mini_step = 0

        draw(game_info, direction, score, eat_food=update_body)
        mini_step += game_info.SNAKE_VEL

        update_body = False
        collisions = check_collision(game_info, direction)
        if collisions["wall"] or collisions['body']:
            game_over_screen = True
            game_over_text = game_info.BIG_FONT.render(GAME_OVER, True, game_info.RED)
            score_text =  game_info.FONT.render(f"your score: {score}", True, game_info.WHITE)
            any_key = game_info.FONT.render('wanna play again? y/n', True, game_info.WHITE)
            while game_over_screen:
                game_info.screen.fill(game_info.BACKGROUND_COLOR)
                game_info.screen.blit(
                    game_over_text, (((game_info.center[0] + (game_info.real_width - game_info.hight) / 2)) - game_over_text.get_width() // 2, game_info.center[1] - game_over_text.get_height()))
                game_info.screen.blit(
                    score_text, (((game_info.center[0] + (game_info.real_width - game_info.hight) / 2)) - score_text.get_width() // 2, game_info.center[1] + game_over_text.get_height() + 10))
                game_info.screen.blit(
                    any_key, (((game_info.center[0] + (game_info.real_width - game_info.hight) / 2)) - any_key.get_width() // 2, game_info.center[1] + game_over_text.get_height() + score_text.get_height() + 10))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over_screen = False
                        game_running = False
                        break
                    if event.type != pygame.KEYDOWN:
                        continue
                    if event.key == pygame.K_y:
                        game_info.reset_snake()
                        game_info.set_bodies()
                        game_info.update_food()
                        FPS = 5
                        score = 0
                        game_over_screen = False
                        break
                    elif event.key == pygame.K_n:
                        game_over_screen = False
                        game_running = False
                        break
                pygame.display.update()
        elif collisions["food"]:
            score += 1
            FPS += 0.5
            game_info.update_food()
            update_body = True

    pygame.quit()

if __name__ == "__main__":
    main()
