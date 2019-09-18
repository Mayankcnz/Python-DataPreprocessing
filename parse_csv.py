import csv 
import re
import random
import numpy as np
from decimal import *

def main():
	with open('Merged-Challenge.csv', 'r', encoding = "ISO-8859-1") as csv_file:
		csv_reader = csv.DictReader(csv_file)
	

		with open('final.csv', 'w', newline='',encoding = "ISO-8859-1") as new_file:
			#fieldnames = ['X','Y','OBJECTID','name','introduction','difficulty','completionTime','hasAlerts', 'introductionThumbnail', 'walkingAndTrampingWebPage','dateLoadedToGIS']
			#fieldnames2 = ['OBJECTID','name','introduction','difficulty', 'completionTime', 'hasAlerts', 'introductionThumbnail', 'walkingAndTrampingWebPage', 'dateLoadedToGIS', 'Shape__Length']
			final_FieldNames = ['X','Y','name','difficulty', 'completionTime','Shape__Length']
			csv_writer = csv.DictWriter(new_file,fieldnames=final_FieldNames, delimiter=',')
			csv_writer.writeheader()

			for line in csv_reader:

				item = line['completionTime']
				difficulty = line['difficulty']
				name = line['name']
				modifiedName = re.sub(r'\'', '', name)
				res = re.findall(r'\d*\.?\d+',item) # extract only integers to a list
				new = "".join([w for w in item if not w.isdigit()]) # extract only words
				tes = re.sub(r'[,]+',' ,',new)
				testing = re.sub(r'\b(?!hr|min|days|one|way|return|under|or|hours|minutes|m)\b\S+', '', tes)
				result = list(filter(None, re.split(r"[^-\|\,a-zA-Z]+",testing))) # split by spaces

				computedTime = 0

				if len(res) != 0 and len(result) != 0:
						computedTime = parseTime(res, result)

				
				line['completionTime'] = computedTime
				line['name'] = modifiedName
				csv_writer.writerow(line)

def parseTime(res, result):

	'''
	print('cuming')
	if not any(x in result for x in [',', '|','or','-']):
		if len(res) > 1 or len(result) >1:
			print('yoza')
		computedTime = doConversion(res, 0, result, 0, [0]*len(result))
		return computedTime
	'''	

	first_Counter = 0
	array = [0]*4
	counter = 0
	computedTime = 0
	timeCounter = 0
	flag = True
	last = ''
	for index, i in enumerate(result):

		if  (result[first_Counter] == '-' or result[first_Counter] == 'to') and flag == True:
			computedTime = 	calculateTime(res[timeCounter], result[first_Counter+1])
			computedTime2 = calculateTime(res[timeCounter+1], result[first_Counter+1])
			flag = False
			difference = abs(computedTime-computedTime2)
			timeCounter = timeCounter+2
			array[counter] = computedTime+(difference/2)
		elif i == ',' or i == '|' or i == 'or':
			first_Counter = index+1
			flag = True
			counter = counter + 1
		elif i == 'way':
			array[counter] = array[counter] * 2
		elif flag == True and (i == 'hr' or i == 'hrs' or i == 'days' or i == 'hours' or i == 'min' or i == 'minutes' or i == 'm'):
			computedTime = calculateTime(res[timeCounter], result[index])
			array[counter] = array[counter] + computedTime
			timeCounter = timeCounter + 1

		if (last == '-' or last == 'to') and flag == True:
			first = array[counter] - computedTime
			difference = abs(first-computedTime)
			array[counter] = first+(difference/2)

		last = result[index]

	return sum(array)



def calculateTime(time, type):

	if type == 'hr' or type == 'hrs' or type == 'hours':
		return Decimal(time) * 60
	elif type == 'days':
		return (Decimal(time) * 8) * 60
	elif type == 'min' or type == 'm' or type == 'minutes':
		return Decimal(time)
	else:
		return 0


if __name__=='__main__':
	main()






	

