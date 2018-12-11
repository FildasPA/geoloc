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
from StringIO import StringIO

WAIT = 2 # in seconds
PROMPT_SYMBOL = term.green + '\n❯ ' + term.off
MAX_COLUMNS = 10

REMOTE_DEVICES = {
		'BALISE_1': '',
		'BALISE_2': '',
		'BALISE_3': '',
		'BALISE_4': '',
		'BALISE_5': ''
}

balises = sorted([name for name, address in REMOTE_DEVICES.items()])
df = pd.DataFrame(index=balises)


class UserInput(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.typing = False

		os.system('clear')
		term.down(len(df.index) + 2)
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

			if c == 'q':
				print('')
				print(term.yellow + 'Exiting...' + term.off)
				sending.end = True
				return

			command = c + raw_input()

			# Traitement commande

			term.up(1)
			term.clearLine()
			term.up(1)
			self.print_prompt()

			sending.resume()

class SendData(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.active = False
		self.end = False

	def refresh_table(self):
		global df

		term.homePos()
		self.print_status()

		stri = str(df)
		term.left(1000)
		term.clearLine()
		for c in stri:
			sys.stdout.write(c)
			if c == '\n':
				term.left(1000)
				term.clearLine()

		term.restoreCursor()

	def send_data(self):
		global df
		# print('Sending data')
		df[len(df.columns)] = [random.randint(-100, 0) for index in df.index]
		if len(df.columns) > MAX_COLUMNS:
			df.drop(df.columns[0], axis=1, inplace=True)
			df = df.rename(index=str, columns={i:i-1 for i in df.columns})
		# print('Sent data')

	def refresh_status(self):
		term.saveCursor()
		term.up(len(df.index)+3)
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
		while not self.end:
			# print('Démarrage')
			if self.active:
				self.send_data()
				self.refresh_table()
				# print('Sent data')
			sleep(WAIT)
			# self.stop()

user = UserInput()
user.start()

sending = SendData()
sending.start()
sending.join()
