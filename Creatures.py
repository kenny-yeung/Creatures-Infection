### COMPSCI 130, Summer School 2019
### Project Two - Creatures
import turtle
import hashlib

## This class represents a creature
class Creature:

    ## A creature stores its position and direction and its "DNA" - the list of instructions it follows
    def __init__(self, row, col, dna, direction):
        self.direction = direction
        self.row = row
        self.col = col
        self.dna = dna
        self.next_instruction = 1

    ## A creature draws itself using the colour specified as part of its dna
    ## the size of the grid squares, and the position of the top-left pixel are provided as input
    def draw(self, grid_size, top_left_x, top_left_y):

        ## Compute the position of the top left hand corner of the cell this creature is in
        x = top_left_x + (self.col-1)*grid_size
        y = top_left_y - (self.row-1)*grid_size
        turtle.color(self.dna[0].split(":")[1])

        ## Draw the creature
        turtle.goto(x, y)
        turtle.pendown()
        turtle.begin_fill()
        
        ##draws the creature if facing North
        if self.direction == "North":
            turtle.goto(x + grid_size / 2, y)
            turtle.goto(x + grid_size, y - grid_size)
            turtle.goto(x, y - grid_size)
            turtle.goto(x + grid_size/ 2, y)
            
        ##draws the creature if facing East    
        if self.direction == "East":
            turtle.goto(x + grid_size, y - grid_size / 2)
            turtle.goto(x + grid_size, y - grid_size / 2)
            turtle.goto(x, y - grid_size)
            turtle.goto(x, y)
            
        ##draws the creature if facing South    
        if self.direction == "South":
            turtle.goto(x + grid_size, y)
            turtle.goto(x + grid_size/2, y - grid_size)
            turtle.goto(x + grid_size/ 2, y - grid_size)
            turtle.goto(x, y)
            
        ##draws the creature if facing West    
        if self.direction == "West":
            turtle.goto(x + grid_size, y)
            turtle.goto(x + grid_size, y - grid_size)
            turtle.goto(x, y - grid_size / 2)
            turtle.goto(x + grid_size, y)
            
        turtle.end_fill()
        turtle.penup()
            
        turtle.color("black")

    ## Returns the name of the species for this creature
    def get_species(self):
        return self.dna[0].split(":")[0]

    ## Gets the current position of the creature
    def get_position(self):
        return (self.row, self.col)

    ## Returns a string representation of the creature
    def __str__(self):
        return str(self.get_species() + ' ' + str(self.row) + ' ' + str(self.col) + ' ' + str(self.direction))

    ## Execute a single move (either hop, left or right) for this creature by following the instructions in its dna
    def make_move(self, world):
        finished = False
        
        # Find out what lies ahead by calling the world_get_cell function
        
        ahead_row = self.row
        ahead_col = self.col
        
        if self.direction == 'North':
            ahead_row = ahead_row - 1 
        elif self.direction == 'South':
            ahead_row = ahead_row + 1 
        elif self.direction == 'East':
            ahead_col = ahead_col + 1 
        elif self.direction == 'West':
            ahead_col = ahead_col - 1 
        ahead_value = world.get_cell(ahead_row, ahead_col)


        # Continue to execute the creature's instructions until a "hop" instruction is reached
        while not finished:
            next_op = self.dna[self.next_instruction]
            op = next_op.split()
            
            ################## GO #########################2
            if op[0] == 'go':
                self.next_instruction = int(op[1])
            ################## HOP #########################3
            if op[0] == 'hop':
                if ahead_value == 'EMPTY':
                    self.row = ahead_row
                    self.col = ahead_col
                self.next_instruction = self.next_instruction + 1
                finished = True
                
            ################ REVERSE #######################
            #reverses the direction of the creature
            if op[0] == "reverse":
                if self.direction == 'North':
                    self.direction = 'South'
                elif self.direction == 'South':
                    self.direction = 'North'
                elif self.direction == 'East':
                    self.direction = 'West'
                elif self.direction == 'West':
                    self.direction = 'East' 
                    
                self.next_instruction += 1
                finished = True
             
            ################ IFNOTWALL ################
            #perform specified action if creature not infront of wall
            if op[0] == "ifnotwall":
                if ahead_value != "WALL":
                    self.next_instruction = int(op[1])
                else:
                    self.next_instruction += 1
               
            ################ TWIST ################
            #changes the direction of the creature by 90 degrees
            if op[0] == "twist":
                if self.direction == 'North':
                    self.direction = 'East'
                elif self.direction == 'East':
                    self.direction = 'South'
                elif self.direction == 'South':
                    self.direction = 'West'
                elif self.direction == 'West':
                    self.direction = 'North'
                self.next_instruction += 1
                finished = True
            
            ################ IFSAME & IFENEMY################
            #if the creature had the operation ifsame, and the creature ahead is the same
            #it will perform a certain action at X
            if op[0] == "ifsame":
                species = self.get_species()
                x_pos = self.row
                y_pos = self.col
            
                if ahead_value == "EMPTY" or ahead_value == "WALL":
                    self.next_instruction += 1
                else:
                    if ahead_value.get_species() == species:
                        self.next_instruction = int(op[1])
                    else:
                        self.next_instruction += 1
                    
            #if the creature had the operation ifenemy, and the creature ahead is an
            #enemy i.e not the same species, it will preform X operator
            if op[0] == "ifenemy":
                species = self.get_species()
                x_pos = self.row
                y_pos = self.col
            
                if ahead_value == "EMPTY" or ahead_value == "WALL":
                    self.next_instruction += 1
                else:
                    if ahead_value.get_species() != species:
                        self.next_instruction = int(op[1])
                    else:
                        self.next_instruction += 1
                    
            ############ IFRANDOM ###########
            # Calls thepseudo random function in the world class to generate a number between 0 or 1
            if op[0] == "ifrandom":
                if world.pseudo_random() == 1:
                    self.next_instruction = int(op[1])
                else:
                    self.next_instruction += 1
                    
            ############# infect #############
            #This instruction take the creature that is next to it and turn it into the same species as itself
            if op[0] == "infect":
                for creatures in world.creature_list:
                    if creatures == ahead_value:
                        creatures.dna = self.dna
                        
                self.next_instruction += 1
                finished = True
                    
            


