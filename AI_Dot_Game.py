import sys
import pygame
import operator  #add TUPLES
import random



pygame.init()
clockobject = pygame.time.Clock()
clockobject.tick(1)

size = WIDTH, HEIGHT = 800,800

BLACK = 0, 0, 0
GREEN = 0,255,0
RED = 255,0,0
BLUE = 0,0,255
WHITE = 255,255,255

MUTATE_RATIO = 0.02

TARGET_XY = (int(WIDTH/2),5)
START_XY =  (400,200) #(int(WIDTH/2),HEIGHT-5)  # start at the bottom centre
VECTOR_LEN = 10
POPULATION_SIZE = 100


def draw_target():
    pygame.draw.circle(screen,GREEN,TARGET_XY,8)

# -------------------------------------------------------------------

class Dot:
    def __init__(self):
        self.instructions = []
        self.posXY = START_XY
        self.dead = False
        self.reached_goal = False
        self.winner = False
        self.step= 0
        self.fitness = 0.000000


    def __random_vector(self):
        X = random.randint(VECTOR_LEN*(-1),VECTOR_LEN)
        Y = random.randint(VECTOR_LEN*(-1),VECTOR_LEN)
        return (X,Y)

    def randomize_instructions(self, size=1000):
        for i in range(size):
            XY = self.__random_vector()
            self.instructions.append(XY)
        return self.instructions        

    def __distance(self, posA=(0,0), posB=(0,0)):
        dx = abs(posA[0] - posB[0])
        dy = abs(posA[1] - posB[1])
        return (dx**2 + dy**2)**0.5

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
        # or has the dot reached the target?
        elif self.__distance(self.posXY,TARGET_XY) < 5 :
            self.reached_goal = True


    def calculate_fitness(self):
        # fitness is a function of distance to target
        # if target reached it is a function of steps taken
        dist = self.__distance(self.posXY, TARGET_XY)
        if dist == 0.0:
            dist = 0.1        
        self.fitness = 1.00 / (dist**2)
        return self.fitness

    def alive(self):
        return not (self.reached_goal or self.dead)

    def clone(self):
         clone = Dot()
         clone.instructions = self.instructions
         return clone

    def mutate(self):
        for i in range(len(self.instructions)):
            if random.random() < MUTATE_RATIO:
                self.instructions[i] = random_vector()


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


    def show(self):
        [dot.show() for dot in self.dots]

    def update(self):
        [dot.update() for dot in self.dots]

    def calculate_fitness(self):
        self.total_fitness = sum([dot.calculate_fitness() for dot in self.dots])
        return self.total_fitness

    def randomize_instructions(self, size=1000):
        [dot.randomize_instructions(size) for dot in self.dots]

    def alive(self):
        for dot in self.dots:
            if dot.alive():
                return True
        return False  # nobody alive

    def natural_selection(self):
        nextGen = Population(len(self.dots))
        print(f'next gen size: {len(nextGen.dots)}')
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

        #rand = random.uniform(0,self.total_fitness)
        
        rand = random.randint(0,POPULATION_SIZE-1)
        return self.dots[rand].clone()

#        running_sum = 0.000
#        for dot in self.dots:
#            running_sum += dot.fitness
#            if running_sum >= rand:
#                return dot.clone()
#
#        # this should never happen
#        return None


# -------------------------------------------------------------------
screen = pygame.display.set_mode(size)

gen = []
pop = Population(POPULATION_SIZE)
pop.randomize_instructions(1000)

for i in range(5) :
# let evolution do its work


    pygame.display.update()
    while pop.alive():
        # draw the playing field
        draw_target()

        pop.show()
        pop.update()

        # clean up for next move
        pygame.display.flip()
        screen.fill(BLACK)

    # generation done
    pop.calculate_fitness()
    gen.append(pop)
    print(f'Gen {pop.generation} total fitness {pop.total_fitness}')
    print(f'  best fitness: {pop.best_fitness}')
   # pop = Population(POPULATION_SIZE)
    next_pop = pop.natural_selection()
    pop = next_pop

  #  test.mutateDemBabies();




pygame.quit()
#sys.exit()
