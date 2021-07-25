from GameClass import Game
import pygame

if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        if g.level_complete:
            g.show_win_screen()
        else:
            g.show_go_screen()

    pygame.quit()
