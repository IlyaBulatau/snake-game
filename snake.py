import pygame

from random import randrange
import sys

from colors import *


class Game():
    '''
    Класс мнеджер игры
    '''
    def __init__(self):
        self.window_width = 720 # ширина окна
        self.window_hight = 480 # высота окна
        self.clock = pygame.time.Clock() # переменная таймера
        self.score = 0 # счет игры
        self.FPS = 30 # ФПС - влияет на скорость игры
        self.movie = 'right' # определяет куда будет двигаться змеяя

    def game_surf(self):
        '''
        Создает окно и надпись
        '''
        self.window = pygame.display.set_mode((self.window_width, self.window_hight))
        pygame.display.set_caption('Snake')

    def window_update(self):
        '''
        Обновляет экран в цикле и запускает ФПС
        '''
        pygame.display.update()
        self.clock.tick(self.FPS)

    def keyboard_controller(self):
        '''
        Конролирует нажатие клавишь - для управления змейкой по стрелкам
        а так же закрывает игру нажатием клавиши ESC
        '''
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.movie != 'right':
                    self.movie = 'left'
                elif event.key == pygame.K_RIGHT and self.movie != 'left':
                    self.movie = 'right'
                elif event.key == pygame.K_UP and self.movie != 'down':
                    self.movie = 'up'
                elif event.key == pygame.K_DOWN and self.movie != 'up':
                    self.movie = 'down'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return self.movie
    
    def show_score(self): # TODO - вести и отоброажать счет игры
        ...
    
    def game_over(self): # TODO - окончание игр если змейка врезалась в сому себя или стенку
        ...

class Apple(Game):
    '''
    Класс отвечает за появления яблок которые будет есть змея
    '''
    def __init__(self):
        Game.__init__(self)
        self.apple_position = [randrange(1, (self.window_width//10))*10,
                            randrange(1, (self.window_hight//10))*10,] # позиция появления яблока по 2 осям рандомно на экране
        self.apple_spawn = True # появляться ли яблокам 
    
    def apple_spawn_check(self):
        '''
        Если яблока нету создает яблоко на экране
        '''
        if not self.apple_spawn:
                self.apple_position = [randrange(1, (self.window_width//10))*10,
                            randrange(1, (self.window_hight//10))*10,]
        
    def apple_draw(self, window):
        '''
        Рисует яблоко на экране
        '''
        pygame.draw.rect(window,
                         WHITE, 
                         pygame.Rect(self.apple_position[0], # координата по оси х
                                     self.apple_position[1], # по оси у
                                     10, 10)) # размер яблока

class Snake(Apple):
    '''
    Класс змеи
    '''
    def __init__(self):
        super(Apple, self).__init__()
        self.snake_position = [100, 50] # позиция головы змеи на экране
        self.snake_body = [[100, 50], # позиции тела змеи 1 элемент - голова 2 - тело 3 - хвост
                           [90, 50],
                           [80, 50],
                          ]
      
    def snake_move(self, movie):
        '''
        Отвечает за передвижения змеии принимает параметр movie из класса Game 
        который выбирает направление движения в зависимости от нажатой клавиши
        '''
        if movie == 'right':
            self.snake_position[0] += 10
        elif movie == 'left':
            self.snake_position[0] -= 10
        elif movie == 'up':
            self.snake_position[1] -= 10
        elif movie == 'down':
            self.snake_position[1] += 10
        return movie
    
    def snake_body_increase(self, apple_pos_x, apple_pos_y, windwo_x, window_y):
        '''
        Функция отвечающая за рост зменни после сьедания яблока,
        так же возращает новую позицию яблока для его последующего появления за которое отвечает класс Apple
        '''
        self.snake_body.insert(0, list(self.snake_position)) # добавляет в начало списка тела змеи позиция головы
        if self.snake_position[0] == apple_pos_x and self.snake_position[1] == apple_pos_y: # если змея сьела головой яблоко
            apple_pos_x, apple_pos_y = [randrange(1, (windwo_x//10))*10, # создаеться новая позиция для яблока
                            randrange(1, (window_y//10))*10,]
        else:
            self.snake_body.pop() # удаляется послдний элемент что бы змея постоянно не росла
        return apple_pos_x, apple_pos_y # возврат новых координат яблока
        
    
    def snake_draw(self, window):
        '''
        Рисует змейку по координата из списка snake_body
        '''
        for pos in self.snake_body:
            pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    def check_snake_boudaries(sefl): # TODO - преверить столкнулась ли змейка с собой или стенкой
        ...
    
# создание обьектов
game = Game() 
snake = Snake()
apple = Apple()
# инициализация pygame
pygame.init()
# создание окна
game.game_surf()

while True:
    game.keyboard_controller() # главный цикл
    game.window.fill(BLACK) # заливвка экрана для его обновления
    snake.snake_move(game.movie) # проверят направления движения змейкит
    apple.apple_position = snake.snake_body_increase(apple.apple_position[0], apple.apple_position[1], game.window_width, game.window_hight) # передает яблоку новую позиция для создания
    snake.snake_draw(game.window) # рисует змею
    apple.apple_draw(game.window) # рисует яблоко
    game.window_update() # обновление окна + таймер
    
    


# if __name__ == '__main__':
#     main()