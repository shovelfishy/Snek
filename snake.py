from xmlrpc.client import Boolean
import pygame
import random
import math
 
WIDTH, HEIGHT = 690, 450
WIN = pygame.display.set_mode((WIDTH+100, HEIGHT+100))
BOARD = pygame.Surface((WIDTH, HEIGHT))

GRID = 30
GRID_HEIGHT = HEIGHT/GRID
GRID_WIDTH = WIDTH/GRID
collided = 0
start = 0


class player:
    def __init__(self):
        self.reset()
    
    def reset(self, pos=None):
        self.start = 0
        if pos != None:
            self.positions = pos
        else:
            self.positions = [[random.randint(0,GRID_WIDTH-1)*GRID,random.randint(0,GRID_HEIGHT-1)*GRID]]
        self.length = 1
        self.directions = ["up","down","left","right"]
        self.score = 0
        if self.head()[1] <= GRID:
            self.directions.remove("up")
        elif self.head()[1] >= HEIGHT-2*GRID:
            self.directions.remove("down")
        if self.head()[0] <= GRID:
            self.directions.remove("left")
        elif self.head()[0] >= WIDTH-2*GRID:
            self.directions.remove("right")
        self.directions = [("up","down"),("left","right"), self.directions]

    def head(self):
        return self.positions[0]

    def keys(self, events):
        input = pygame.key.get_pressed()
        for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
        
        if self.start == 1:
            if (input[pygame.K_w] or input[pygame.K_UP]):
                self.turn("up", 0)
            elif (input[pygame.K_s] or input[pygame.K_DOWN]):
                self.turn("down", 0)
            elif (input[pygame.K_a] or input[pygame.K_LEFT]):
                self.turn("left", 1)
            elif (input[pygame.K_d] or input[pygame.K_RIGHT]):
                self.turn("right", 1)
        else:
            if (input[pygame.K_w] or input[pygame.K_UP]) and "up" in self.directions[-1]:
                self.turn("up", 0)
                self.start = 1
            elif (input[pygame.K_s] or input[pygame.K_DOWN]) and "down" in self.directions[-1]:
                self.turn("down", 0)
                self.start = 1
            elif (input[pygame.K_a] or input[pygame.K_LEFT]) and "left" in self.directions[-1]:
                self.turn("left", 1)
                self.start = 1
            elif (input[pygame.K_d] or input[pygame.K_RIGHT]) and "right" in self.directions[-1]:
                self.turn("right", 1)
                self.start = 1
        
    def turn(self, direction, position):
        if self.directions[-1] in self.directions[position]:
            return 
        else:
            self.directions[-1] = direction
        
    def collide(self):
        global collided
        rect = pygame.Rect(self.head(),[GRID,GRID])
        if rect.right > WIDTH:
            self.reset()
            collided = 1
        elif rect.left < 0:
            self.reset()
            collided = 1
        if rect.bottom > HEIGHT:
            self.reset()
            collided = 1
        elif rect.top < 0:
            self.reset()
            collided = 1
        if self.length > 2 and self.head() in self.positions[2:]:
            self.reset()

    def move(self):
        current = list(self.head())
        if self.directions[-1] == "up":
            current[1]-=GRID
        elif self.directions[-1] == "down":
            current[1]+=GRID
        elif self.directions[-1] == "left":
            current[0]-=GRID
        elif self.directions[-1] == "right":
            current[0]+=GRID
        
        self.positions.insert(0,current)
        if len(self.positions) > self.length:
            self.positions.pop()


    def draw(self, **kwargs):
        for length in self.positions:
            rect = pygame.Rect(length[0],length[1],GRID,GRID)
            pygame.draw.rect(BOARD,(65,110,225),rect)
            pygame.draw.rect(BOARD,(255,255,255),rect,1)

