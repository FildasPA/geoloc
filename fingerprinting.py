#!/usr/bin/python
#-*- coding: utf-8 -*-

# https://github.com/gravmatt/py-term
# https://github.com/magmax/python-readchar

# http://www.tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html

import os
import sys
import random
# import numpy as np
from time import sleep
# import pandas as pd
import threading
import term
import readchar
# from communication import Communication
import at
import db


WAIT = 2 # in seconds
PROMPT_SYMBOL = term.green('\n❯ ')
MAX_COLUMNS = 10

REMOTE_DEVICES = [
		# 'BALISE_1',
		'OBJET_2',
		# 'BALISE_3',
		# 'BALISE_4',
		# 'BALISE_5'
]

# df = pd.DataFrame(index=REMOTE_DEVICES)
bdd = db.BDD()


class UserInput(threading.Thread):

	def __init__(self, table):
		threading.Thread.__init__(self)
		self.typing = False

		os.system('clear')
		term.down(len(table))
		self.print_prompt()
		term.saveCursor()


	def print_prompt(self):
		sys.stdout.write(PROMPT_SYMBOL)
		sys.stdout.flush()


	def run(self):
		global sending

		while True:
			c = readchar.readchar()
			sending.stop()
			sys.stdout.write(c)
			sys.stdout.flush()

			command = c + raw_input()

			# Traitement commande
			result = self.process_command(command)
			if result is True:
				return
			self.print_prompt()

			sending.resume()


	def process_command(self, command):
		if command[0] == 'q':
			print(term.yellow('Exiting...'))
			sending.end = True
			return True
		elif command[0] == 's':
			n = raw_input('n ? ')
			fingers = self.sending
			# print()
			fingers['x'] = raw_input('x ? ')
			fingers['y'] = raw_input('y ? ')
			print(fingers)
			bdd.add_fingerprint(fingers)
			self.sending.clear_fingers()
		return False


class SendData(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.active = False
		self.end = False
		self.fingers = {}
		# self.df = df
		# self.communication = Communication()


	def clear_fingers(self):
		self.fingers = {}


	def __len__(self):
		return len(self.fingers) + self.get_len_header() + 1


	def get_len_header(self):
		return 2


	def refresh_status(self):
		term.saveCursor()
		term.homePos()
		term.left(1000)
		term.clearLine()
		self.print_status()
		term.restoreCursor()


	def print_status(self):
		if self.active:
			status = term.green('ACTIF')
		else:
			status = term.red('ARRET')

		print('RSSI: [' + status + ']')


	def print_table(self):
		term.left(1000)
		term.clearLine()

		for node_id, value in self.fingers:
			term.left(1000)
			term.clearLine()
			print(node_id + ' : ' + value)


	def refresh_table(self):
		term.homePos()
		term.down(self.get_len_header())
		self.print_table()
		term.restoreCursor()


	def send_data(self):
		# self.append_data([random.randint(-100, 0) for index in self.df.index])
		# self.communication.send_data_all()
		self.append_data(at.send())


	# def get_rssi(self):
	# 	self.append_data(self.communication.get_values())
	# 	self.communication.clear_values()


	def append_data(self, finger):
		if finger:
			self.fingers = dict(self.fingers.items() + finger.items())
		# self.df[len(self.df.columns)] = fingerprinting
		# if len(self.df.columns) > MAX_COLUMNS:
		# 	self.df.drop(self.df.columns[0], axis=1, inplace=True)
		# 	self.df = self.df.rename(index=str, columns={i:i-1 for i in self.df.columns})



	def stop(self):
		self.active = False
		self.refresh_status()


	def resume(self):
		self.active = True
		self.refresh_status()


	def run(self):
		self.active = True
		self.end = False

		self.refresh_status()
		while not self.end:
			if self.active:
				self.send_data()
				# sleep(WAIT)
				if self.active:
					# self.get_rssi()
					self.refresh_table()
			else:
				sleep(0.1)


sending = SendData()

user = UserInput(sending)

user.start()
sending.start()
sending.join()