## This class represents the grid-based world
class World:

    ## The world stores its grid-size, and the number of generations to be executed.  It also stores a creature. 4
    def __init__(self, size, max_generations):
        self.size = size
        self.generation = 0
        self.max_generations = max_generations
        self.creature = None  #5
        self.creature_list = []

    ## Adds a creature to the world
    def add_creature(self, c):
        self.creature_list.append(c)

    ## Gets the contents of the specified cell.  This could be 'WALL' if the cell is off the grid
    ## or 'EMPTY' if the cell is unoccupied
    def get_cell(self, row, col):
        if len(self.creature_list) > 1:
            for creatures in self.creature_list:
                if creatures.row == row and creatures.col == col:
                    return creatures
        if row <= 0 or col <= 0 or row >= self.size + 1 or col >= self.size + 1:
            return 'WALL'            
        return 'EMPTY'

    ## Executes one generation for the world - the creature moves once.  If there are no more
    ## generations to simulate, the world is printed
    def simulate(self):
        if self.generation < self.max_generations:
            for creature in self.creature_list:
                self.creature = creature
                self.creature.make_move(self)
            self.generation += 1
            return False
        else:
            print(self)
            return True

    ## Returns a string representation of the world
    def __str__(self):
        string = str(self.size)
        creature_count = {}
        list_creatures = []
        names_list = []
        
        #Loops through the list of creatures
        for creatures in self.creature_list:
            name = creatures.get_species()
            if name not in creature_count:
                creature_count[name] = 1
            else:
                creature_count[name] += 1
        for names in creature_count:
            names_list += [names]
            
        for names in names_list:
            name_count = (str(names), int(creature_count[names]))
            list_creatures += [tuple(name_count)]
            
        #This sorts the tuple list based on number and then alphabetical
        #This works due to the fact that lists and tuples comparison happens in order i.e, compare the first element; if not equal then the second element
        list_creatures = sorted(list_creatures, key = lambda x: (-x[1], x[0]))
        
        string += "\n" + str(list_creatures)
        
        for creatures in self.creature_list:
            string += "\n" + str(creatures)
        
        
        return string

    ## Display the world by drawing the creature, and placing a grid around it
    def draw(self):

        # Basic coordinates of grid within 800x800 window - total width and position of top left corner
        grid_width = 700
        top_left_x = -350
        top_left_y = 350
        grid_size = grid_width / self.size

        # Draw the creature
        for creature in self.creature_list:
            self.creature = creature
            self.creature.draw(grid_size, top_left_x, top_left_y)

        # Draw the bounding box
        turtle.goto(top_left_x, top_left_y)
        turtle.setheading(0)
        turtle.pendown()
        for i in range(0, 4):
            turtle.rt(90)
            turtle.forward(grid_width)
        turtle.penup()

        # Draw rows
        for i in range(self.size):
            turtle.setheading(90)
            turtle.goto(top_left_x, top_left_y - grid_size*i)
            turtle.pendown()
            turtle.forward(grid_width)
            turtle.penup()

        # Draw columns
        for i in range(self.size):
            turtle.setheading(180)
            turtle.goto(top_left_x + grid_size*i, top_left_y)
            turtle.pendown()
            turtle.forward(grid_width)
            turtle.penup()
            
    # Generates a random number based on the position of the creatures and current world generation
    def pseudo_random(self):
        string_total = 0
        for creature in self.creature_list:
            string_total += creature.row
            string_total += creature.col
            
        string_total = string_total * self.generation
        string_total = str(string_total)
        
        return int(hashlib.sha256(string_total.encode()).hexdigest(), 16) % 2