class food:
    def __init__(self):
        self.randomize()

    def randomize(self, snake_pos=[]):
        self.position = (random.randint(0,GRID_WIDTH-1)*GRID,random.randint(0,GRID_HEIGHT-1)*GRID)
        while list(self.position) in snake_pos:
            self.position = (random.randint(0,GRID_WIDTH-1)*GRID,random.randint(0,GRID_HEIGHT-1)*GRID)

    def draw(self):
        if collided == 1:
            self.randomize()
        rect = pygame.Rect(self.position[0]+(GRID*1/10),self.position[1]+(GRID*1/10),GRID*4/5,GRID*4/5)
        pygame.draw.rect(BOARD,(231,71,29),rect)
        pygame.draw.rect(BOARD,(255,255,255),rect,1)

def grid():
    WIN.blit(BOARD,(50,50))
    for x in range(0, WIDTH, GRID):
            for y in range(0, HEIGHT, GRID):
                if (x/GRID + y/GRID) % 2 == 0:
                    pos = pygame.Rect(x, y, GRID, GRID)
                    pygame.draw.rect(BOARD, (167,217,72), pos)
                else: 
                    pos = pygame.Rect(x, y, GRID, GRID)
                    pygame.draw.rect(BOARD, (142,204,57), pos)

class Button:
    def __init__(self, pos, text, font, hover_font, color, hover_color=None):
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.hover_font = hover_font
        self.color = color
        self.text = text
        self.display = self.font.render(self.text, True, self.color)
        self.rect = self.display.get_rect(center=(self.x,self.y))
        self.rect.height = self.rect.height*0.7
        self.rect.center = (self.x,self.y)

    def draw(self, screen):
        # pygame.draw.rect(screen,(231,71,29),self.rect)
        screen.blit(self.display,(self.rect.topleft[0],self.rect.topleft[1]-self.rect.height*0.07))

    def mouse_distance(self, mouse):
        pos = tuple(abs(x-y) for x, y in zip(self.rect.center,mouse))
        self.relative = math.hypot(pos[0],pos[1])
        return self.relative

    def input(self, mouse):
        if self.rect.collidepoint(mouse):
            return True
        return False

    def hover(self, mouse, skip=False):
        if self.rect.collidepoint(mouse) and skip == False:
            self.display = self.hover_font.render(self.text, True, self.color)
            self.rect = self.display.get_rect(center=(self.x,self.y))
            self.rect.height = self.rect.height*0.7
            self.rect.center = (self.x,self.y)
        else:
            self.display = self.font.render(self.text, True, self.color)
            self.rect = self.display.get_rect(center=(self.x,self.y))
            self.rect.height = self.rect.height*0.7
            self.rect.center = (self.x,self.y)

def get_font(font, size, sysfont = True, bold = False, italic = False):
    if sysfont:
        return pygame.font.SysFont(font, size, bold, italic)
    else:
        if ".ttf" in font:
            return pygame.font.Font(font,size)
        else:
            return pygame.font.Font(font+".ttf",size)

def fade(displays1,displays2=None, variable=[], time=[1]):
    fade = pygame.Surface((WIDTH+100, HEIGHT+100))
    fade.fill((0,0,0))

    def create_display1():
        if isinstance(displays1[0][-1], list):
            for displays in displays1[0][:-1]:
                exec(displays)
            for displays in range(len(displays1[0][-1])):
                tempvar=variable[displays]
                exec(displays1[0][-1][displays])
        else:
            for displays in displays1[0]:
                exec(displays)
        for variables in range(len(displays1[1])):
            exec(f'{displays1[1][variables]=}'.split('=')[0] + displays1[2][variables])

    for alpha in range(0,255,2):
        fade.set_alpha(alpha)
        create_display1()
        WIN.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.wait(time[0])

    if displays2 is not None:
        def create_display2():
            for displays in displays2[0]:
                exec(displays)
            for variables in range(len(displays2[1])):
                if displays2[1][variables] != None:
                    exec(f'{displays2[1][variables]=}'.split('=')[0] + displays2[2][variables])
                else:
                    exec(displays2[2][variables])

        for alpha in range(255,0,-2):
            fade.set_alpha(alpha)
            create_display2()
            WIN.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.wait(time[1 if len(time) == 2 else 0])

def keys():
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return True

