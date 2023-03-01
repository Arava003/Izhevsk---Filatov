# подключаем нужные библиотеки
import pygame
from random import randint
from math import floor

# основной класс Board
class Board:
    # инит
    def __init__(self, width, height, left, top):
        #
        self.game_go = False
        self.turn = False
        self.width = width
        self.height = height
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                      [5, 0, 5, 5, 5, 0, 0, 0, 0, 0],
                      [5, 0, 0, 0, 0, 0, 5, 5, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 5, 5, 5, 0, 0, 0, 5, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
                      [0, 0, 0, 5, 0, 5, 5, 0, 0, 0],
                      [5, 0, 0, 5, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 5, 0, 5, 0, 0, 0, 0],
                      [0, 5, 0, 5, 0, 0, 0, 0, 5, 0]]
        self.left = left
        self.top = top
        self.cell_size = 60

        # подключаем звуки попаданий
        self.sound_est_probitie1 = pygame.mixer.Sound('data/sounds/probitie1.wav')
        self.sound_est_probitie2 = pygame.mixer.Sound('data/sounds/probitie2.wav')
        self.sound_popadanie = pygame.mixer.Sound('data/sounds/popadanie.wav')
        self.sounds_good = [self.sound_est_probitie1, self.sound_est_probitie2, self.sound_popadanie]

        # подключаем звуки промахов
        self.sound_ne_probil = pygame.mixer.Sound("data/sounds/ne-probil.wav")
        self.bronja_ne_probita = pygame.mixer.Sound("data/sounds/bronja-ne-probita.wav")
        self.sounds_bad = [self.sound_ne_probil, self.bronja_ne_probita]

        # подключаем звуки уничтожения
        self.sound_gotov = pygame.mixer.Sound("data/sounds/gotov.wav")
        self.unichtoshen = pygame.mixer.Sound("data/sounds/unichtoshen.wav")
        self.sounds_kill = [self.sound_gotov, self.unichtoshen]

        # подключаем звуки выстрелов
        self.shot1 = pygame.mixer.Sound("data/sounds/shot_1.wav")
        self.shot2 = pygame.mixer.Sound("data/sounds/shot_2.wav")
        self.shot3 = pygame.mixer.Sound("data/sounds/shot_3.wav")
        self.shot4 = pygame.mixer.Sound("data/sounds/shot_4.wav")
        self.sounds_shots = [self.shot1, self.shot2, self.shot3, self.shot4]

    # функция отрисовки доски с элементами
    def render(self, screen):

        # проверка на то, что идёт игра
        if self.game_go:
            # отрисовка полей доски
            for y in range(self.height):
                for x in range(self.width):
                    pygame.draw.rect(screen, pygame.Color(0, 0, 0), (
                        x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                        self.cell_size), 2)

            # отрисовка буковок для доски
            x = self.left + self.cell_size // 2 - 5
            y = self.top - self.cell_size // 2 + 5
            for book in ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']:
                f = pygame.font.SysFont('arial', 16)
                sc_text = f.render(book, True, (255, 255, 255))
                screen.blit(sc_text, (x, y))
                x += self.cell_size

            # отрисовка циферок для доски
            x = self.left - self.cell_size // 2 + 10
            y = self.top + self.cell_size // 2 - 10
            for book in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                f = pygame.font.SysFont('arial', 16)
                sc_text = f.render(book, True, (255, 255, 255))
                screen.blit(sc_text, (x, y))
                y += self.cell_size

            # отрисовка промахов и попаданий
            for i in range(10):
                for j in range(10):
                    if self.board[i][j] == -1:
                        pygame.draw.circle(screen, (0, 0, 255), (
                            self.left + j * self.cell_size + self.cell_size / 2,
                            self.top + i * self.cell_size + self.cell_size / 2), 10)
                    elif self.board[i][j] == 1:
                        pygame.draw.line(screen, (255, 0, 0),
                                         (self.left + j * self.cell_size + 2, self.top + i * self.cell_size + 2),
                                         (
                                             self.left + (j + 1) * self.cell_size - 2,
                                             self.top + (i + 1) * self.cell_size - 2),
                                         2)
                        pygame.draw.line(screen, (255, 0, 0),
                                         (self.left + (j + 1) * self.cell_size - 2, self.top + i * self.cell_size + 2),
                                         (self.left + j * self.cell_size + 2, self.top + (i + 1) * self.cell_size - 2),
                                         2)

        # начальный экран
        else:

            # отрисовка кнопки PvP
            f1 = pygame.font.SysFont('arial', 70)
            sc_text1 = f1.render("Player VS Bot", True, (255, 255, 255), (128, 128, 128))
            screen.blit(sc_text1, (sc_text1.get_rect(center=(1430 // 2, 200))))

            # отрисовка кнопки PvE
            f2 = pygame.font.SysFont('arial', 70)
            sc_text2 = f2.render("Player VS Player", True, (255, 255, 255), (128, 128, 128))
            screen.blit(sc_text2, (sc_text2.get_rect(center=(1430 // 2, 300))))

            # отрисовка кнопки Settings
            f3 = pygame.font.SysFont('arial', 70)
            sc_text3 = f3.render("Settings", True, (255, 255, 255), (128, 128, 128))
            screen.blit(sc_text3, (sc_text3.get_rect(center=(1430 // 2, 400))))



    # функция выстрела
    def shot(self, x, y, other):
        # звук выстрела
        self.sounds_shots[randint(0, 3)].play()
        # проверка на пустую клетку
        if self.board[y][x] == 0:
            self.board[y][x] = -1
            self.sounds_bad[randint(0, 1)].play()
        # проверка на клетку с кораблём
        elif self.board[y][x] == 5:
            self.board[y][x] = 1
            self.turn = True
            other.turn = False
            self.sounds_good[randint(0, 2)].play()


# запуск программы
if __name__ == '__main__':

    #
    game_start = False
    start_menu = True
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    # подключение музыки
    pygame.mixer.music.load("data/music/music1.mp3")
    pygame.mixer.music.play(-1)
    music_pause = False
    vol = 0.5

    # задание размеров окна
    size = 1430, 670
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Морской бой на минималках')
    board1 = Board(10, 10, 30, 30)
    board1.turn = True
    board2 = Board(10, 10, 820, 30)
    board2.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 5, 0, 0, 0, 5, 0, 0, 0, 0],
                    [0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 5, 0, 0, 0, 0, 5, 0, 0, 0],
                    [0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 5, 0, 5, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 5, 0, 5, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    running = True
    # цикл всех игровых действий
    while running:

        # отрисовка фона
        fon = pygame.image.load("data/images/fon.jpg")
        fon = pygame.transform.scale(fon, (1430, 670))
        screen.blit(fon, (0, 0))

        # отрисовка досок
        board1.render(screen)
        board2.render(screen)
        for event in pygame.event.get():

            # выход из игры
            if event.type == pygame.QUIT:
                running = False

            # клик мышки
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if game_start:

                    # проверка на ход первого игрока
                    if board1.turn == True:

                        # проверка на нахождение мышки во время клика в пределах второй доски
                        if board2.left <= event.pos[0] <= board2.width * board2.cell_size + board2.left and \
                                board2.top <= event.pos[1] <= board2.height * board2.cell_size + board2.top:
                            x, y = floor((event.pos[0] - board2.left) / board2.cell_size), floor(
                                (event.pos[1] - board2.top) / board2.cell_size)

                            # проверка на пустоту клетки(ещё не стреляли)
                            if board2.board[y][x] in (0, 5):
                                board1.turn = False
                                board2.turn = True
                                board2.shot(x, y, board1)

                    # проверка на ход второго игрока
                    elif board2.turn == True:

                        # проверка на нахождение мышки во время клика в пределах первой доски
                        if board1.left <= event.pos[0] <= board1.width * board1.cell_size + board1.left and \
                                board1.top <= event.pos[1] <= board1.height * board1.cell_size + board1.top:
                            x, y = floor((event.pos[0] - board1.left) / board1.cell_size), floor(
                                (event.pos[1] - board1.top) / board1.cell_size)

                            # проверка на пустоту клетки(ещё не стреляли)
                            if board1.board[y][x] in (0, 5):
                                board1.turn = True
                                board2.turn = False
                                board1.shot(x, y, board2)

                elif start_menu:
                    if 500 <= event.pos[0] <= 930 and 260 <= event.pos[1] <= 340:
                        game_start = True
                        start_menu = False
                        board1.game_go = True
                        board2.game_go = True
                    elif 540 <= event.pos[0] <= 900 and 160 <= event.pos[1] <= 240:
                        game_start = True
                        start_menu = False
                        board1.game_go = True
                        board2.game_go = True


            # проверка на нажатие клавиатуры
            elif event.type == pygame.KEYDOWN:

                # проверка на нажатие пробела
                if event.key == pygame.K_SPACE:

                    # пауза/продолжение музыки
                    music_pause = not music_pause
                    if music_pause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

                # проверка на нажатие левой стрелочки
                elif event.key == pygame.K_LEFT:

                    # уменьшение громкости
                    vol -= 0.05
                    pygame.mixer.music.set_volume(vol)
                    if vol < 0:
                        vol = 0.0

                # проверка на нажатие левой стрелочки
                elif event.key == pygame.K_RIGHT:

                    # увеличение громкости
                    vol += 0.05
                    pygame.mixer.music.set_volume(vol)
                    if vol > 1:
                        vol = 1.0

                # проверка на нажатие кнопки q
                elif event.key == pygame.K_q:

                    # воспроизведение музыки заново
                    pygame.mixer.music.rewind()

        pygame.display.flip()
    pygame.quit()



# Дядя Дима, прошу вас, пощадите этого бедного разработчика
# Он не спла целых три ночи, чтобы написать этот прекрасный(нет) код
# Поставьте ему чуть-чуть побольше баллов
# Во вселенной существует карма, и если вы сделаете добро, то оно обязательно вернётся к вам
# Да хранит вас господь
# Аминь
