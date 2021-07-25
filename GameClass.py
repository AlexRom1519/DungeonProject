import pygame

from Player import *
from Enemy import *
from settings import *
from levels import *
from camera import *

from os import path
import copy

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH_RESOLUTION,HEIGHT_RESOLUTION))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)

        self.load_data()

    def load_data(self):
        #load Sound
        self.dir = path.dirname(__file__)
        self.snd_dir = path.join(self.dir, 'Resources/Music')
        self.jump_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'Jump5.wav'))

        self.bulletSound = pygame.mixer.Sound('Resources/Music/bullet.mp3')
        self.hitSound = pygame.mixer.Sound('Resources/Music/hit.mp3')
        self.music = pygame.mixer.music.load('Resources/Music/music.mp3')
        #pygame.mixer.music.play(-1)

        self.bg = pygame.image.load(BACKGROUND_IMAGE)
        self.bg = pygame.transform.scale(self.bg, (WIDTH_RESOLUTION, HEIGHT_RESOLUTION))

    #main draw cycle
    def draw(self):
        self.screen.blit(self.bg, (0,0))

        #apply camera to sprites
        for sprite in self.all_sprites:
            temp = copy.copy(sprite)
            temp = self.camera.apply(temp)
            self.screen.blit(sprite.image, temp)

        self.draw_text('Score: ' + str(self.score), 50, BLUE, 390, 10)

        pygame.display.update()

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.knifes = pygame.sprite.Group()

        self.load_level(FIRST_LEVEL)
        self.level_complete = False

        pygame.mixer.music.load(path.join(self.snd_dir, MAIN_GAME_MUSIC))
        self.run()

    def transform_pos(self, i):
        return [[i[0][0] * TILE_SIZE,i[0][1] * TILE_SIZE], [i[1][0] * TILE_SIZE,i[1][1] * TILE_SIZE]]


    def load_level(self, level):
        self.player = player(KNIGHT_START_POS, KNIGHT_TEXTURE_SIZE, KNIGHT_TEXTURES_NAMES, (KNIGHT_NUM_TEXTURE_WALK, KNIGHT_TEXTURE_SCALE, KNIGHT_ANIMATION_DELAY), KNIGHT_HEALTH)
        self.all_sprites.add(self.player)
        self.player_last_pos = self.player.pos
        for pos in ENEMY_POS:
            temp = enemy(self.transform_pos(pos), ENEMY_TEXTURE_SIZE, ENEMY_TEXTURES_NAMES, (ENEMY_NUM_TEXTURE_WALK, ENEMY_TEXTURE_SCALE, ENEMY_ANIMATION_DELAY), ENEMY_HEALTH)
            self.enemies.add(temp)
            self.all_sprites.add(temp)


        row_count = 0
        for row in level:
            col_count = 0
            for tile in row:
                if tile == 1 or tile == 2:
                    x = col_count * TILE_SIZE
                    y = row_count * TILE_SIZE
                    p = StaticTextureObject((x, y), (PLATFORM_WIDTH, PLATFORM_HEIGHT), PLATFORM_IMAGE, 1)
                    self.all_sprites.add(p)
                    self.platforms.add(p)
                if tile ==9:
                    x = col_count * TILE_SIZE
                    y = row_count * TILE_SIZE
                    p = StaticTextureObject((x, y), (PLATFORM_WIDTH, PLATFORM_HEIGHT), EXIT_IMAGE, 9)
                    self.all_sprites.add(p)
                    self.platforms.add(p)
                col_count += 1
            row_count += 1

        self.level_width  = col_count*PLATFORM_WIDTH
        self.level_height = row_count*PLATFORM_HEIGHT

        self.camera = Camera(camera_configure, self.level_width, self.level_height)



    def run(self):
        # Game Loop
        pygame.mixer.music.play(loops=-1) # loops=-1 - repeats indefinately
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(MUSIC_FADEOUT)

    def update(self):
        self.player.onGround = False
        self.all_sprites.update()

        self.camera.update(self.player)

        # collide with mobs
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask)
            if hits:
                self.playing = False
                #self.show_go_screen()

        # knife collides
        for knife in self.knifes:
            hits = pygame.sprite.spritecollide(knife, self.enemies, False)
            if hits:
                second_hits = pygame.sprite.spritecollide(knife, self.enemies, False, pygame.sprite.collide_mask)
                for enemy in second_hits:
                    enemy.kill()
                    knife.kill()
                    self.score += 1
                    pass
            hits = pygame.sprite.spritecollide(knife, self.platforms, False)
            if hits:
                knife.kill()
                pass
            if knife.rect.x < 0 or knife.rect.x > self.level_width:
                knife.kill()
                pass

        # linear move
        '''
        self.player.pos.y += self.player.vel.y
        self.player.rect.y = self.player.pos.y
        self.check_plat(0, self.player.vel.y)
        self.player.pos.x += self.player.vel.x
        self.player.rect.x = self.player.pos.x
        self.check_plat(self.player.vel.x, 0)
        '''

        # equation of movement
        self.player.pos.y += self.player.vel.y + 0.5 * self.player.acc.y
        self.player.rect.y = self.player.pos.y
        self.check_plat(0, self.player.vel.y)
        self.player.pos.x += self.player.vel.x + 0.5 * self.player.acc.x
        self.player.rect.x = self.player.pos.x
        self.check_plat(self.player.vel.x, 0)


    def check_plat(self, xvel, yvel):

        for p in self.platforms:
            if pygame.sprite.collide_rect(self.player, p):
                if p.type == 9:
                    self.playing = False
                    self.level_complete = True
                    return
                if xvel > 0:
                    self.player.rect.right = p.rect.left

                if xvel < 0:
                    self.player.rect.left = p.rect.right

                # check falling
                if yvel > 0:
                    self.player.vel.y = 0
                    self.player.rect.bottom = p.rect.top
                    self.player.jumping = False
                    self.player.onGround = True

                #check jumpnig
                if yvel < 0:
                    self.player.vel.y = 0
                    self.player.rect.top = p.rect.bottom


        self.player.pos.x = self.player.rect.x
        self.player.pos.y = self.player.rect.y
        self.player_last_pos = self.player.pos



    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                    if self.player.jumping:
                        self.jump_sound.play()
                if event.key == pygame.K_f:
                    if self.player.left:
                        facing = -1
                        position = self.player.rect.topleft
                    else:
                        facing = 1
                        position = self.player.rect.topright
                    temp = knife(position, KNIFE_TEXTURE_SIZE, KNIFE_TEXTURES_NAMES, (KNIFE_NUM_TEXTURE_WALK,KNIFE_TEXTURE_SCALE,KNIFE_ANIMATION_DELAY),facing)

                    self.knifes.add(temp)
                    self.all_sprites.add(temp)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump_cut()
                if event.key == pygame.K_q:
                    self.playing = False


    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def show_start_screen(self):
        # game splash/start screen
        pygame.mixer.music.load(path.join(self.snd_dir, START_SCREEN_MUSIC))
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH_RESOLUTION / 2, HEIGHT_RESOLUTION / 4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH_RESOLUTION / 2, HEIGHT_RESOLUTION / 2)
        self.draw_text("Press a key to play", 22, WHITE, WIDTH_RESOLUTION / 2, HEIGHT_RESOLUTION * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(MUSIC_FADEOUT)

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        pygame.mixer.music.load(path.join(self.snd_dir, GAME_OVER_MUSIC))
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH_RESOLUTION / 2, HEIGHT_RESOLUTION / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH_RESOLUTION / 2, HEIGHT_RESOLUTION / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH_RESOLUTION / 2, HEIGHT_RESOLUTION * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(MUSIC_FADEOUT)

    def show_win_screen(self):
        # game over/continue
        if not self.running:
            return
        pygame.mixer.music.load(path.join(self.snd_dir, GAME_OVER_MUSIC))
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("LEVEL COMPLETE !!!", 48, WHITE, WIDTH_RESOLUTION / 2, HEIGHT_RESOLUTION / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH_RESOLUTION / 2, HEIGHT_RESOLUTION / 2)
        self.draw_text("Press a key to play again", 22, WHITE, WIDTH_RESOLUTION / 2, HEIGHT_RESOLUTION * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(MUSIC_FADEOUT)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    waiting = False
