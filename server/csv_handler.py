from prettytable import from_csv
import csv,shutil
from os import path
import os


def add(ip,port):
	csv_columns = ['IP','Port']
	csv_file = "active_hosts.csv"
	
	if path.exists(csv_file):
		csvfile = open(csv_file, 'a',newline='')
		hostwriter = csv.DictWriter(csvfile, fieldnames=csv_columns)
		hostwriter.writerow({'IP':ip,'Port':port})

	else:
		csvfile = open(csv_file, 'w',newline='')
		hostwriter = csv.DictWriter(csvfile, fieldnames=csv_columns)
		hostwriter.writeheader()
		hostwriter.writerow({'IP':ip,'Port':port})

def remove(ip,port):
	fieldnames = ['IP', 'Port']
	with open('active_hosts.csv') as csvfile, open('output.csv', 'w',newline='') as outputfile:
		reader = csv.DictReader(csvfile, fieldnames=fieldnames)
		writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
		for row in reader:
			if ip != row['IP'] or port != row['Port']:
					writer.writerow({'IP': row['IP'], 'Port': row['Port']})
	shutil.move('output.csv','active_hosts.csv')

def clear():
	csv_file = "active_hosts.csv"
	if path.exists(csv_file):
		os.remove(csv_file)
	
def view():
	with open('active_hosts.csv', 'r') as fp: 
	    x = from_csv(fp)
	print(x)

