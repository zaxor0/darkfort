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

# MAIN FUNCTION
def main() :
  player, playerWeapon, room = gameStart()
  roomCount = 0
  print('starting room',room,'count',roomCount)
  while True:
    #clear()
    print("----------")
    print('next room',room,'count',roomCount)
    print(room.doorPlacement)
    print(player.name,':','HP:',player.hitPoints,'| Coordinates:',player.xPos, player.yPos)
    player, room = playerInput(player, room)
    if room not in roomsExplored:
      roomsExplored.append(room)
      roomCount += 1
    else:
      print('returning to a room you have visited',room.xPos, room.yPos)

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


class Room:
  def __init__(self, roomNumber, xPos, yPos, shape, item, monster, scroll, doors, doorPlacement):
    self.roomNumber = roomNumber
    self.xPos = xPos
    self.yPos = yPos
    self.shape = shape
    self.item = item
    self.monster = monster
    self.scroll = scroll
    self.doors = doors
    self.doorPlacement = doorPlacement

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

  def entranceDescription(self):
    message = '\nFrom the southern door, you enter a ' + self.shape + ' room with ' + self.doors
    if self.scroll:
      message = message + ' and a dying mystic gives you a scroll of ' + self.scroll
    elif self.item:
      message = message + ' and a' + self.item + ' lays on the floor'
    elif self.monster:
      message = message + ' and here a ' + self.monster + ' stands guard, it attacks!'
    else:
      message = message + ' and the room is quite empty.'
    return message

  def entrance():
    entranceContents = ['item','monster','scroll','empty']
    roomNumber = 1
    xPos = 0
    yPos = 0
    item = ''
    monster = ''
    scroll = ''
    doors = doorCount[diceRoll(1,4)]
    oppositeDoor = 'south'
    doorPlacement = Room.doorPlacements(doors, oppositeDoor) 
    shape = roomShapes[diceRoll(2, 6)]
    contentsRoll = int(diceRoll(1, 4) - 1)
    entranceResult = entranceContents[contentsRoll]
    if entranceResult == 'item':
      itemRoll = int(diceRoll(1,6) - 1)
      item = sorted(items)[itemRoll]
      if item == 'Weapon': 
         item = Weapon.randomWeapon()[0]
    if entranceResult == 'monster':
      monsterRoll = int(diceRoll(1,4) - 1)
      monster = sorted(weakMonsters)[monsterRoll]
    if entranceResult == 'scroll':
      scrollRoll = int(diceRoll(1,4) - 1)
      scroll = sorted(scrolls)[scrollRoll]
    return 1, 0, 0, shape, item, monster, scroll, doors, doorPlacement

  def randomRoom(player, oppositeDoor):
    xPos = player.xPos
    yPos = player.yPos
    item = ''
    monster = ''
    scroll = ''
    doors = doorCount[diceRoll(1,4)]
    shape = roomShapes[diceRoll(2, 6)]
    doorPlacement = Room.doorPlacements(doors, oppositeDoor) 
    roomFeature = roomTable[diceRoll(1,6 -1)]
    print(xPos, yPos, shape, item, monster, scroll, doors, doorPlacement)
    return 2, xPos, yPos, shape, item, monster, scroll, doors, doorPlacement

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
  print(startingRoom.entranceDescription())
  return player, playerWeapon, startingRoom
 

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
  elif moved:
    explored = False
    for oldRoom in roomsExplored:
      if oldRoom.xPos == player.xPos and oldRoom.yPos == player.yPos:
        explored = True
        nextRoom = oldRoom
    if explored == True:
      room = nextRoom
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
