import pygame

start = 0
num_of_images = 10
source_name = "Resources/hero/left/BlueKnight_entity_000_walk_00{counter}.png"
res_name = "Resources/hero/right/BlueKnight_entity_000_walk_00{counter}.png"


for i in range(start, num_of_images):
    first_name = source_name.format(counter=i)
    second_name = res_name.format(counter=i)
    image = pygame.image.load(first_name)
    image = pygame.transform.flip(image, True, False)
    pygame.image.save(image, second_name)
