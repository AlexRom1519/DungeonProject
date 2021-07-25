from GameObjects import *
from settings import *
vec = pygame.math.Vector2

class player(Creature):
    def __init__(self, position, textureSize, textureNames, textureParams, health):
        super().__init__(position, textureSize, textureNames, textureParams, health)
        self.jumping = False
        self.onGround = False

        self.deathScore = KNIGHT_DEATH_SCORE
        self.hitTimer = KNIGHT_HIT_TIMER
        self.attackDelay = KNIGHT_ATTACK_DELAY

        self._layer = 2

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -SHORT_JUMP:
                self.vel.y = -SHORT_JUMP

    def jump(self):
        # jump only if standing on a platform
        if self.onGround:
            self.jumping = True
            self.onGround = False
            self.vel.y = -PLAYER_JUMP

    def update(self):

        self.move()
        self.animate()

    def simple_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.left = True
            self.right = False
            self.standing = False
            self.vel.x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT]:
            self.left = False
            self.right = True
            self.standing = False
            self.vel.x = PLAYER_SPEED
        else:
            self.standing = True
            self.vel.x = 0


        if not self.onGround:
            self.vel.y += PLAYER_GRAV

        #self.pos += self.vel


        self.x = self.pos.x
        self.y = self.pos.y
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    # equations of motion
    def move(self):

        if not self.onGround:
            self.acc = vec(0, PLAYER_GRAV)
        else:
            self.acc = vec(0, 0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.left = True
            self.right = False
            self.standing = False
            self.acc.x = -PLAYER_ACC
        elif keys[pygame.K_RIGHT]:
            self.left = False
            self.right = True
            self.standing = False
            self.acc.x = PLAYER_ACC
        else:
            self.standing = True

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION


        self.vel += self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        #self.pos += self.vel + 0.5 * self.acc


    def hit(self, win):
        self.jumping = False
        self.vel.y = 0
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render(str(self.deathScore), 1, (255,0,0))
        win.blit(text, ((WIDTH_RESOLUTION/2) - round(text.get_width()/2), HEIGHT_RESOLUTION/2))
        pygame.display.update()
        i = 0
        while i < self.hitTimer:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = self.hitTimer + 1
                    pygame.quit()
