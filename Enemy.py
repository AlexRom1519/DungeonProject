from GameObjects import *
from settings import *
from levels import TILE_SIZE

class enemy(Creature):
    def __init__(self, position, textureSize, textureNames, textureParams, health):
        super().__init__(position[0], textureSize, textureNames, textureParams, health)
        self.path = [position[0][0], position[1][0]]
        self.direction = 'right'

    def update(self):
        self.new_move()

        self.animate()

#change position and moving direction if need
    def move(self):
        if self.velocity > 0:
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.walkCount = 0
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.walkCount = 0

    def new_move(self):
        #self.acc = vec(0, 0)
        # check for reverse movement
        if self.pos.x > self.path[1]:
            self.left = True
            self.right = False
            self.standing = False
            self.direction = 'left'
        if self.pos.x <= self.path[0]:
            self.left = False
            self.right = True
            self.standing = False
            self.direction = 'right'

        if self.direction == 'right':
            self.acc.x = ENEMY_ACC
        else:
            self.acc.x = -ENEMY_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equations of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        self.x = self.pos.x
        self.y = self.pos.y
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
