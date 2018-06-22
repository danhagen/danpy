import time
from scipy import interpolate
import numpy as np
from termcolor import cprint,colored

class dsb:
	def __init__(self):
		self.counter = 0
		self.TimeArray = []
		self.StartTime = time.time()
		self.TimeLeft = '--'
	def statusbar(self,i,N,**kwargs):
		"""
		i is the current iteration (must be an int) and N is the length of
		the range (must be an int). i must also be in [0,N).

		~~~~~~~~~~~~~~
		**kwargs
		~~~~~~~~~~~~~~

		Title should be a str that will be displayed before the statusbar. Title
		should be no longer than 25 characters.

		~~~~~~~~~~~~~~

		NOTE: you should place a print('\n') after the loop to ensure you
		begin printing on the next line.

		"""
		def get_terminal_width():
			try:
				from shutil import get_terminal_size
				return get_terminal_size().columns
			except ImportError:
				import subprocess
				return int(subprocess.check_output(["tput", "cols"]))

		TerminalWidth = get_terminal_width()
		UsedSpace = len('XXXX.X' + '% Complete, ' + 'XXXXX.X ' \
							+ ' sec, (est. ' + "XXXXX.X" + ' sec left)')
		StatusBarWidth = TerminalWidth - 2 - UsedSpace

		Title = kwargs.get("Title",'')
		assert type(Title) == str, "Title should be a string"

		assert type(i)==int, "i must be an int"
		assert type(N)==int, "N must be an int"
		assert N>i, "N must be greater than i"
		assert N>0, "N must be a positive integer"
		assert i>=0, "i must not be negative (can be zero)"

		statusbar = colored('[' + '\u25a0'*int((i+1)/(N/StatusBarWidth)) \
							+ '\u25a1'*(StatusBarWidth-int((i+1)/(N/StatusBarWidth))) + '] ',\
							'white',attrs=['bold'])
		if hasattr(self,'Bars'):
			if i == self.Bars[0]:
				self.__delattr__('Bars')
				self.__init__()

		if self.counter == 0:
			self.Bars = list(set([int(el) for el in np.linspace(i,N,StatusBarWidth+1)]))
			print(colored(">>> Running " + Title + " <<<",'blue',attrs=['bold']))
			self.counter += 1
		elif i==self.Bars[1] and self.counter == 1:
			self.TimeArray.append(time.time()-self.StartTime)
			self.TimeLeft = '{0:1.1f}'.format(self.TimeArray[-1]*(N/(i+1)))
			self.counter += 1
		elif i == self.Bars[self.counter]:
			self.TimeArray.append(time.time()-self.StartTime)
			self.TimeLeft = \
					'{0:1.1f}'.format(\
						float(\
							interpolate.interp1d(\
								np.arange(len(self.TimeArray)),self.TimeArray,\
									fill_value='extrapolate')(len(self.Bars)-3))\
										-(time.time()-self.StartTime))
			self.counter += 1
		print(" "*TerminalWidth,end='\r')
		print(statusbar + colored('{0:1.1f}'.format((i+1)/N*100) + '% complete, ','blue') + \
			colored('{0:1.1f}'.format(time.time() - self.StartTime) + ' sec,','red') + \
			colored(' (est. ' + self.TimeLeft + ' sec left)','white'), end='\r')
		if i == N-1:
			print(" "*TerminalWidth)
			print(statusbar + colored('{0:1.1f}'.format((i+1)/N*100) + '% complete, ','blue') + \
				+ colored('(Total Run Time: ' + '{0:1.1f}'.format(time.time() - self.StartTime) + ' sec)','green'))
			print('\n')
	def reset_dsb(self):
		self.__delattr__('Bars')
		self.__init__()
