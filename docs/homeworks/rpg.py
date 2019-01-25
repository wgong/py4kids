
def showInstructions():
  #print a main menu and the commands
  print('''
         RPG Game
Haunted House: the lost diamond
========
Game commands:
  go [direction]  # navigate in the house. for example: go south
  get [item]      # pick up something. for example: get hammer
  use [item]      # use something against an enemy. for example: use hammer
  exit            # exit the game
Game goal:
    Find the lost diamond.
''')

def showStatus():
  #print the player's current status
  print('---------------------------')
  print('You are in the ' + currentRoom)
  #print the current inventory
  print('Your Tressure Box : ' + str(inventory))
  #print an item if there is one
  if "item" in rooms[currentRoom]:
    print('You see a ' + str(rooms[currentRoom]['item']))
  #print any enemy in the room
  if "Enemy" in rooms[currentRoom]:
    print('You see a ' + str(rooms[currentRoom]['Enemy'][0]))
  print("---------------------------")

#an inventory, which is initially empty
inventory = []

#a dictionary linking a room to other rooms
rooms = {

            'Hall' : { 
                  'south' : 'Kitchen',
                  'west'  : 'Bedroom',
                  'east'  : 'Office',
                  'item' : ['key']
                },

            'Kitchen' : {
                  'north' : 'Hall',
                  'south' : 'Garden',
                  'east' :  'Bedroom',
                  'west' :  'Office',
                  'item' : ['kinef', 'plate'],
                  'Enemy' : ('A mouse in a box','hammer')               
                },
            'Bedroom' : { 
                  'west' : 'Kitchen',
                  'east' : 'Hall',
                  'item' : ['pillow']
                },
            'Office' : { 
                  'east' : 'Kitchen',
                  'west' : 'Hall'
                },
            'Garden' : {
                'north' : 'Kitchen',
                'south' : 'DogHouse',
                'item' : ['hammer']
                },
            'DogHouse' : {
                'north' : 'Garden',
                'Enemy' : ('Monster','')
                }
         }

#start the player in the Hall
currentRoom = 'Hall'

showInstructions()

#loop forever
while True:

  #showInstructions()   # turn this on will display instrucions every time after user input
  showStatus()
  
  if  "Enemy" in rooms[currentRoom]:
      if rooms[currentRoom]['Enemy'][0] == 'Monster':
          print('You are eaten by a Monster.\nGame is over. Good luck next time!')
          break

  #get the player's next 'move'
  
  move = ''
  # only leave the loop until the user has entered something
  while move == '':  
    move = input('>')
    
  #.split() breaks it up into an list array
  #eg typing 'go east' would give the list:
  #['go','east']
  move = move.lower().split()

  #if they type 'go' first
  if move[0] == 'go' and len(move) > 1:
    #check that they are allowed wherever they want to go
    if move[1] in rooms[currentRoom]:
      #set the current room to the new room
      currentRoom = rooms[currentRoom][move[1]]
    #there is no door (link) to the new room
    else:
        print('You can\'t go that way!')

  #if they type 'get' first
  if move[0] == 'get' and len(move) > 1:
    #if the room contains an item, and the item is the one they want to get
    if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
      #add the item to their inventory
      inventory.append(move[1])
      #display a helpful message
      print(move[1] + ' got!')
      #delete the item from the room
      rooms[currentRoom]['item'].remove(move[1])
      if len(rooms[currentRoom]['item']) == 0:
          del rooms[currentRoom]['item']
    #otherwise, if the item isn't there to get
    else:
      #tell them they can't get it
      print('Can\'t get ' + move[1] + '!')

  # if they type 'use' first
  if move[0] == 'use' and len(move) > 1:
    # check if the room contains  a enemy and
    # check enemy tuple to see if the item used is effective or not
    if 'Enemy' in rooms[currentRoom] and rooms[currentRoom]['Enemy'][1] == move[1]:
        print('Good Job! You just kill a %s' % rooms[currentRoom]['Enemy'][0])
        print('You just found a diamond in the box where the mouse hide!')
        inventory.append('Diamond')
    else:
        print('Sorry, use %s has no effect.' % move[1])
        
  # if input is 'exit'
  if move[0] == 'exit':
    if 'Diamond' in inventory:
        print('You found the diamond. You won!')
    else:
        print('You have not found the diamond. Mission aborted.')
    print('Game is over')
    break
          
print('------------------------')