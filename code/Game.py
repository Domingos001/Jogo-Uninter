import pygame

#from code.Menu import Menu
class  Game:
    def __init__(self):
        pygame.init()
        window = pygame.display.set_mode(size=(600, 480))

    def run(self, ):
        print('Setup Start')
        print('Setup End')

        print('Loop Start')
        while True:
            #menu = Menu(self.window)
            #pass
            #check for all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('Quiting...')
                    pygame.quit() #Close window
                    quit()
