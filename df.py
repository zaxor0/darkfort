#!/usr/bin/python3

import getch
import os
import random
import textwrap
import time

clear = lambda: os.system('clear')

def main() :
  player, playerWeapon, startingRoom = gameStart()
  action, player = playerInput(player)
  print(action)
  while True:
   # clear()
    action, player = playerInput(player)
    print(action)
    # get player input, usually directional change

# variables
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
  'null', 'oval', 'irregular cave', 'cross-shaped', 'corridor','square',
  'square', 'square', 'round', 'rectangular', 'triangular', 'skull-shaped'
  ]

doorCount = [ 'no doors, a dead end', 'one door', 'two doors', 'two doors', 'three doors']
doorPosition = [ 'North', 'South', 'East', 'West' ]

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
  def __init__(self, roomNumber, xPos, yPos, shape, item, monster, scroll, doors):
    self.roomNumber = roomNumber
    self.xPos = xPos
    self.yPos = yPos
    self.shape = shape
    self.item = item
    self.monster = monster
    self.scroll = scroll
    self.doors = doors

  def entranceDescription(self):
    message = '\nYou enter a ' + self.shape + ' room with ' + self.doors
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
    shapeRoll = diceRoll(2, 6)
    shape = roomShapes[shapeRoll]
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
    return 1, 0, 0, shape, item, monster, scroll, doors

  def randomRoom():
    print('testing')

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


def menu(key):
  if key == chr(27):
    clear()
    quitYes = input('Do you really want to quit? ')
    if quitYes in yesses:
      exit()
    else:
      status = 'Congratulations, you are no coward!'
  return status

def movement(direction, player):
  print('in movement', direction)
  # move north
  if direction == 'w':
    print('move north')
    player.yPos += 1
    status = 'Moved North'
  # move south
  if direction == 's':
    player.yPos -= 1
    status = 'Moved South'
  # move east
  if direction == 'd':
    player.xPos += 1
    status = 'Moved East'
  elif direction == 'd':
    player.xPos += 1
    status = 'Moved South East'
  # move west
  if direction == 'a':
    player.xPos -= 1
    status = 'Moved West'
  coordinates = str(player.xPos) + ',' + str(player.yPos)
  status = status + ' : ' + coordinates
  return status, player

def spells(spellNum):
  if spellNum == '1':
    print('CAST MAGIC MISSILE')

def playerInput(player):
  playerKey = getch.getch()
  actions = {
    menu : { chr(27), chr(28) },
    movement : { 'w','a','s','d' },
    spells : {'1','2' }
  }
  for actionType in actions:
    for key in actions[actionType]:
      if playerKey == key:
        status = actionType(key, player)
      #else:
      #  status = 'not a valid key'
  return status, player

main()
