#!/usr/bin/python3

import getch
import os
import random
import sys
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
  'BLOOD-DRENCHED SKELETON' : { 'points' : 3, 'dmgDie' : 4, 'hp' : 6 , 'loot' : 'dagger', 'lootChance' : 6 },
  'CATACOMB CULTIST' : { 'points' : 3, 'dmgDie' : 4, 'hp' : 6 , 'loot' : 'scroll', 'lootChance' : 2 },
  'GOBLIN' : { 'points' : 3, 'dmgDie' : 4, 'hp' : 5, 'loot' : 'rope', 'lootChance' : 2 },
  'UNDEAD HOUND' : { 'points' : 3, 'dmgDie' : 4, 'hp' : 6, 'loot' : 'none', 'lootChance' : 0 }
  }

roomShapes = [ 
  'null', 'irregular cave', 'oval', 'cross-shaped', 'corridor','square',
  'square', 'square', 'round', 'rectangular', 'triangular', 'skull-shaped'
  ]

doorCount = [ 'no doors, a dead end', 'one door', 'two doors', 'two doors', 'three doors']

doorPosition = [ 'north', 'south', 'east', 'west' ]

entranceEncounters = ['item','weak monster','scroll','empty']

roomEncounters = [ 'nothing', 'pit trap', 'riddling soothsayer', 'weak monster', 'tough monster', 'peddler from beyond the void' ]

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
  clear()
  player, playerWeapon, room = gameStart()
  roomsExplored.append(room)
  roomCount = 0
  print('\n...press any key to continue...')
  anyKey = getch.getch()
  while True:
    clear()
    print(' ###  DARK FORT ### \n')
    print(player.name,' : ',' HP: ',player.hitPoints,' | Coordinates: ',player.xPos, player.yPos,'\n')
    slowPrint('You enter a ',room.shape,' shaped room ',room.roomName,'\n')
    slowPrint('You encounter a ',str(room.encounter),' \nthere are doors to the:')
    print(room.doorPlacement)
    printRoom(room)
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

class Monster:
  #weakMonsters = {
  #  'BLOOD-DRENCHED SKELETON' : { 'points' : 3, 'dmgDie' : '4', 'hp' : 6 , 'loot' : 'dagger', 'lootChance' : 2 },
  #  'CATACOMB CULTIST' : { 'points' : 3, 'dmgDie' : '4', 'hp' : 6 , 'loot' : 'scroll', 'lootChance' : 2},
  #  'GOBLIN' : { 'points' : 3, 'dmgDie' : '4', 'hp' : 5, 'loot' : 'rope', 'lootChance' : 2},
  #  'UNDEAD HOUND' : { 'points' : 3, 'dmgDie' : '4', 'hp' : 6, 'loot' : 'none'}
  #  }
  def __init__(self, name, points, damageDie, hp, loot, lootChance):
    self.name = name
    self.points = points
    self.damageDie = damageDie
    self.hp = hp
    self.loot = loot
    self.lootChance = lootChance

class Room:
  def __init__(self, roomName, xPos, yPos, shape, doors, doorPlacement, encounter):
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

  def randomRoom(player, oppositeDoor):
    xPos = player.xPos
    yPos = player.yPos
    # if entrance at 0,0
    if xPos == 0 and yPos == 0:
      roomName = '"dark fort entrance"'
      encounter = entranceEncounters[int(diceRoll(1, 4) - 1)]
      shape = 'square'
    # if other rooms
    else:
      roomName = str('"' + roomDescriptor[diceRoll(1,25) - 1] + ' ' + roomType[diceRoll(1,25) - 1] + '"')
      encounter = roomEncounters[diceRoll(1,6 - 1)]
      shape = roomShapes[diceRoll(2, 6) - 1]
    encounter = Room.encounterSelect(encounter)
    doors = doorCount[diceRoll(1,4)]
    doorPlacement = Room.doorPlacements(doors, oppositeDoor) 
    #encounter = Room.encounterSelect() 
    return roomName, xPos, yPos, shape, doors, doorPlacement, encounter

  def encounterSelect(encounter):
    if encounter == 'weak monster':
      monsterRoll = diceRoll(1,4) - 1 
      monster = sorted(weakMonsters)[monsterRoll]
#      monster = Monster(monster, weakMonsters[monster]['points'],weakMonsters[monster]['dmgDie'],weakMonsters[monster]['hp'],weakMonsters[monster]['loot'],weakMonsters[monster]['lootChance'])
      monster = Monster(monster,*weakMonsters[monster].values())
      return monster
    else:
      return encounter


  # need to add a function that if two rooms are newly connected its considered a secret door

def gameStart() : 
  # starting screen
  slowPrint(startMessage)
  # create player
  player = Player('Kargunt')
  # the * lets us expand the list of variables 
  playerWeapon = Weapon(*Weapon.randomWeapon())
  # create entrance room
  startingRoom = Room(*Room.randomRoom(player, 'south'))
  # print start details
  slowPrint('Your name is Kargrunt. You begin with ',str(player.hitPoints),' hit points (hp)\nand ',str(player.silver),' silver. You may carry unlimited items.')
  slowPrint('\nYour weapon is a ',str(playerWeapon.name), ', it attacks with a +', str(playerWeapon.attackBonus),' and deals d',str(playerWeapon.damageDie),' damage')
  return player, playerWeapon, startingRoom
 
