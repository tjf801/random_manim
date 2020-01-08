from big_ol_pile_of_manim_imports import *
import mpmath
from math import floor, log

class PlotFunctions(GraphScene):
	CONFIG = {
		"x_min": -20,
		"x_max": 20,
		"x_axis_width": 30,
		"x_tick_frequency": 5,
		"x_leftmost_tick": None, # Change if different from x_min
		"x_axis_label": "$x$",
		"y_min": -10,
		"y_max": 10,
		"y_axis_height": 16,
		"y_tick_frequency": 5,
		"y_bottom_tick": None, # Change if different from y_min
		"y_axis_label": "$y$",
		"exclude_zero_label": True,

		"axes_color" :GREEN,
		"function_color_1" :RED,
		"function_color_2" :BLUE,
		"x_labeled_nums" :range(-20,22,2),
		"y_labeled_nums" :range(-10,10,1),
		"graph_origin" :ORIGIN,
	}
	def construct(self):
		self.setup_axes(animate=True)
		func_graph1=self.get_graph(self.func_to_graph1, self.function_color_1)
		func_graph2=self.get_graph(self.func_to_graph2, self.function_color_2)
		graph_lab1 = self.get_graph_label(func_graph1, label = "\\pi(x)")
		graph_lab2 = self.get_graph_label(func_graph2, label = "ln(x)")
		
		self.play(
			ShowCreation(func_graph1), 
			ShowCreation(func_graph2)
		)
		self.play( 
			ShowCreation(graph_lab1), 
			ShowCreation(graph_lab2)
		)
		

	def func_to_graph1(self,x):
		x = math.floor(x)
		t = 0
		for i in range(int(x)):
			for n in range(i):
				if n % i == 0:
					break
			t += 1
		return t
				
		
	def func_to_graph2(self,x):
		try: return float(math.log(x))
		except: return 0