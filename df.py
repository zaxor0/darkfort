#!/usr/bin/python3

import getch
import os
import random
import textwrap
import time

clear = lambda: os.system('clear')

# variables
global roomCount
roomsExplored = []

yesses = ['Yes','yes','Y','y','Ye','ye','ya','Ya','Yup','yup']

startMessage = "\n  This begins your perilous delve into the DARK FORT.\n\n     THE CATACOMB ROGUE enters the stage\n\n"

startingWeapons =  {
  'warhammer' : { 'damageDie' : 6, 'damageBonus' : 0, 'attackBonus' : 0 }, 
  'dagger' : { 'damageDie' : 4, 'damageBonus' : 0, 'attackBonus' : 1 },
  'sword' : { 'damageDie' : 6, 'damageBonus' : 0, 'attackBonus' : 1 },
  'flail' : { 'damageDie' : 6, 'damageBonus' : 1, 'attackBonus' : 0 }
  }

startingItems =  {
  'armor' : { 'damageReductionDie' : 4 },
  'potion' : { 'healingDie' : 6 },
  'scroll' : { 'power' : 'summon weak demon' },
  'cloak' : { 'type' : 'invisibility' }
  }

items = [ 'weapon', 'potion', 'rope', 'scroll', 'armor', 'cloak' ]

scrolls = [ 'Summon weak daemon', 'Palms Open the Southern Gate', 'Aegis of Sorrow', 'False Omen' ]

weakMonsters = {
  'BLOOD-DRENCHED SKELETON' : { 'points' : 3, 'dmgDie' : '4', 'hp' : 6 , 'loot' : 'dagger', 'lootChance' : 2 },
  'CATACOMB CULTIST' : { 'points' : 3, 'dmgDie' : '4', 'hp' : 6 , 'loot' : 'scroll', 'lootChance' : 2},
  'GOBLIN' : { 'points' : 3, 'dmgDie' : '4', 'hp' : 5, 'loot' : 'rope', 'lootChance' : 2},
  'UNDEAD HOUND' : { 'points' : 3, 'dmgDie' : '4', 'hp' : 6, 'loot' : 'none'}
  }

roomShapes = [ 
  'null', 'irregular cave', 'oval', 'cross-shaped', 'corridor','square',
  'square', 'square', 'round', 'rectangular', 'triangular', 'skull-shaped'
  ]

doorCount = [ 'no doors, a dead end', 'one door', 'two doors', 'two doors', 'three doors']

doorPosition = [ 'north', 'south', 'east', 'west' ]

roomTable = [ 'nothing', 'pit trap', 'riddling soothsayer', 'weak monster', 'tough monster', 'peddler from beyond the void' ]

roomType = [
  'armory','chapel','blacksmith','kitchen','altar room',
  'throne room','treasury','garbage pit','baths','library',
  'study','temple','shrine','quarters','barracks',
  'granary','great hall','chambers','well room','bedchamber',
  'workshop','commandant quarters','torture chamber','prison','cell block']

roomDescriptor = [
  'decrepit','foul','revered','unholy','filthy',
  'putrid','horrid','monstrous','stinking','vile',
  'disgraceful','contemptible','unworthy','detestable','ignoble',
  'blessed','divine','hallowed','revered','holy',
  'sacred','profane','exalted','grimy','nasty']

# MAIN FUNCTION
def main() :
  player, playerWeapon, room = gameStart()
  roomsExplored.append(room)
  roomCount = 0
  while True:
    clear()
    print('\n DARK FORT\n')
    printRoom(room)
    print('You have entered room',room.roomName,'you encounter a',room.encounter,'\nthere are doors to the',room.doorPlacement)
    print(player.name,':','HP:',player.hitPoints,'| Coordinates:',player.xPos, player.yPos)
    player, room = playerInput(player, room)
    if room not in roomsExplored:
      roomsExplored.append(room)
      roomCount += 1
    else:
      print('...returning to a room you have visited')

# standard weapon stats
class Player:
  def __init__(self,name):
    self.name = name
    self.xPos = 0 
    self.yPos = 0
    self.level = 1
    self.hitPoints = 15
    self.silver = 15 + diceRoll(1,6)
    items = []
    
  def levelPlayer():
    print('testing')

