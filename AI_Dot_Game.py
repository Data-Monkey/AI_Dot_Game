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

MUTATE_RATIO = 0.5

TARGET_XY = (int(WIDTH/2),5)
START_XY =  (400,200) #(int(WIDTH/2),HEIGHT-5)  # start at the bottom centre
VECTOR_LEN = 10
POPULATION_SIZE = 200


def random_vector():
    X = random.randint(VECTOR_LEN*(-1),VECTOR_LEN)
    Y = random.randint(VECTOR_LEN*(-1),VECTOR_LEN)
    return [X,Y]

def generate_instructions(num = 1000):
    inst = []
    for i in range(num):
        XY = random_vector()
        inst.append(XY)
    return inst


            

def draw_target():
    pygame.draw.circle(screen,GREEN,TARGET_XY,8)
    
# -------------------------------------------------------------------    
    
class Dot:
    def __init__(self):
        self.instructions = generate_instructions(1000)
        self.posXY = START_XY
        self.dead = False
        self.reached_goal = False
        self.winner = False
        self.step= 0
        self.fitness =0.00

    def _distance(self, posA=(0,0), posB=(0,0)):
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
        # or has the dot reached the target?
        elif self._distance(self.posXY,TARGET_XY) < 5 :
            self.reached_goal = True
            
            
    def calculate_fitness(self):
        # fitness is a function of distance to target
        # if target reached it is a function of steps taken
        
        if self.reached_goal:
            #self.fitness = 1.0/16.0 
            self.fitness = 1.0/160.0 + 10000.00/float(self.step**2);
            print(f'steps {self.step} / fitness {self.fitness*1000}')
        else:
            dist = self._distance(self.posXY, TARGET_XY)
            if dist == 0.0:
                self.fitness = 0.0
            else:
                self.fitness = 1.00 / (dist**2)
            
            print(f'distance {dist} / fitness {float(self.fitness*1000)} / steps {self.step}')
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
        self.generation = 1
        self.total_fitness = 0
        self.best_steps = 1000
        self.dots = []
        # create the generation of dots
        [self.dots.append(Dot()) for i in range(pop_size)]
            
            
    def show(self):
        [dot.show() for dot in self.dots]
            
    def update(self):
        [dot.update(self.best_steps) for dot in self.dots]

    def calculate_fitness(self):
        self.total_fitness = sum([dot.calculate_fitness() for dot in self.dots])
        return self.total_fitness
            
    def alive(self):
        for dot in self.dots:
            if dot.alive():
                return True
        return False  # nobody alive
    
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
        best = Dot()
        for dot in self.dots:
            if dot.fitness > best.fitness:
                best = dot
        
        if best.reached_goal:
            #update best steps
            self.best_steps = best.step
            print (f'best steps: {self.best_steps}')
            print (f'best fitness: {best.fitness}')
        
        #only take the instructions
        best = best.clone()
        best.winner = True
        return best

    def select_parent(self):
        multiplier = 100000
        rand = random.randint(0,int(self.total_fitness*multiplier))
        
        running_sum = 0.000        
        for dot in self.dots:
            running_sum += (dot.fitness*multiplier)
            if running_sum > rand:
                return dot.clone()
        
        # this should never happen
        return dot[1].clone()
            
        
# -------------------------------------------------------------------
screen = pygame.display.set_mode(size)


pop = Population(POPULATION_SIZE)

for i in range(2) : 
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
    print(f'Gen {pop.generation} total fitness {pop.total_fitness}')
   # pop = Population(POPULATION_SIZE)
    pop = pop.natural_selection()

  #  test.mutateDemBabies();




pygame.quit()
sys.exit()
