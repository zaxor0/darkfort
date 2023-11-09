#!/usr/bin/python3

import random
import textwrap
import time

def main() :
  gameStart()

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
  'null', 'Oval', 'Irregular Cave', 'Cross-shaped', 'Corridor','Square',
  'Square', 'Square', 'Round', 'Rectangular', 'Triangular', 'Skull-shaped'
  ]

doorCount = [ 'no doors, a dead end', 'one door', 'two doors', 'two doors', 'three doors']
doorPosition = [ 'North', 'South', 'East', 'West' ]

# standard weapon stats
class Player:
  def __init__(self,name):
    self.name = name
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
  def __init__(self, roomNumber, xPos, yPos, item, monster, scroll, doors):
    self.roomNumber = roomNumber
    self.xPos = xPos
    self.yPos = yPos
    self.item = item
    self.monster = monster
    self.scroll = scroll
    self.doors = doors

  def entranceDescription(self):
    message = '\nYou enter a room with ' + self.doors
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
    return 1, 0, 0, item, monster, scroll, doors

  def randomRoom():
    print('testing')

def gameStart() : 
  # starting screen
  print(startMessage)
  # create player
  player = Player('Kargunt')
  print('Your name is Kargrunt. You begin with',player.hitPoints,'hit points (hp)\nand',player.silver,'silver. You may carry unlimited items.')
  playerWeapon = Weapon.randomWeapon()
  player_weapon = Weapon(playerWeapon[0], playerWeapon[1], playerWeapon[2], playerWeapon[3])
  print('\nYour weapon is a',player_weapon.name, ', it attacks with a +', player_weapon.attackBonus,'and deals d',player_weapon.damageDie,'damage')
  startingRoom = Room.entrance() 
  starting_room = Room(startingRoom[0],startingRoom[1],startingRoom[2],startingRoom[3],startingRoom[4],startingRoom[5],startingRoom[6]) 
  print(starting_room.entranceDescription())
 
 

def diceRoll(dieCount,dieSides):
  dieTotal = 0
  for i in range(0,dieCount):
    min = 1
    max = dieSides
    dieVal = random.randint(min,max)
    dieTotal += dieVal
  return(dieTotal)

main()