## This class reads the data files from disk and sets up the window
class CreatureWorld:

    ## Initialises the window, and registers the begin_simulation function to be called when the space-bar is pressed
    def __init__(self):
        self.framework = SimulationFramework(800, 800, 'COMPSCI 130 Project Two')
        self.framework.add_key_action(self.begin_simulation, ' ')
        self.framework.add_tick_action(self.next_turn, 100) # Delay between animation "ticks" - smaller is faster.

    ## Starts the animation
    def begin_simulation(self):
        self.framework.start_simulation()

    ## Ends the animation
    def end_simulation(self):
        self.framework.stop_simulation()

    ## Reads the data files from disk
    def setup_simulation(self):
        
        ## If new creatures are defined, they should be added to this list: #6
        all_creatures = ['Hopper', 'Parry', 'Rook', "Roomber", "Randy", "Flytrap", "Roamer", "Drunk", "Civilian", "Bat", "Gambler"]        

        # Read the creature location data
        with open('world_input.txt') as f:
            world_data = f.read().splitlines()
        

        # Read the dna data for each creature type
        dna_dict = {}
        for creature in all_creatures:
            with open('Creatures//' + creature + '.txt') as f:
                dna_dict[creature] = f.read().splitlines()
                

        # Create a world of the specified size, and set the number of generations to be performed when the simulation runs
        world_size = world_data[0]
        world_generations = world_data[1]
        self.world = World(int(world_size), int(world_generations))
        creatures = world_data[2:]
        list_location = []
        unique_locations = []
        unique_index = []
        
        for i in range(len(creatures)):
            creatures[i] = creatures[i].split()
        
        #adds the location of all the creatures into a list
        for data in creatures:
            list_location.append(tuple([int(data[1]), int(data[2])]))
            
        #checks if the location of a creature is unique, if it is, the index and location are stored in sep lists
        for cord in list_location:
            if cord not in unique_locations:
                unique_locations.append(cord)
        for cord in unique_locations:
            unique_index.append(list_location.index(cord))
        for i in unique_index:
            self.world.add_creature(Creature(int(creatures[i][1]), int(creatures[i][2]), dna_dict[creatures[i][0]], creatures[i][3]))

        # Draw the initial layout of the world
        self.world.draw()

    ## This function is called each time the animation loop "ticks".  The screen should be redrawn each time.         
    def next_turn(self):
        turtle.clear()
        self.world.draw() 
        if self.world.simulate():
            self.end_simulation()

    ## This function sets up the simulation and starts the animation loop
    def start(self):
        self.setup_simulation() 
        turtle.mainloop() # Must appear last.


## This is the simulation framework - it does not need to be edited
class SimulationFramework:

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.simulation_running = False
        self.tick = None #function to call for each animation cycle
        self.delay = 100 #default is .1 second.       
        turtle.title(title) #title for the window
        turtle.setup(width, height) #set window display
        turtle.hideturtle() #prevent turtle appearance
        turtle.tracer(False) #prevent turtle animation
        turtle.listen() #set window focus to the turtle window
        turtle.mode('logo') #set 0 direction as straight up
        turtle.penup() #don't draw anything
        self.__animation_loop()
        
    def start_simulation(self):
        self.simulation_running = True
        
    def stop_simulation(self):
        self.simulation_running = False

    def add_key_action(self, func, key):
        turtle.onkeypress(func, key)

    def add_tick_action(self, func, delay):
        self.tick = func
        self.delay = delay

    def __animation_loop(self):
        if self.simulation_running:
            self.tick()
        turtle.ontimer(self.__animation_loop, self.delay)
   
cw = CreatureWorld()
cw.start()
