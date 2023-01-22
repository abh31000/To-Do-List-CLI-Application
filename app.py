from rich.console import Console
from pick import pick
import pandas as pd
import csv, os, getpass


choice = '0'
console = Console()


def clean_screen():
	if(os.name == 'posix'):
		os.system('clear')
	else:
		os.system('cls')

def options_menu():
	title = 'Please choose an option'
	options = ['List Tasks','Add Task','Delete Task', 'Change Status', '(Exit)']
	option, index = pick(options, title, indicator='=>')

	return index

def list_tasks():
	fo = pd.read_csv("tasks.csv")
	states = fo['state']
	names = fo['name']

	if(len(names.tolist()) == 0):
		clean_screen()
		return

	console.print(" Your To Do List\n",justify="center")
	for i,j in zip(states, names):
		if(i == 0):
			console.print("	"+str(j), style="strike")
		else:
			console.print(f"	[b]{str(j)} ------ [i](completed)[/i][/b]")
	getpass.getpass("\n\n press enter to quit")
	clean_screen()

def add_task():
	task_name = input("\n   > ")

	if task_name == '':
		clean_screen()
		return

	task_list = [task_name, '0']
	with open('tasks.csv', 'a', newline='') as f_object:
		writer_object = csv.writer(f_object)
		writer_object.writerow(task_list)
		f_object.close()

	clean_screen()

def delete_task():
	with open("tasks.csv") as fileObject:
		heading = next(fileObject)
		reader_obj = csv.reader(fileObject)
		task_names = []
		for task in reader_obj:
			task_names.append(task[0])

		if(len(task_names) == 0):
			clean_screen()
			return

		title = 'Select task to delete'
		task_names, index = pick(task_names, title, indicator='=>')

	fo = pd.read_csv("tasks.csv")

	fo = fo.drop(fo.index[index])

	fo.to_csv("tasks.csv", index=False)

def change_status():
	fo = pd.read_csv("tasks.csv")
	states = fo['state'].tolist()
	names = fo['name'].tolist()

	un_states = []
	un_names = []

	for i,j in zip(states, names):
		if(i == 0):
			un_names.append(j)
			un_states.append(i)

	if len(un_states) == 0:
		clean_screen()
		return


	title = 'Select task to mark as completed'
	un_name, index = pick(un_names, title, indicator='=>', min_selection_count = 0)

	
	un_states[index] = 1 #Change the selected task's state to completed
	fnl = {}

	un_tasks = dict(zip(un_names, un_states))
	tasks = dict(zip(names,states))
	fnl = {**tasks, **un_tasks}

	df = pd.DataFrame.from_dict(fnl, orient="index")
	header = ['name','state']
	
	df.reset_index().to_csv("tasks.csv", index=False, header=header)


clean_screen()
while True:
	index = options_menu()

	if(index== 0):
		list_tasks()

		continue

	if(index == 1):
		add_task()
		continue

	if(index == 2):
		delete_task()
		continue

	if(index == 3):
		change_status()
		continue

	if(index == 4):
		break