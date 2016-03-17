import flowParam as param
class Graph:
	def __init__(self, start, dstList, mnodeList, numEdges, edges, start_time, fout, testNum):
		self.start = start
		self.dstList = dstList
		self.mnodeList = mnodeList
		self.numEdges = numEdges
		self.edges = edges
		self.start_time = start_time
		self.time = start_time
		self.found = False
		self.end_time = -1
		self.fout = fout
		self.loop = 0
		self.testNum = testNum
		self.written = 0

	def run(self, method):
		res = None
		if method == param.SEARCH_METHOD['BFS']:
			self.search_bfs()

		elif method == param.SEARCH_METHOD['DFS']:
			self.search_dfs()
		else:
			self.search_ucs()

		if not self.found:
			self.fout.write('None\n')

	def search_bfs(self):
		#print 'bfs search'
		queue = []
		if self.start.color == param.COLOR['WHITE'] and not self.found:
			self.start.distance = 0
			self.start.startTime = self.time
			self.start.color = param.COLOR['BLACK']
			if self.isReached(self.start):
				self.fout.write('None'+'\n')
				return
			queue.append(self.start)
			
			while queue and not self.found:
				self.loop += 1
				queue1 = []
				node = queue[0]
				#print 'node-label:', node.label,'distance', node.distance
				del queue[0]
				if self.edges.get(node.label, None):
					elist = self.edges[node.label]
					for dst in sorted(elist, reverse=False):
						edge = elist[dst]
						if self.loop == 1:
							for period in edge.offList:
								item = period.split('-')
								if node.startTime>=int(item[0]) and node.startTime<=int(item[1]):
									continue
						if edge.endNode.color == param.COLOR['WHITE']:
							edge.endNode.color = param.COLOR['GRAY']
							edge.endNode.distance = node.distance+1
							edge.endNode.parent = node
							if self.isReached(edge.endNode):
								self.fout.write(edge.endNode.label+' '+str((self.start_time+edge.endNode.distance)%24)+'\n')
								break
							queue1.append(edge.endNode)
				self.start.color = param.COLOR['BLACK']
				queue.extend(queue1)

	def search_dfs(self):
		#print 'dfs-called'
		#self.print_edges()
		if self.isReached(self.start):
			self.fout.write('None'+'\n')
			return

		if self.start.color == param.COLOR['WHITE'] and not self.found:
			self.start.distance = 0
			self.dfs_visit(self.start)

	def dfs_visit(self, node):
		self.loop+=1
		if not self.found and not self.isReached(node):
			node.color = param.COLOR['GRAY']
			node.startTime = self.time
			##print 'node:',node.label, ' st:',node.startTime
			self.time+=1
			if self.edges.get(node.label, None):
				elist = self.edges[node.label]
				for dst in sorted(elist, reverse=False):
					edge = elist[dst]
					if self.loop == 1:
						for period in edge.offList:
							item = period.split('-')
							if node.startTime>=int(item[0]) and node.startTime<=int(item[1]):
								continue
					if edge.endNode.color == param.COLOR['WHITE']:
						edge.endNode.distance = node.distance+1
						edge.endNode.parent = node
						#print 'visiting node', edge.endNode.label, ' distance:', edge.endNode.distance, ' Parent:', edge.endNode.parent.label
						self.dfs_visit(edge.endNode)
			node.endTime = self.time
			self.time+=1
			node.color = param.COLOR['BLACK']
		elif self.found and not self.written:
			#node is the destination node.
			self.fout.write(node.label+' '+str((self.start_time+node.distance)%24)+'\n')
			self.written = 1


	def isReached(self, node):
		if self.dstList.__contains__(node):
			self.end_time = self.time
			self.time+=1
			self.found = True
			node.color = param.COLOR['GRAY']
			#write into output file
			##print 'destination node:',node.label, 'end_time',self.end_time, ' distance:',node.distance
		return self.found

	def search_ucs(self):
		#print 'ucs-called'
		self.print_edges()
		frontier = {}
		if self.start.color == param.COLOR['WHITE'] and not self.found:
			self.start.distance = self.start_time
			self.start.startTime = self.start_time
			frontier[self.start] = self.start.distance
			self.start.parent = self.start
			self.start.color = param.COLOR['GRAY']
			if self.isReached(self.start):
				self.fout.write('None'+'\n')
				return
		while frontier and not self.found:
			nearestNode = self.getNearestNode(frontier)
			if nearestNode:
				if self.start==nearestNode or self.canPassWater(nearestNode):
					if self.isReached(nearestNode):
						self.fout.write(nearestNode.label+' '+str(nearestNode.startTime%24)+'\n')
						break
					del frontier[nearestNode]
					#print 'nearestNode',nearestNode.label
					nearestNode.color = param.COLOR['BLACK']
					if self.edges.get(nearestNode.label, None):
						elist = self.edges[nearestNode.label]
						for dst in elist:
							edge = elist[dst]
							if self.dstList.__contains__(edge.endNode) and not self.canUcsPassWater(edge.endNode, nearestNode):
								continue
							if edge.endNode.color == param.COLOR['WHITE']:
								edge.endNode.distance = (nearestNode.startTime+edge.weight)
								edge.endNode.color = param.COLOR['GRAY']
								edge.endNode.startTime = (nearestNode.startTime+edge.weight)
								edge.endNode.parent = nearestNode
								frontier[edge.endNode] = edge.endNode.distance
								#print 'endnode added to frontier',edge.endNode.label,' start-time',edge.endNode.startTime
							elif edge.endNode.color == param.COLOR['GRAY']:
								if((((nearestNode.startTime+edge.weight))<edge.endNode.startTime)):
									if self.canUcsPassWater(edge.endNode, nearestNode):
										edge.endNode.distance = (nearestNode.startTime+edge.weight)
										edge.endNode.color = param.COLOR['GRAY']
										edge.endNode.startTime = (nearestNode.startTime+edge.weight)
										edge.endNode.parent = nearestNode
										frontier[edge.endNode] = edge.endNode.distance
										#print 'endnode added to frontier',edge.endNode.label,' start-time',edge.endNode.startTime
				else:
					del frontier[nearestNode]
					nearestNode.color = param.COLOR['WHITE']
					nearestNode.distance = -1
					nearestNode.startTime = -1
					nearestNode.parent = None
					continue
			else:
				break

	def canPassWater(self, node):
		edge = self.edges[node.parent.label][node.label]
		parent = node.parent
		##print 'node-label', node.label, 'start-time',node.startTime, 'parent', node.parent
		#print 'checking node for ..',node.label, 'start-time:',node.startTime, ' --parent:',parent.label
		for period in edge.offList:
			item = period.split('-')
			#print 'off item',item
			if ((parent.startTime%24)>=int(item[0]) and (parent.startTime%24)<=int(item[1])):
				#print 'node',node.label, ' cannot be selected to pass water: ',node.startTime
				return False
		#print 'node',node.label, ' canbe selected to pass water: ',node.startTime
		return True

	def canUcsPassWater(self, node, parent):
		edge = self.edges[parent.label][node.label]
		for period in edge.offList:
			item = period.split('-')
			#print 'off item',item
			#if (((node.startTime%24)>=int(item[0]) and (node.startTime%24)=<int(item[1])))or ((parent.startTime%24)>=int(item[0]) and (parent.startTime%24)=<int(item[1])):
			if ((parent.startTime%24)>=int(item[0]) and (parent.startTime%24)<=int(item[1])):
				#print 'node',node.label, ' cannot be selected to pass water: ',node.startTime
				return False
		#print 'ucs pass water selected'
		#print 'node',node.label, ' canbe selected to pass water: ',node.startTime
		return True



	def relaxEdge(self, edge, src):
		edge.endNode.color = param.COLOR['GRAY']
		if (edge.endNode.distance == -1) or (edge.endNode.distance<=(src.distance+edge.weight)):
			edge.endNode.distance = src.distance+edge.weight
			edge.endNode.parent = src

	def getNearestNode(self, queue):
		q = sorted(queue, key=queue.get)
		q1 = {}
		#print 'queue',queue

		if len(q)==0:
			return None
		elif len(q)==1:
			return q[0]
		elif queue[q[0]] == queue[q[1]]:
			cost = queue[q[0]]
			for elem in q:
				if(queue[elem]==cost):
					q1[elem.label] = elem
				else:
					break
			#print 'q',q
			#print 'q1-w/o sort',q1
			#print 'q1',sorted(q1)
			#print 'q1-s-s',sorted(q1)[0]
			if len(q1)>1:
				if len(sorted(q1)[0])>len(sorted(q1)[1]):
					return q1[sorted(q1)[1]]
			return q1[sorted(q1)[0]]
		else:
			return q[0]

	def print_edges(self):
		#print 'edges',self.edges
		for key in self.edges:
			for dst in self.edges[key]:
				self.edges[key][dst].print_edge()

class Edge:
	def __init__(self, start, end, wt, noff, offList):
		self.startNode = start
		self.endNode = end
		self.weight = wt
		self.noff = noff
		self.offList = offList

	def print_edge(self):
		#print 'src:', self.startNode.label, 'Dst:',self.endNode.label, 'Wt:',self.weight, 'noff',self.noff, 'nlist:',self.offList
		pass

class Node:
	def __init__(self, label):
		self.label = label
		self.color = param.COLOR['WHITE']
		self.parent = None
		self.distance = -1
		self.startTime = -1
		self.endTime = -1
