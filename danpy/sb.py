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
	def __init__(self,number_of_loops,**kwargs):
		"""
		~~~~~~~~~~~~~~
		**kwargs
		~~~~~~~~~~~~~~

		title should be a str that will be displayed before the statusbar. title
		should be no longer than 25 characters.

		starting_value must be an int greater than or equal to zero. Default is zero.
		"""

		self.time_array = []
		self.start_time = time.time()
		self.time_left = '--'

		self.terminal_width = get_terminal_width()
		used_space = len(
			'XXXX.X' + '% Complete, ' + 'XXXXX.X '
			+ ' sec, (est. ' + "XXXXX.X" + ' sec left)')
		self.statusbar_width = self.terminal_width - 2 - used_space

		self.title = kwargs.get("title",'a Loop')
		assert type(self.title) == str, "title should be a string"

		self.starting_value = kwargs.get("starting_value",0)
		assert (type(self.starting_value) == int
				and self.starting_value>=0), \
			"starting_value must be a positvie int or 0."

		self.number_of_loops = number_of_loops
		assert (type(self.number_of_loops) == int
				and self.number_of_loops>0), \
			"number_of_loops must be a positvie int."

	def update(self,i,**kwargs):
		"""
		i is the current iteration (must be an int) and must be in [0,N).


		~~~~~~~~~~~~~~

		NOTE: you should place a print('\n') after the loop to ensure you
		begin printing on the next line.

		"""
		if not hasattr(self,"title"):
			self.title = kwargs.get("title","a Loop")
			assert type(self.title) == str, "title should be a string"
		else:
			previous_title = self.title
			self.title = kwargs.get("title",previous_title)
			assert type(self.title) == str, "title should be a string"
		assert type(i)==int, "i must be an int"
		assert self.starting_value<=i<self.number_of_loops, \
			("i must be greater than or equal to "
			+ str(self.starting_value)
			+ " but less than "
			+ str(self.number_of_loops)
			)

		if not hasattr(self,"bar_indices"):
			self.bar_indices = sorted(
				list(
					set(
						[int(el) for el in np.linspace(	self.starting_value,
														self.number_of_loops,
														self.statusbar_width+1)]
						)
					)
				)
			self.percentage_indices = sorted(
				list(
					set(
						[int(el) for el in np.linspace(	self.starting_value,
														self.number_of_loops,
														1001)]
						)
					)
				)
		else:
			if i == self.bar_indices[0]:
				self.reset()
				self.bar_indices = sorted(
					list(
						set(
							[int(el) for el in np.linspace(	self.starting_value,
															self.number_of_loops,
															self.statusbar_width+1)]
							)
						)
					)
				self.percentage_indices = sorted(
					list(
						set(
							[int(el) for el in np.linspace(	self.starting_value,
															self.number_of_loops,
															1001)]
							)
						)
					)

		if i == self.starting_value:
			print(colored(
				(">>> Running "
				+ self.title
				+ " <<<"
				),'blue',attrs=['bold']))
			self.statusbar_string = colored((
				'['
				+ '\u25a0'*int((i+1)/(self.number_of_loops/self.statusbar_width)) \
				+ '\u25a1'*(self.statusbar_width-int((i+1)/(self.number_of_loops/self.statusbar_width)))
				+ '] '
				), 'white',attrs=['bold'])
		elif i == self.bar_indices[1]:
			self.statusbar_string = colored((
				'['
				+ '\u25a0'*int((i+1)/(self.number_of_loops/self.statusbar_width)) \
				+ '\u25a1'*(self.statusbar_width-int((i+1)/(self.number_of_loops/self.statusbar_width)))
				+ '] '
				), 'white',attrs=['bold'])
			self.time_array.append(abs(time.time()-self.start_time))
			self.time_left = '{0:1.1f}'.format(self.time_array[-1]*(self.number_of_loops/(i+1)))
		elif i+1 in self.bar_indices[2:]:
			self.statusbar_string = colored((
				'['
				+ '\u25a0'*int((i+1)/(self.number_of_loops/self.statusbar_width)) \
				+ '\u25a1'*(self.statusbar_width-int((i+1)/(self.number_of_loops/self.statusbar_width)))
				+ '] '
				), 'white',attrs=['bold'])
			self.time_array.append(abs(time.time()-self.start_time))
			run_time_func = interpolate.interp1d(
				np.arange(len(self.time_array)),
				self.time_array,
				fill_value='extrapolate'
				)
			end_time_estimate = run_time_func(len(self.bar_indices)-3)
			self.time_left = '{0:1.1f}'.format(
				float(abs(end_time_estimate - (time.time()-self.start_time)))
				)

		if i+1 in self.percentage_indices:
			if i+1 == self.percentage_indices[-1]:
				self.statusbar = (
					self.statusbar_string
					+ colored(
						('{0:1.1f}'.format((i+1)/self.number_of_loops*100)
						+ '% complete, '
						),'blue')
					+ colored(
						('(Total Run Time: '
						+ '{0:1.1f}'.format(time.time() - self.start_time)
						+ ' sec)'
						),'green')
					+ '\n'
					)
				print(" "*(self.terminal_width-1), end='\r')
				print(self.statusbar + '\n', end='\r')
			else:
				self.statusbar = (
					self.statusbar_string
					+ colored((
						'{0:1.1f}'.format((i+1)/self.number_of_loops*100)
						+ '% complete, '
						),'blue')
					+ colored((
						'{0:1.1f}'.format(time.time() - self.start_time)
						+ ' sec,'
						),'red')
					+ colored((
						' (est. '
						+ self.time_left
						+ ' sec left)'
						),'white')
					)
				print(" "*(self.terminal_width-1), end='\r')
				print(self.statusbar, end='\r')
	def reset(self,**kwargs):
		"""
		Resets the statusbar for easy sequential loops. Default settings are best used for consecutive loops of the same size, with the same starting value and the same title. Title, starting value, and number of loops can be changed via **kwargs.

		~~~~~~~~~~~~~~
		**kwargs
		~~~~~~~~~~~~~~

		title should be a str that will be displayed before the statusbar. title
		should be no longer than 25 characters. Default will be the previous title.

		starting_value must be an int greater than or equal to zero. Default is the previous starting_value.

		number_of_loops must be a positive int. Default is the previous number_of_loops.
		"""

		self.__delattr__('bar_indices')

		self.time_array = []
		self.start_time = time.time()
		self.time_left = '--'

		assert hasattr(self,"title"), "dsb() has no attr 'title'. dsb() must be initialized before it can be reset."
		self.title = kwargs.get("title",self.title)
		assert type(self.title) == str, "title should be a string"

		assert hasattr(self,"starting_value"), "dsb() has no attr 'starting_value'. dsb() must be initialized before it can be reset."
		self.starting_value = kwargs.get("starting_value",self.starting_value)
		assert (type(self.starting_value) == int
				and self.starting_value>=0), \
			"starting_value must be a positvie int or 0."

		assert hasattr(self,"number_of_loops"), "dsb() has no attr 'number_of_loops'. dsb() must be initialized before it can be reset."
		self.number_of_loops = kwargs.get('number_of_loops',self.number_of_loops)
		assert (type(self.number_of_loops) == int
				and self.number_of_loops>0), \
			"number_of_loops must be a positvie int."
