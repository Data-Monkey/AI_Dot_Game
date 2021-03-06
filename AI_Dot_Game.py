import sys
import pygame
import operator  #add TUPLES
import random




WIDTH, HEIGHT = 800,800

BLACK = 0, 0, 0
GREEN = 0,255,0
RED = 255,0,0
BLUE = 0,0,255
WHITE = 255,255,255

MUTATE_RATIO = 0.02

TARGET_XY = (int(WIDTH/2),5)
START_XY =  (int(WIDTH/2),HEIGHT-50)  # start at the bottom centre
VECTOR_LEN = 10
POPULATION_SIZE = 100
OBSTACLE_MODE = ('none','simple','medium','hard','rand')[3]


def draw_target():
    pygame.draw.circle(screen,GREEN,TARGET_XY,8)

# -------------------------------------------------------------------
class Obstacle:
    def __init__(self, tlXY=(300,400), width=100, height=20):
        self.tlXY = tlXY
        self.width = width
        self.height = height
        self.color = RED
        self.rect = [*self.tlXY, self.width, self.height]
        
    def show(self):
        return pygame.draw.rect(screen, self.color, self.rect,2)
        
    def collision(self, dotXY=(0,0)):
        if (dotXY[0] >= self.tlXY[0] and 
            dotXY[0] <= self.tlXY[0]+self.width and  
            dotXY[1] >= self.tlXY[1] and 
            dotXY[1] <= self.tlXY[1]+self.height):
               return True
        return False

# -------------------------------------------------------------------

class Obstacles:
    def __init__(self, mode='none'):
        self.mode = mode            
        self.obstacles = []
        self.create_obstacles()
        
    def create_obstacles(self):
        if self.mode == 'simple':
            self.obstacles.append(Obstacle((300,400),400,20))
        elif self.mode == 'medium':
            self.obstacles.append(Obstacle((100,500),300,10))
        elif self.mode == 'hard':
            self.obstacles.append(Obstacle((300,300),500,10))
            self.obstacles.append(Obstacle((0,400),500,10))
        elif self.mode == 'rand':
            for i in range(random.randint(3,5)):
                X = random.randint(0,WIDTH-10)
                Y = random.randint(50,HEIGHT-50)
                W = random.randint(10,WIDTH-X)
                H = random.randint(10,20)
                self.obstacles.append(Obstacle((X,Y),W,H))
    
    def show(self):
        [obst.show() for obst in self.obstacles]

    def collision(self, dotXY):            
        if True in [obst.collision(dotXY) for obst in self.obstacles]:
            return True
        return False
    
# -------------------------------------------------------------------
class Dot:
    def __init__(self):
        self.instructions = []
        self.posXY = START_XY
        self.dead = False
        self.reached_goal = False
        self.winner = False
        self.step = 0
        self.fitness = 0.0

    def random_vector(self):
        X = random.randint(VECTOR_LEN*(-1),VECTOR_LEN)
        Y = random.randint(VECTOR_LEN*(-1),VECTOR_LEN)
        return (X,Y)

    def randomize_instructions(self, size=1000):
        for i in range(size):
            XY = self.random_vector()
            self.instructions.append(XY)
        return self.instructions        

    def __distance(self, posA=(0,0), posB=(0,0)):
        dx = abs(posA[0] - posB[0])
        dy = abs(posA[1] - posB[1])
        return int((dx**2 + dy**2)**0.5)

    def show(self):
        if self.winner:
            pygame.draw.circle(screen, BLUE, self.posXY,3)
        elif self.reached_goal:
            pygame.draw.circle(screen, RED, self.posXY,1)
        else:
            pygame.draw.circle(screen, WHITE, self.posXY,1)

    def move(self, move_limit=1000):
        if min(len(self.instructions),move_limit) > self.step:
            #still instructions left to do
            self.posXY = tuple(map(operator.add, self.posXY, self.instructions[self.step]))
            self.step += 1
        else:
            self.dead = True

    def update(self, move_limit=1000):
        # move the dot if it is still alive
        if self.alive() :
            self.move(move_limit)
        # check if that move killed the dot
        if (self.posXY[0]<3 or self.posXY[1]<3 or
           self.posXY[0]>WIDTH-3 or self.posXY[1]>HEIGHT-3):
            self.dead = True
        elif obst.collision(self.posXY):
            self.dead = True
        # or has the dot reached the target?
        elif self.__distance(self.posXY,TARGET_XY) < 4 :
            self.reached_goal = True


    def calculate_fitness(self):
        # fitness is a function of distance to target
        # if target reached it is a function of steps taken
        dist = self.__distance(self.posXY, TARGET_XY)
        if self.reached_goal:
            self.fitness = 1.0/16.0 + 1000.0/self.step
        else:
            self.fitness = 1.00 / (dist**2)
        return self.fitness

    def alive(self):
        return not (self.reached_goal or self.dead)

    def clone(self):
         clone = Dot()
         clone.instructions = self.instructions[:]
         return clone

    def mutate(self):
        for i in range(len(self.instructions)):
            if random.random() < MUTATE_RATIO:
                self.instructions[i] = self.random_vector()


