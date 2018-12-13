#!/usr/bin/python
#-*- coding: utf-8 -*-

# https://github.com/gravmatt/py-term
# https://github.com/magmax/python-readchar

# http://www.tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html

import os
import sys
import random
import numpy as np
from time import sleep
import pandas as pd
import threading
import term
import readchar
# from StringIO import StringIO

WAIT = 2 # in seconds
PROMPT_SYMBOL = term.green + '\n❯ ' + term.off
MAX_COLUMNS = 10

REMOTE_DEVICES = [
		'BALISE_1',
		'BALISE_2',
		'BALISE_3',
		'BALISE_4',
		'BALISE_5'
]

df = pd.DataFrame(index=REMOTE_DEVICES)


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
			print(term.yellow + 'Exiting...' + term.off)
			sending.end = True
			return True
		elif command[0] == 's':
			print('Lul')
		return False


class SendData(threading.Thread):

	def __init__(self, df):
		threading.Thread.__init__(self)
		self.active = False
		self.end = False
		self.df = df


	def __len__(self):
		return len(self.df.index) + 3


	def get_len_header(self):
		return 2


	def print_table(self):
		term.left(1000)
		term.clearLine()
		for c in str(self.df):
			sys.stdout.write(c)
			if c == '\n':
				term.left(1000)
				term.clearLine()


	def refresh_table(self):
		term.homePos()
		term.down(self.get_len_header())
		self.print_table()
		term.restoreCursor()


	def send_data(self):
		# TO REMOVE
		self.append_data([random.randint(-100, 0) for index in self.df.index])


	def append_data(self, fingerprinting):
		self.df[len(self.df.columns)] = fingerprinting
		if len(self.df.columns) > MAX_COLUMNS:
			self.df.drop(self.df.columns[0], axis=1, inplace=True)
			self.df = self.df.rename(index=str, columns={i:i-1 for i in self.df.columns})


	def refresh_status(self):
		term.saveCursor()
		term.homePos()
		term.left(1000)
		term.clearLine()
		self.print_status()
		term.restoreCursor()


	def print_status(self):
		if self.active:
			status = term.green + 'ACTIF'
		else:
			status = term.red + 'ARRET'

		print('RSSI: [' + status + term.off + ']')


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
				self.refresh_table()
				sleep(WAIT)
			else:
				sleep(1)


sending = SendData(df)

user = UserInput(sending)

user.start()
sending.start()
sending.join()
