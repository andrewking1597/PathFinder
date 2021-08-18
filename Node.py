class Node:
	def __init__(self, r, c, g=None, h=None, f=None, status=None, size=25, screen=None):
		self.ROW = r
		self.COL = c
		self.SIZE = size # length in px of one side of node
		self.SCREEN = screen
		self.X = self.COL * self.SIZE
		self.Y = self.ROW * self.SIZE
		self.gcost = g # distance from start node
		self.hcost = h # distance from end node
		self.fcost = f # gcost + hcost
		self.status = status # None (not yet opened), green (open), red (already clicked), start, end
		self.prev = None # this will be set when a node is 'selected'; it will point at the previously selected node

	def set_hcost(self, endnode):
		
		# if deltaR > deltaC: (deltaC * 14) + (deltaR - deltaC) * 10
		deltaR = abs(endnode.ROW - self.ROW)
		deltaC = abs(endnode.COL - self.COL)

		if deltaR > deltaC:
			self.hcost = (deltaC * 14) + (deltaR - deltaC) * 10
		elif deltaC > deltaR:
			self.hcost = (deltaR * 14) + (deltaC - deltaR) * 10
		else:
			self.hcost = 14 * deltaR

		return

	def update_fcost(self):
		self.fcost = self.gcost + self.hcost
		return