def game():
    global collided, start
    pygame.init()
    FPS = 10
    # pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    snake = player()
    snakefood = food()
    font = pygame.font.SysFont('monospace', 28, True)
    music = {'Pixel Game Background Music.wav':[0.25, 20000],'Boom Nation - your love is my drug (8bit slowed).wav':[0.35, 6000],'8 bit Seishun Buta Yarou - Fukashigi no carte.wav':[0.35, 6000],'Fukashigi no Carte (Bunny Girl Senpai ED) (Famitracker VRC6 8-Bit Cover).wav':[0.35, 6000],'Fukashigi no Carte Chiptune 8 bit Hetryll.wav':[0.35, 6000]}
    if not MAI_SANN:
        music_choice = random.choices(list(music.keys()), weights = (10,2,1,1,1))[0]
    else:
        music_choice = random.choices(list(music.keys()), weights = (0,0,1,1,1))[0]
    SONG_END = pygame.USEREVENT
    pygame.mixer.music.set_endevent(SONG_END)
    pygame.mixer.music.set_volume(music[music_choice][0])
    pygame.mixer.music.load('music/'+ music_choice)
    pygame.mixer.music.play(0, fade_ms=music[music_choice][1])
    bg = pygame.image.load("uwu.jpg")
    bg = pygame.transform.scale(bg,(bg.get_width()*1.2,bg.get_height()*1.2))
    bg_pos = bg.get_rect()
    bg_pos.center = (WIDTH/2,HEIGHT/2)
    
    while True:
        clock.tick(FPS)
        if not MAI_SANN:
            WIN.fill((87,138,52))
            grid()
        else:
            WIN.fill((0,0,0))
            WIN.blit(BOARD,(50,50))
            BOARD.blit(bg, bg_pos)
        
        events = pygame.event.get()

        for event in events:
            if event.type == SONG_END:
                music_choice = random.choices(list(music.keys()), weights = (10,4,2,2,2))[0]
                pygame.mixer.music.set_volume(music[music_choice][0])
                pygame.mixer.music.load('music/' + music_choice)
                pygame.mixer.music.play(0, fade_ms=music[music_choice][1])

        if start == 1:
            snake.reset(snake_startpos)
            snakefood.position = food_startpos
            start = 0

        snake.keys(events)
        snake.move()
        snake.collide()
        snakefood.draw()
        snake.draw()
        
        if collided == 1:
            collided = 0
        if tuple(snake.head()) == snakefood.position:
            snake.length += 1
            snakefood.randomize(snake.positions)
            snake.score+=1

        if not MAI_SANN:
            score = font.render(f"SCORE: {snake.score}", True, (0,0,0))
        else:
            score = font.render(f"SCORE: {snake.score}", True, (255,255,255))
        score_rect = score.get_rect()
        score_rect.center = (395, 25)
        WIN.blit(score, score_rect)
        
        pygame.display.update()


def myround(num, multiple):
    return math.ceil(num/multiple)