class Weapon:
  def __init__(self, name, damageDie, damageBonus, attackBonus):
    self.name = name
    self.damageDie = damageDie
    self.damageBonus = damageBonus
    self.attackBonus = attackBonus

  def randomWeapon():
    weaponRoll = int(diceRoll(1,4) - 1)
    weaponName = sorted(startingWeapons)[weaponRoll]
    weaponDamageDie = startingWeapons[weaponName]['damageDie']
    weaponDamageBonus = startingWeapons[weaponName]['damageBonus']
    weaponAttacks = startingWeapons[weaponName]['attackBonus']
    return weaponName, weaponDamageDie, weaponDamageBonus, weaponAttacks

class encounter():
  def __init__(self, name):
    self.name = name
  #if entranceResult == 'item':
  #  itemRoll = int(diceRoll(1,6) - 1)
  #  item = sorted(items)[itemRoll]
  #  if item == 'Weapon': 
  #     item = Weapon.randomWeapon()[0]
  #if entranceResult == 'monster':
  #  monsterRoll = int(diceRoll(1,4) - 1)
  #  monster = sorted(weakMonsters)[monsterRoll]
  #if entranceResult == 'scroll':
  #  scrollRoll = int(diceRoll(1,4) - 1)
  #  scroll = sorted(scrolls)[scrollRoll]
#
#  def entranceDescription(self):
#    message = '\nFrom the southern door, you enter a ' + self.shape + ' room with ' + self.doors
#    if self.scroll:
#      message = message + ' and a dying mystic gives you a scroll of ' + self.scroll
#    elif self.item:
#      message = message + ' and a' + self.item + ' lays on the floor'
#    elif self.monster:
#      message = message + ' and here a ' + self.monster + ' stands guard, it attacks!'
#    else:
#      message = message + ' and the room is quite empty.'
#    return message



class Room:
  def __init__(self, roomNumber, roomName, xPos, yPos, shape, doors, doorPlacement, encounter):
    self.roomNumber = roomNumber
    self.roomName = roomName
    self.xPos = xPos
    self.yPos = yPos
    self.shape = shape
    self.doors = doors
    self.doorPlacement = doorPlacement
    self.encounter = encounter

  def doorPlacements(doors, oppositeDoor):
    numDoors = 0
    if doors == 'no doors, a dead end': return
    elif doors == 'one door': numDoors = 1
    elif doors == 'two doors': numDoors = 2
    elif doors == 'three doors': numDoors = 3
    directions = [ 'north', 'south', 'east', 'west' ]
    sides = [oppositeDoor]
    for i in range(numDoors):
      doorOnSide=False  
      while doorOnSide == False:
        position = diceRoll(1,4) - 1
        if directions[position] not in sides:
          doorOnSide = True
          sides.append(directions[position])
    return sides

  def entrance():
    entranceContents = ['item','monster','scroll','empty']
    roomNumber = 1
    xPos = 0
    yPos = 0
    doors = doorCount[diceRoll(1,4)]
    oppositeDoor = 'south'
    doorPlacement = Room.doorPlacements(doors, oppositeDoor) 
    shape = roomShapes[diceRoll(2, 6)]
    encounter = entranceContents[int(diceRoll(1, 4) - 1)]
    return 1, '"dark fort entrance"', 0, 0, shape, doors, doorPlacement, encounter 

  def randomRoom(player, oppositeDoor):
    roomName = str('"' + roomDescriptor[diceRoll(1,25) - 1] + ' ' + roomType[diceRoll(1,25) - 1] + '"')
    xPos = player.xPos
    yPos = player.yPos
    item = ''
    monster = ''
    scroll = ''
    doors = doorCount[diceRoll(1,4)]
    shape = roomShapes[diceRoll(2, 6)]
    doorPlacement = Room.doorPlacements(doors, oppositeDoor) 
    encounter = roomTable[diceRoll(1,6 - 1)]
    return 2, roomName, xPos, yPos, shape, doors, doorPlacement, encounter

  # need to add a function that if two rooms are newly connected its considered a secret door

