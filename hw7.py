#!/usr/bin/env python3
from pymongo import MongoClient
import numpy as np
from random import randint

client = MongoClient()
db = client.ngv
coll = db.cities

def pointOfInterestQuestion(list):
  inputPointsOfInterest = input('Any points of interest? (y/n) ')

  while inputPointsOfInterest != 'n':
    if inputPointsOfInterest == 'y':
      interestName = input('Enter name: ')
      interesAddress = input('Enter address: ')

      list.append([interestName, interesAddress])

    elif inputPointsOfInterest != 'n':
      print("Invalid input...")

    if inputPointsOfInterest != 'n':
      inputPointsOfInterest = input('Any points of interest? (y/n) ')

  return list

print('Our Travel database\n')

userEnter = input('Enter i to insert, f to find, q to quit: ')

while userEnter != 'q':
  if userEnter == 'i':
    cityName = input('Enter city name: ')
    stateName = input('Enter state: ')

    update = True
    targetName = coll.find_one( {'city': cityName, 'state': stateName}, {'_id': 0, 'interests': 1} )
    #print(targetName)

    if targetName == None:
      update = False

    interestList = []
    if targetName != None:
      for mat in targetName["interests"]:
        interestList.append([mat[0], mat[1]])

    interestList = pointOfInterestQuestion(interestList)
    #print(interestList)

    if update == False:
      city = {
        'city': cityName,
        'state': stateName,
        'interests': interestList
      }
      #print(city)

      coll.insert_one(city)
    else:
      coll.update_one({'city': cityName, 'state': stateName}, {'$set': {'interests': interestList}})

  elif userEnter == 'f':
    cityName = input('Enter city name: ')
    stateName = input('Enter state: ')

    #cityName = 'Hayward'
    #stateName = 'CA'

    print('Points of interest:')

    targetName = coll.find_one( {'city': cityName, 'state': stateName}, {'_id': 0, 'interests': 1} )

    #if targetName != None:
      #print(len(targetName))

    if targetName != None:
      for mat in targetName["interests"]:
        print(mat[0] , ':', mat[1])
    else:
      print(cityName, ',', stateName, 'not found in database')

  else:
    print("Invalid input...")

  # ask new input
  if userEnter != 'q':
    userEnter = input('Enter i to insert, f to find, q to quit: ')

#coll.find_one( {'city': 'Hayward'} )
