# game options/settings
TITLE = "Path away: Dungeon"
WIDTH_RESOLUTION = 800
HEIGHT_RESOLUTION = 800
FPS = 60
ANIMATION_DELAY = 100
FONT_NAME = 'arrial'

#Music
MAIN_GAME_MUSIC = 'Happy Tune.ogg'
START_SCREEN_MUSIC = 'Yippee.ogg'
GAME_OVER_MUSIC = 'Yippee.ogg'
MUSIC_FADEOUT = 500

#Images
PLATFORM_IMAGE = "Resources/Platform.png"
BACKGROUND_IMAGE = 'Resources/BackGround.png'
EXIT_IMAGE = "Resources/Exit.png"

#KNIGHT PROPERTIES
KNIGHT_START_POS = (200, HEIGHT_RESOLUTION - 200 )
KNIGHT_TEXTURE_SIZE = (64, 64)
KNIGHT_VELOCITY = 0
KNIGHT_TEXTURES_NAMES = ('Resources/Hero/walk/BlueKnight_entity_000_walk_00{}_r.png',
                         'Resources/Hero/BlueKnight_entity_000_Idle_000.png')

KNIGHT_TEXTURE_SCALE = (64,64)
KNIGHT_ANIMATION_DELAY = 100
KNIGHT_NUM_TEXTURE_WALK = 9
KNIGHT_HEALTH = 100
KNIGHT_HITBOX_PARAM = (20, 0, 28, 60)

KNIGHT_DEATH_SCORE = -5
KNIGHT_HIT_TIMER = 300
KNIGHT_ATTACK_DELAY = 5

#movement properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.10
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20
SHORT_JUMP = 12
PLAYER_SPEED = 3

ENEMY_ACC = 0.1

#ENEMY PROPERTIES
ENEMY_START_POS = (720, 800)
ENEMY_TEXTURE_SIZE = (80, 80)
ENEMY_VELOCITY = 5
ENEMY_TEXTURES_NAMES = ('Resources/Enemies/Minotaur_01/PNG Sequences/Walking/Minotaur_01_Walking_00{}.png',
                        'Resources/Enemies/Minotaur_01/PNG Sequences/Walking/Minotaur_01_Walking_000.png')
ENEMY_TEXTURE_SCALE = (80,80)
ENEMY_ANIMATION_DELAY = 100
ENEMY_NUM_TEXTURE_WALK = 9
ENEMY_HEALTH = 10
ENEMY_HITBOX_PARAM = (14, 0, 21, 53)

#knife PROPERTIES
KNIFE_TEXTURE_SIZE = (32, 32)
KNIFE_TEXTURES_NAMES = ('Resources/axe/spinning_axe_gif-{}.png',
                        'Resources/axe/spinning_axe_gif-0.png')
KNIFE_TEXTURE_SCALE = (32, 32)
KNIFE_NUM_TEXTURE_WALK = 7
KNIFE_ANIMATION_DELAY = 100


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