def gameStart() : 
  # starting screen
  print(startMessage)
  # create player
  player = Player('Kargunt')
  # the * lets us expand the list of variables 
  playerWeapon = Weapon(*Weapon.randomWeapon())
  startingRoom = Room(*Room.entrance())
  # print start details
  print('Your name is Kargrunt. You begin with',player.hitPoints,'hit points (hp)\nand',player.silver,'silver. You may carry unlimited items.')
  print('\nYour weapon is a',playerWeapon.name, ', it attacks with a +', playerWeapon.attackBonus,'and deals d',playerWeapon.damageDie,'damage')
  return player, playerWeapon, startingRoom
 
def printRoom(room):
  top="\n  +----------+ "
  mid="\n  |          | \n  |          | \n  |          | "
  btm="\n  +----------+ \n"
  if 'east' in room.doorPlacement and not 'west' in room.doorPlacement:
    mid="\n  |          | \n  |          [] \n  |          | "
  if 'west' in room.doorPlacement and not 'east' in room.doorPlacement:
    mid="\n  |          | \n []          | \n  |          | "
  if 'west' in room.doorPlacement and 'east' in room.doorPlacement:
    mid="\n  |          | \n []          [] \n  |          | "
  if 'north' in room.doorPlacement:
    top="\n  +---[--]---+ "
  if 'south' in room.doorPlacement:
    btm="\n  +---[--]---+ \n"
  printedRoom = top + mid + btm
  print(printedRoom)

def diceRoll(dieCount,dieSides):
  dieTotal = 0
  for i in range(0,dieCount):
    min = 1
    max = dieSides
    dieVal = random.randint(min,max)
    dieTotal += dieVal
  return(dieTotal)

def menu(key, player):
  if key == chr(27):
    quitYes = input('\nDo you really want to quit? ')
    if quitYes in yesses:
      exit()
    else:
      print('Congratulations, you are no coward!')
  return player

def movement(direction, player, room):
  moved = False
  if direction == 'w' and 'north' in room.doorPlacement:
    player.yPos += 1
    oppositeDoor = 'south'
    moved = True
  if direction == 's' and 'south' in room.doorPlacement:
    player.yPos -= 1
    oppositeDoor = 'north'
    moved = True
  if direction == 'd' and 'east' in room.doorPlacement:
    player.xPos += 1
    oppositeDoor = 'west'
    moved = True
  if direction == 'a' and 'west' in room.doorPlacement:
    player.xPos -= 1
    oppositeDoor = 'east'
    moved = True
  if not moved:
    print('there is no door in that direction')
    print(room.doorPlacement)
  # after a logical movement / move through a door that exists
  elif moved:
    explored = False
    # check to see if the new X Y coordinates match those of an existing room
    for oldRoom in roomsExplored:
      # if the coordinates match an existing room, load up that room instead of creating a new one
      if oldRoom.xPos == player.xPos and oldRoom.yPos == player.yPos:
        explored = True
        nextRoom = oldRoom
    # loading "nextRoom" which is a previously explored room
    if explored == True:
      room = nextRoom
    # else, just make a whole new room
    else:
      room = Room(*Room.randomRoom(player, oppositeDoor))
  return player, room

def combat(player):
  print(player.name,'entering combat')
  return player

def combatActions(playerAction,player):
  if playerAction == 'c':
    combat(player)
  elif playerAction == 'f':
    fleeYes = input('\nOnly cowards flee, are you sure? ')
    if fleeYes in yesses:
      damage = diceRoll(1,4)
      print('The monster swipes at you for d4 damage! Dealing',damage)
      player.hitPoints = player.hitPoints - damage
  return player

def playerInput(player, room):
  playerKey = getch.getch()
  actions = {
    menu : { chr(27), chr(28) }, # 27 is escape
    movement : { 'w','a','s','d' },
    combatActions : { 'c','f' }
  }
  playerAction = ''
  for actionType in actions:
    for key in actions[actionType]:
      if playerKey == key:
        playerAction = actionType
  if not playerAction:
    print('invalid key')
  else:
    player, room = playerAction(playerKey, player, room)
  return player, room

main()