def printRoom(room):
  # room shapes 
  # irregular cave oval cross-shaped corridor square round rectangular triangular skull-shaped
  if room.shape == 'corridor': 
    top="\n\n  +------------+ "
    mid="\n  |............| "
    btm="\n  +------------+ \n"
    if 'east' in room.doorPlacement and not 'west' in room.doorPlacement:
      mid="\n  |............[] "
    if 'west' in room.doorPlacement and not 'east' in room.doorPlacement:
      mid="\n []............|  "
    if 'west' in room.doorPlacement and 'east' in room.doorPlacement:
      mid="\n []............[] "
    if 'north' in room.doorPlacement:
      top="\n  +----[--]----+ "
    if 'south' in room.doorPlacement:
      btm="\n  +----[--]----+ \n\n"
  elif room.shape == 'rectangular': 
    top="\n  +----------------+ "
    mid="\n  |                | \n  |                | \n  |                | "
    btm="\n  +----------------+ \n"
    if 'east' in room.doorPlacement and not 'west' in room.doorPlacement:
      mid="\n  |                | \n  |                [] \n  |                | "
    if 'west' in room.doorPlacement and not 'east' in room.doorPlacement:
      mid="\n  |                | \n []                | \n  |                | "
    if 'west' in room.doorPlacement and 'east' in room.doorPlacement:
      mid="\n  |                | \n []                [] \n  |                | "
    if 'north' in room.doorPlacement:
      top="\n  +------[--]------+ "
    if 'south' in room.doorPlacement:
      btm="\n  +------[--]------+ \n"
  elif room.shape == 'cross-shaped': 
    top="\n        +------+\n        |      |\n        |      |"
    mid="\n  +-----+      +-----+\n  |                  |\n  |                  |\n  |                  |\n  +-----+      +-----+ "
    btm="\n        |      |\n        |      |\n        +------+ \n"
    if 'east' in room.doorPlacement and not 'west' in room.doorPlacement:
      mid="\n  +-----+      +-----+\n  |                  |\n  |                  []\n  |                  |\n  +-----+      +-----+ "
    if 'west' in room.doorPlacement and not 'east' in room.doorPlacement:
      mid="\n  +-----+      +-----+\n  |                  |\n []                  |\n  |                  |\n  +-----+      +-----+ "
    if 'west' in room.doorPlacement and 'east' in room.doorPlacement:
      mid="\n  +-----+      +-----+\n  |                  |\n []                  []\n  |                  |\n  +-----+      +-----+ "
    if 'north' in room.doorPlacement:
      top="\n        +-[--]-+\n        |      |\n        |      |"
    if 'south' in room.doorPlacement:
      btm="\n        |      |\n        |      |\n        +-[--]-+ \n"
  elif room.shape == 'triangular': 
    top="\n       +----+ \n       /    \ "
    mid="\n      /      \ \n     /        \  \n    /          \ "
    btm="\n   /            \ \n  +--------------+ \n"
    if 'east' in room.doorPlacement and not 'west' in room.doorPlacement:
      mid="\n      /      \ \n     /        []  \n    /          \ "
    if 'west' in room.doorPlacement and not 'east' in room.doorPlacement:
      mid="\n      /      \ \n    []        \  \n    /          \ "
    if 'west' in room.doorPlacement and 'east' in room.doorPlacement:
      mid="\n      /      \ \n    []        [] \n    /          \ "
    if 'north' in room.doorPlacement:
      top="\n       +[--]+ \n       /    \ "
    if 'south' in room.doorPlacement:
      btm="\n   /            \ \n  +-----[--]-----+ \n"
  elif room.shape == 'oval': 
    top="\n     +----------+ \n    /            \ "
    mid="\n   |              | " 
    btm="\n    \            / \n     +----------+  \n"
    if 'east' in room.doorPlacement and not 'west' in room.doorPlacement:
      mid="\n   |             [] " 
    if 'west' in room.doorPlacement and not 'east' in room.doorPlacement:
      mid="\n   []             | " 
    if 'west' in room.doorPlacement and 'east' in room.doorPlacement:
      mid="\n   []            [] " 
    if 'north' in room.doorPlacement:
      top="\n     +---[--]---+ \n    /            \ "
    if 'south' in room.doorPlacement:
      btm="\n    \            / \n     +---[--]---+  \n"
  else:
    top="\n  +----------+ "
    mid="\n  |..........| \n  |..........| \n  |..........| "
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
  slowPrint(printedRoom)

def diceRoll(dieCount,dieSides):
  dieTotal = 0
  for i in range(0,dieCount):
    min = 1
    max = dieSides
    dieVal = random.randint(min,max)
    dieTotal += dieVal
  return(dieTotal)

def menu(key, player, room):
  if key == chr(27):
    quitYes = input('\nDo you really want to quit? ')
    if quitYes in yesses:
      exit()
    else:
      print('Congratulations, you are no coward!')
  return player, room

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

# slow printing function, like Alien (1979)
def slowPrint(*text):
  for word in text:
    for letter in word:
      sys.stdout.write(letter)
      sys.stdout.flush()
      time.sleep(.02)

main()
