#!/usr/bin/python
# vim: set fileencoding=utf-8

from battleship.pygame_engine import *
from battleship.pygame_controller import *


fonts_dir = 'fonts'
font_name = 'neo_retro.ttf'
font_path = os.path.join(fonts_dir, font_name)
menu_back_c = (212, 227, 230)
menu_back_selected_c = (116, 213, 218)
menu_font_c = (0, 0, 0)
menu_font_selected_c = (0, 0, 0)


class TestMenuElementFlat(pygame.sprite.Sprite):
    
    font = pygame.font.Font(font_path, 40)
    width = 315
    height = 60
    padding_left = 30
    padding_top = 5
    
    def __init__(self, text):
        pygame.sprite.Sprite.__init__(self)
        
        self.is_chosen = False
        
        self.text = text
        self.txt = self.font.render(text ,True, menu_font_c)
        
        self._draw()
        self.rect = self.image.get_rect()

    def _draw(self):
        self.image = pygame.Surface((self.width, self.height))
        if self.is_chosen:
            self.image.fill(menu_back_selected_c)
            self.image.blit(self.txt, [self.padding_left, self.padding_top])
        else:
            self.image.fill(menu_back_c)
            self.image.blit(self.txt, [self.padding_left, self.padding_top])

    def update(self):
        self._draw()


class TestMenuController(Controller):
    def input(self, events):
        Controller.input(self, events)
        scene = self.engine.world
        
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    scene.select('left')
                    
                elif e.key == pygame.K_RIGHT:
                    scene.select('right')

            
class MenuFlat(pygame.sprite.LayeredUpdates):
    
    selection = 0
    
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)
        self.items = ['item1', 'item2', 'item3']
        for i, a in enumerate(self.items):
            item = TestMenuElementFlat(a)
            if i == self.selection:
                item.is_chosen = True
            item.rect.y = item.height * i
            item.rect.x = 50
            self.add(item)

    def get_group(self):
        return self

    def select(self, trend):
        self.get_sprite(self.selection).is_chosen = False
        size = len(self.items)
        if trend == "left":
            self.selection = (self.selection - 1) % size
        elif trend == "right":
            self.selection = (self.selection + 1) % size
        print("change selection to", self.selection)
        self.get_sprite(self.selection).is_chosen = True


def main():
    engine = Engine()
    engine.name = 'Test Menu Flat'
    engine.swidth = 640
    engine.sheight = 480
    engine.back_color = (0,0,0)
    engine.start()
    
    menu = MenuFlat()
    menu.initialize = False
    menu.get_sprites = False
    test_menu_controller = TestMenuController(engine)
    engine.add_scene('battleship', menu, test_menu_controller)

    clock = pygame.time.Clock()
    while 1:
        engine.draw_scene()
        clock.tick(20)

if __name__ == '__main__': main()