# -------------------------------------------------------------------
class Population:
    def __init__(self,pop_size=10):
        self.generation = 0
        self.total_fitness = 0.000000
        self.best_fitness = 0.000000
        self.best_steps = 1000
        self.dots = []
        # create the generation of dots
        [self.dots.append(Dot()) for i in range(pop_size)]

    def show_stats(self):
        screen.blit(font.render(f'Generation: {self.generation+1}', True, (255,0,0)), (10, 10))
        pygame.display.update()

    def show(self):
        self.show_stats()
        [dot.show() for dot in self.dots]

    def update(self):
        [dot.update() for dot in self.dots]

    def calculate_fitness(self):
        self.total_fitness = sum([dot.calculate_fitness() for dot in self.dots])
        return self.total_fitness

    def randomize_instructions(self, size=1000):
        [dot.randomize_instructions(size) for dot in self.dots]

    def alive(self):
        return (True in [dot.alive() for dot in self.dots])
        
    def natural_selection(self):
        nextGen = Population(len(self.dots))
        # find a parent for all new dots and mutate them
        for i in range(len(nextGen.dots)):
            newDot = self.select_parent()
            newDot.mutate()
            nextGen.dots[i] = newDot

        # keep the winner!
        nextGen.dots[0] = self.best_dot()
        nextGen.best_steps = self.best_steps
        nextGen.generation = self.generation + 1
        return nextGen

    def best_dot(self):
        fittest_dot = Dot()
        for dot in self.dots:
            if dot.fitness > fittest_dot.fitness:
                fittest_dot = dot

#        if fittest.reached_goal:
            #update best steps
#            self.best_steps = fittest.step
#            print (f'best steps: {self.best_steps}')
#            print (f'best fitness: {best.fitness}')
        
        self.best_fitness = fittest_dot.fitness
        #only take the instructions
        best_dot = fittest_dot.clone()
        best_dot.winner = True
        return best_dot

    def select_parent(self):
        """ the fitness of each parent determines the likelyhood 
            of being chosen to have babies (each baby only has 1 parent)
        """
        rand = random.uniform(0,self.total_fitness)
        running_sum = 0.0
        for dot in self.dots:
            running_sum += dot.fitness
            if running_sum >= rand:
                return dot.clone()

        # this should never happen
        return None

    def stop_evolution(self):
        return self.total_fitness > 6

# -------------------------------------------------------------------
if __name__ == "__main__":
# -------------------------------------------------------------------
    pygame.init()
    clockobject = pygame.time.Clock()
    #clockobject.tick(1)

    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    font = pygame.font.SysFont('Arial', 12)
    
    obst = Obstacles(mode=OBSTACLE_MODE)
    
    pop = Population(POPULATION_SIZE)
    pop.randomize_instructions(1000)
    
    stop_evolution = False
    
    while not stop_evolution:
    # let evolution do its work
        pygame.display.update()
        while pop.alive():
            # draw the playing field
            draw_target()
            obst.show()
            # show the dots and move them
            pop.show()
            pop.update()
            # clcean up for next move
            pygame.display.flip()
            screen.fill(BLACK)
            
        # generation done
        pop.calculate_fitness()
        print(f'Gen {pop.generation} total fitness {pop.total_fitness}')
        stop_evolution = pop.stop_evolution()
        next_pop = pop.natural_selection()
        pop = next_pop
    
    input('Press ENTER to exit')
    pygame.quit()
    sys.exit()