def main():
    pygame.init()
    FPS = 120
    pygame.display.set_caption("Snake Menu")
    clock = pygame.time.Clock()
    PLAY_BUTTON = Button((395,325),'Play',get_font("Silver",120,False),get_font("Silver",150,False),(0,0,0))
    QUIT_BUTTON = Button((395,415),'Quit',get_font("Silver",120,False),get_font("Silver",150,False),(0,0,0))
    button_sound = pygame.mixer.Sound("button sound.wav")
    button_sound.set_volume(0.5)
    pygame.mixer.music.load('music/8-Bit Fantasy & Adventure Music.wav')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1, fade_ms=3000)
    
    title = 1
    first_iter = 1
    timings = [2,3,4,5,6]
    timer = random.choices(timings, weights = [1,2,3,4,1])[0]
    frames = {'grass':[1,6*FPS,[(540,538),(600,435)],[5.5,6]], 'grass2_':[1,6*FPS,[(675,335),(350,523)],[4.3,6]],'sunflower':[1,4*FPS,[(150,390)],[6.5]],'lavender':[1,4*FPS,[(547,392)],[6]]}
    staticgrass = pygame.image.load('images/static grass.png')
    staticgrass = pygame.transform.scale(staticgrass,(100,35))
    blueflower = pygame.image.load('images/flower.png')
    blueflower = pygame.transform.scale(blueflower,(32,28))
    fade_variablesname = []
    fade_variablesobject = []
    numsurfaces = 0
    for x in list(frames.keys()):
        numsurfaces += len(frames[x][2])
    secret = pygame.Rect((0,0),(30,30))
    secret.topright = (WIDTH+100,0)
    global MAI_SANN 
    MAI_SANN = False

    while True:
        clock.tick(FPS)
        WIN.fill((87,138,52))
        pygame.draw.rect(WIN, (87,138,52), secret)
        MOUSE_POS = pygame.mouse.get_pos()
        BUTTON_POS = {}

        for button in ['PLAY_BUTTON', 'QUIT_BUTTON']:
            class_instance = eval(button)
            BUTTON_POS[str(button)] = class_instance.mouse_distance(MOUSE_POS)
            index = list(BUTTON_POS.values()).index(min(list(BUTTON_POS.values())))
            check = list(BUTTON_POS.keys())[index]

        for button in ['PLAY_BUTTON', 'QUIT_BUTTON']:
            class_instance = eval(button)
            if check == button:
                class_instance.hover(MOUSE_POS)
            else:
                class_instance.hover(MOUSE_POS, skip = True)
            class_instance.draw(WIN)
            class_instance.hover((WIDTH+1000,HEIGHT+1000))

        temp = myround(title,120)
        if temp > 10:
            temp = 10
        if first_iter == 1:
            path = 'images/'+'first_'+str(temp)+'.png'
        else:
            path = 'images/'+str(temp)+'.png'
        snek = pygame.image.load(path)
        snek = pygame.transform.scale(snek,(374,88)) 
        snek_pos = snek.get_rect()
        snek_pos.center = (395,180)
        WIN.blit(snek,snek_pos)
        title+=3
        if title >= 1200+timer*120 and first_iter != 1:
            title = 1
            timer = random.choices(timings, weights = [1,2,3,4,1])[0]
        elif title >= 1200+timer*120:
            title = 1
            first_iter = 0
            timer = random.choices(timings, weights = [1,2,3,4,1])[0]

        for frame in frames:
            temp = myround(frames[frame][0],120)
            exec(frame+f"=pygame.image.load('images/{frame}{temp}.png')")
            size = eval(frame).get_size()
            temp = fade_variablesname.copy()
            for surfaces in range(len(frames[frame][3])):
                current_surface = pygame.transform.scale(eval(frame),(frames[frame][3][surfaces]*size[0],frames[frame][3][surfaces]*size[1]))
                pos = current_surface.get_rect()
                pos.center = frames[frame][2][surfaces]
                WIN.blit(current_surface,pos)
                
                if len(fade_variablesname) == numsurfaces:
                    index = temp.index(frame)
                    if frame in fade_variablesname:
                        fade_variablesobject[index] = current_surface
                        temp[index] = None
            frames[frame][0] += 1
            if frames[frame][0] >= frames[frame][1]:
                frames[frame][0] = 1

            if len(fade_variablesname) != numsurfaces:
                        fade_variablesname.append(frame)
                        fade_variablesobject.append(current_surface)

        WIN.blit(staticgrass,(165,445))
        WIN.blit(staticgrass,(55,430))
        WIN.blit(blueflower,(690,292))

        if keys():
            if PLAY_BUTTON.input(MOUSE_POS) and check == 'PLAY_BUTTON': 
                global start, snake_startpos, food_startpos
                snake_startpos = [[random.randint(0,GRID_WIDTH-1)*GRID,random.randint(0,GRID_HEIGHT-1)*GRID]]
                food_startpos = (random.randint(0,GRID_WIDTH-1)*GRID,random.randint(0,GRID_HEIGHT-1)*GRID)
                button_sound.play()
                pygame.display.set_caption("Snake")
                pygame.mixer.music.fadeout(1500)
                
                variables = [snek, staticgrass,staticgrass,blueflower]
                variables.extend(fade_variablesobject)
                images = ['snek_pos = tempvar.get_rect()\nsnek_pos.center = (395,180)\nWIN.blit(tempvar,snek_pos)','WIN.blit(tempvar,(165,445))','WIN.blit(tempvar,(55,430))','WIN.blit(tempvar,(690,292))']
                temp = [None] * len(fade_variablesname)
                for surface in set(fade_variablesname.copy()):
                    searched_index = 0
                    for instances in range(fade_variablesname.count(surface)):
                        temp[fade_variablesname.index(surface,searched_index)] = f'pos = tempvar.get_rect()\npos.center = {frames[surface][2][instances]}\nWIN.blit(tempvar,pos)'
                        searched_index = fade_variablesname.index(surface) + 1
                images.extend(temp)

                if MAI_SANN:
                    easter_egg = "bg = pygame.image.load(\"uwu.jpg\")\nbg = pygame.transform.scale(bg,(bg.get_width()*1.2,bg.get_height()*1.2))\nbg_pos = bg.get_rect()\nbg_pos.center = (WIDTH/2,HEIGHT/2)\nWIN.blit(BOARD,(50,50))\nBOARD.blit(bg, bg_pos)"

                    fade([['WIN.fill((87,138,52))', images],[PLAY_BUTTON, QUIT_BUTTON],['.draw(WIN)', '.draw(WIN)']], [['WIN.fill((0,0,0))',easter_egg,'snake = player()','snakefood = food()', "font = pygame.font.SysFont('monospace', 28, True)", 'score = font.render(f"SCORE: 0", True, (255 ,255,255))','score_rect = score.get_rect()','score_rect.center = (395, 25)','WIN.blit(score, score_rect)'],[None, None, None, None],[f'snakefood.position={food_startpos}', 'snakefood.draw()', f'snake.positions={snake_startpos}', 'snake.draw()']],variable=variables)
                    start = 1
                    game()

                fade([['WIN.fill((87,138,52))', images],[PLAY_BUTTON, QUIT_BUTTON],['.draw(WIN)', '.draw(WIN)']], [['WIN.fill((87,138,52))','grid()','snake = player()','snakefood = food()', "font = pygame.font.SysFont('monospace', 28, True)", 'score = font.render(f"SCORE: 0", True, (0,0,0))','score_rect = score.get_rect()','score_rect.center = (395, 25)','WIN.blit(score, score_rect)'],[None, None, None, None],[f'snakefood.position={food_startpos}', 'snakefood.draw()', f'snake.positions={snake_startpos}', 'snake.draw()']],variable=variables)

                start = 1
                game()
            elif QUIT_BUTTON.input(MOUSE_POS) and check == 'QUIT_BUTTON':
                button_sound.play()
                pygame.display.set_caption("Quitting...")
                pygame.mixer.music.fadeout(1500)

                variables = [snek, staticgrass,staticgrass,blueflower]
                variables.extend(fade_variablesobject)
                images = ['snek_pos = tempvar.get_rect()\nsnek_pos.center = (395,180)\nWIN.blit(tempvar,snek_pos)','WIN.blit(tempvar,(165,445))','WIN.blit(tempvar,(55,430))','WIN.blit(tempvar,(690,292))']
                temp = [None] * len(fade_variablesname)
                for surface in set(fade_variablesname.copy()):
                    searched_index = 0
                    for instances in range(fade_variablesname.count(surface)):
                        temp[fade_variablesname.index(surface,searched_index)] = f'pos = tempvar.get_rect()\npos.center = {frames[surface][2][instances]}\nWIN.blit(tempvar,pos)'
                        searched_index = fade_variablesname.index(surface) + 1
                images.extend(temp)

                fade([['WIN.fill((87,138,52))', images],[PLAY_BUTTON, QUIT_BUTTON],['.draw(WIN)', '.draw(WIN)']],time=[3], variable=variables)
                pygame.quit()
            elif secret.collidepoint(MOUSE_POS):
                MAI_SANN = True

        pygame.display.update()



main()