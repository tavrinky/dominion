

class Logger(object):
	
	def __init__(self):
		self.log = []

	def add(self, t):
		self.log.append(t)

	def addMany(self, ts):
		self.log.extend(ts)

	def __str__(self):
		self.log.join("\n")

	
