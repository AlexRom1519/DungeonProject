import pygame
from settings import *
vec = pygame.math.Vector2

class GameObject(object):
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]

class TextureObject(GameObject, pygame.sprite.Sprite):
    def __init__(self, position, textureSize):
        GameObject.__init__(self, position)
        pygame.sprite.Sprite.__init__(self)
        self.width = textureSize[0]
        self.height = textureSize[1]

        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class StaticTextureObject(TextureObject):
    def __init__(self, position, textureSize, textureName, type):
        super().__init__(position, textureSize)
        self.image = self.loadTexture(textureName, textureSize)
        self._layer = 1
        self.type = type

    def loadTexture(self, textureName, textureSize):
        temp = pygame.image.load(textureName)
        temp = pygame.transform.scale(temp, textureSize)
        return temp

#textureNames: (moveRight, idle)
#textureParams: (size, scale, animDelay)
#scale: (width, height)

class DynamicTextureObject(TextureObject):
    def __init__(self, position, textureSize, textureNames, textureParams):
        super().__init__(position, textureSize)

        #check for textures
        if textureNames[0]:
            self.moveRight = self.loadTexture(textureNames[0],textureParams)
            self.moveLeft = []
            for i in range(textureParams[0]):
                self.moveLeft.append(pygame.transform.flip(self.moveRight[i], True, False))
        else:
            self.moveRight = None
        if textureNames[1]:
            self.idle = self.loadTexture(textureNames[1],(1, textureParams[1]))
        else:
            self.idle = None

        self.numOfAnimPictures = textureParams[0]

        #for animation
        self.left = False
        self.right = False
        self.standing = True
        self.last_update = 0
        self.current_frame = 0
        self.animation_delay = textureParams[2]
        self.image = self.idle
        self.mask = pygame.mask.from_surface(self.image)

#if size == 1 -> load with same name
#else replace {}} in name to number
    def loadTexture(self, name, textureParams):
        if textureParams[0] == 1:
            temp = pygame.image.load(name)
            temp = pygame.transform.scale(temp, textureParams[1])
            return temp
        else:
            temp_list = []
            for i in range(textureParams[0]):
                temp_name = name.format(str(i+1))
                temp = pygame.image.load(temp_name)
                temp = pygame.transform.scale(temp, textureParams[1])
                temp_list.append(temp)
            return temp_list

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_delay:
            self.last_update = now
            if not(self.standing):
                if self.left:
                    self.current_frame = (self.current_frame + 1) % self.numOfAnimPictures
                    self.image = self.moveLeft[self.current_frame]
                elif self.right:
                    self.current_frame = (self.current_frame + 1) % self.numOfAnimPictures
                    self.image = self.moveRight[self.current_frame]
            else:
                if(self.right):
                    self.image = self.moveRight[0]
                else:
                    self.image = self.moveLeft[0]
        self.mask = pygame.mask.from_surface(self.image)

class Creature(DynamicTextureObject):
    def __init__(self, position, textureSize, textureNames, textureParams, health):
        super().__init__(position, textureSize, textureNames, textureParams)
        self.health = health
        self.pos = vec(self.x, self.y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

class knife(DynamicTextureObject):
    def __init__(self, position, textureSize, textureNames, textureParams, facing):
        super().__init__(position, textureSize, textureNames, textureParams)
        self.facing = facing
        self.vel = 2 * facing
        if facing == 1:
            self.standing = False
            self.right = True
            self.left = False
        else:
            self.standing = False
            self.right = False
            self.left = True

    def update(self):
        self.animate()
        self.rect.x += self.vel
