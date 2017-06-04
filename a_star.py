# Problem is a class which allows us to define our problem statement.
# All functions have default return values, but will use the corresponding function if we pass to it.
class Problem(object):
	def heuristic(self, point, goal):
		return 0

	def neighbor_nodes(self, point):
		return []

	def distance_between_neighbors(self, point, point2):
		return 1

	def is_goal(self, point, goal):
		return point == goal

	def on_open(self, point, f, g, h):
		pass

	def on_close(self, point):
		pass

	def on_update(self, point, f, g, h):
		pass


class PathNotFound(Exception):
	pass

def find_path(problem, start, goal):
	'''
	Finds a path from point start to point goal using the A* algorithm.
	'''

	'''
	The open set contains points that we know how to reach from the start
	but have not yet explored all their neighbors.
	'''
	open_set = set()

	'''
	the open_queue contains the same points as the open_set.
	difference is we associates them with, and order them with their f-score.
	'''
	open_queue = list()
	'''
	The closed set contains points that we won't visit again.
	we won't visit them because we've already visited them, and their neighbors.
	'''
	closed_set = set()

	'''
	The came_from dict is a map from each point to one of it's neighbors.
	'''
	came_from = dict()

	'''
	the g-score is the currently best known cost to reach each point. It
	is syncronized with the came_from dict: if you followed it all
	the way back to the start, the cost would be exactly value found in g-score
	for that point. It isn't necessarily the best possible way to get to that
	point, just the best way we've discovered so far.
	'''
	g_score = dict()

	'''
	the h-score is the estimate for how far away from the goal this point is.
	This is estimated using the problem's heuristic function.
	'''
	h_score = dict()

	'''
	f can be computed rather than stored.
	'''
	def f_score(point):
		return g_score[point] + h_score[point]

	# add start to the set.
	g_score[start] = 0
	h = problem.heuristic(start, goal)
	h_score[start] = h
	open_set.add(start)
	open_queue.append( (f_score(start), start) )
	problem.on_open(start, h, 0, h)

	# keep searching until we find the goal, or until all possible paths have been exhausted.
	while open_set:
		open_queue.sort()
		next_f, point = open_queue.pop(0)
		open_set.remove(point)

		if problem.is_goal(point, goal):
			# reached goal, unwind path
			path = [ point ]
			while point != start:
				point = came_from[point]
				path.append(point)
			path.reverse()
			return path

		closed_set.add(point)
		problem.on_close(point)

		for neighbor in problem.neighbor_nodes(point):
			if not neighbor in closed_set:
				# This is us determining the cost of the node.
				# This uses both the accumulated distance and the admissable distance.
				tentative_g_score = g_score[point] + problem.distance_between_neighbors(neighbor, point)

				# Check to see if we've already added the neighbor to our set.
				# if it isn't, we'll score it, and add it our queue.
				# if it is, we'll check it's g_score, using findings from the other paths,
				# and determine whether or not we need to update it's position in our queue.
				if neighbor not in open_set:
					# new territory to explore
					came_from[neighbor] = point
					g = tentative_g_score
					h = problem.heuristic(neighbor, goal)
					g_score[neighbor] = g
					h_score[neighbor] = h
					open_set.add(neighbor)
					f = g + h
					open_queue.append( (f, neighbor) )
					problem.on_open(neighbor, f, g, h)

				else:
					# reconnected to previously explored area
					if tentative_g_score < g_score[neighbor]:
						# but we found a better route than before!
						came_from[neighbor] = point
						g = tentative_g_score
						g_score[neighbor] = g
						h = problem.heuristic(neighbor, goal)
						h_score[neighbor] = h
						f = g + h

						problem.on_update(neighbor, f, g, h)

	raise PathNotFound("no path from %s to %s." % (str(start), str(goal)))
