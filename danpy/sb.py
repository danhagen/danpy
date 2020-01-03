import time
from scipy import interpolate
import numpy as np
from termcolor import cprint,colored

def get_terminal_width():
	try:
		from shutil import get_terminal_size
		return get_terminal_size().columns
	except ImportError:
		import subprocess
		return int(subprocess.check_output(["tput", "cols"]))

class dsb:
	def __init__(self,initialValue,finalValue,**kwargs):
		"""
		~~~~~~~~~~~~~~
		**kwargs
		~~~~~~~~~~~~~~

		title should be a str that will be displayed before the statusbar. title
		should be no longer than 25 characters.

		"""

		self.terminalWidth = get_terminal_width()
		usedSpace = len(
			'XXXX.X' + '% Complete, ' + 'XXXXX.X '
			+ ' sec, (est. ' + "XXXXX.X" + ' sec left)')
		self.statusbarWidth = self.terminalWidth - 2 - usedSpace

		self.title = kwargs.get("title",'a Loop')
		assert type(self.title) == str, "title should be a string"

		self.initialValue = initialValue
		assert (type(self.initialValue) == int
				and self.initialValue>=0), \
			"initialValue must be a positvie int or 0."

		self.finalValue = finalValue
		assert (type(self.finalValue) == int
				and self.finalValue>0), \
			"finalValue must be a positvie int."

		self.timeRemaining = '--'
		self.timeArray = []
		self.startTime = time.time()

	def update(self,i,**kwargs):
		"""
		i is the current iteration (must be an int) and must be in [0,N).

		~~~~~~~~~~~~~~

		NOTE: you should place a print('\n') after the loop to ensure you
		begin printing on the next line.

		"""
		assert hasattr(self,"title"), "dsb() was not properly initialized. Does not have title."
		self.title = kwargs.get("title",self.title)
		assert type(self.title) == str, "title should be a string"

		assert type(i)==int, "i must be an int"
		assert self.initialValue<=i<self.finalValue, \
			("i must be greater than or equal to "
			+ str(self.initialValue)
			+ " but less than "
			+ str(self.finalValue)
			)

		if not hasattr(self,"barIndices"):
			self.barIndices = sorted(
				list(
					set(
						[int(el) for el in np.linspace(	self.initialValue,
														self.finalValue,
														self.statusbarWidth+1)]
						)
					)
				)
			self.percentageIndices = sorted(
				list(
					set(
						[int(el) for el in np.linspace(	self.initialValue,
														self.finalValue,
														1001)]
						)
					)
				)
		else:
			if i == self.barIndices[0]:
				self.reset()
				self.barIndices = sorted(
					list(
						set(
							[int(el) for el in np.linspace(	self.initialValue,
															self.finalValue,
															self.statusbarWidth+1)]
							)
						)
					)
				self.percentageIndices = sorted(
					list(
						set(
							[int(el) for el in np.linspace(	self.initialValue,
															self.finalValue,
															1001)]
							)
						)
					)

		if i == self.initialValue:
			print(colored(
				(">>> Running "
				+ self.title
				+ " <<<"
				),'blue',attrs=['bold']))
			self.statusbarString = colored((
				'['
				+ '\u25a0'
					*int(
						(i-self.initialValue+1)
						/((self.finalValue-self.initialValue)/self.statusbarWidth)
						) \
				+ '\u25a1'
					*(
						self.statusbarWidth
						-int(
							(i-self.initialValue+1)
							/((self.finalValue-self.initialValue)/self.statusbarWidth)
							)
					)
				+ '] '
				), 'white',attrs=['bold'])
		elif i == self.barIndices[1]:
			self.statusbarString = colored((
				'['
				+ '\u25a0'
					*int(
						(i-self.initialValue+1)
						/((self.finalValue-self.initialValue)/self.statusbarWidth)
						) \
				+ '\u25a1'
					*(
						self.statusbarWidth
						-int(
							(i-self.initialValue+1)
							/((self.finalValue-self.initialValue)/self.statusbarWidth)
							)
					)
				+ '] '
				), 'white',attrs=['bold'])
			self.timeArray.append(abs(time.time()-self.startTime))
			self.timeRemaining = '{0:1.1f}'.format(self.timeArray[-1]*((self.finalValue-self.initialValue)/(i-self.initialValue+1)))
		elif i+1 in self.barIndices[2:]:
			self.statusbarString = colored((
				'['
				+ '\u25a0'
					*int(
						(i-self.initialValue+1)
						/((self.finalValue-self.initialValue)/self.statusbarWidth)
						) \
				+ '\u25a1'
					*(
						self.statusbarWidth
						-int(
							(i-self.initialValue+1)
							/((self.finalValue-self.initialValue)/self.statusbarWidth)
							)
					)
				+ '] '
				), 'white',attrs=['bold'])
			self.timeArray.append(abs(time.time()-self.startTime))
			run_time_func = interpolate.interp1d(
				np.arange(len(self.timeArray)),
				self.timeArray,
				fill_value='extrapolate'
				)
			endTimeEstimate = run_time_func(len(self.barIndices)-3)
			self.timeRemaining = '{0:1.1f}'.format(
				float(abs(endTimeEstimate - (time.time()-self.startTime)))
				)

		if i+1 in self.percentageIndices:
			if i+1 == self.percentageIndices[-1]:
				self.statusbar = (
					self.statusbarString
					+ colored(
						('{0:1.1f}'.format((i-self.initialValue+1)/(self.finalValue-self.initialValue)*100)
						+ '% complete, '
						),'blue')
					+ colored(
						('(Total Run Time: '
						+ '{0:1.1f}'.format(time.time() - self.startTime)
						+ ' sec)'
						),'green')
					+ '\n'
					)
				print(" "*(self.terminalWidth-1), end='\r')
				print(self.statusbar + '\n', end='\r')
			else:
				if not hasattr(self,"statusbar"):
					previousLength = self.terminalWidth-1
				else:
					previousLength = len(self.statusbar)
				self.statusbar = (
					self.statusbarString
					+ colored((
						'{0:1.1f}'.format((i-self.initialValue+1)/(self.finalValue-self.initialValue)*100)
						+ '% complete, '
						),'blue')
					+ colored((
						'{0:1.1f}'.format(time.time() - self.startTime)
						+ ' sec,'
						),'red')
					+ colored((
						' (est. '
						+ self.timeRemaining
						+ ' sec left)'
						),'white')
					)
				if previousLength > len(self.statusbar):
					print(" "*(self.terminalWidth-1), end='\r')
				print(self.statusbar, end='\r')
	def reset(self,**kwargs):
		"""
		Resets the statusbar for easy sequential loops. Default settings are best used for consecutive loops of the same size, with the same starting value and the same title. Title, starting value, and number of loops can be changed via **kwargs.

		~~~~~~~~~~~~~~
		**kwargs
		~~~~~~~~~~~~~~

		title should be a str that will be displayed before the statusbar. title
		should be no longer than 25 characters. Default will be the previous title.

		initialValue must be an int greater than or equal to zero. Default is the previous initialValue.

		finalValue must be a positive int. Default is the previous finalValue.
		"""

		self.__delattr__('barIndices')

		assert hasattr(self,"title"), "dsb() has no attr 'title'. dsb() must be initialized before it can be reset."
		self.title = kwargs.get("title",self.title)
		assert type(self.title) == str, "title should be a string"

		assert hasattr(self,"initialValue"), "dsb() has no attr 'initialValue'. dsb() must be initialized before it can be reset."
		self.initialValue = kwargs.get("initialValue",self.initialValue)
		assert (type(self.initialValue) == int
				and self.initialValue>=0), \
			"initialValue must be a positvie int or 0."

		assert hasattr(self,"finalValue"), "dsb() has no attr 'finalValue'. dsb() must be initialized before it can be reset."
		self.finalValue = kwargs.get('finalValue',self.finalValue)
		assert (type(self.finalValue) == int
				and self.finalValue>0), \
			"finalValue must be a positvie int."

		self.timeRemaining = '--'
		self.timeArray = []
		self.startTime = time.time()
