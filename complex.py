from big_ol_pile_of_manim_imports import *
import cmath

class ComplexMultiplication(ComplexTransformationScene):
	CONFIG = {
		"horiz_end_color" : GOLD,
		"y_min" : -8,
		"y_max" : 8,
		}
	
	def get_path(self, start, finish):
		return ParametricFunction(lambda t: self.z_to_point(start*(1-t) + finish*t))
	
	def get_dot(self, number, Color):
		return Dot(self.z_to_point(number), color = Color)
	
	def construct(self):
		z = 1 - 1j
		p = 2 + 3j
		
		zdot = self.get_dot(z, YELLOW)
		onedot = self.get_dot(1, BLUE)
		pdot = self.get_dot(p, BLUE)
		
		zdot.path = self.get_path(z, p*z)
		onedot.path = self.get_path(1, p)
		
		
		self.add(zdot, pdot, onedot)
		self.add_transformable_plane()
		self.wait()
		function = lambda x: p * x
		self.apply_complex_function(function, added_anims = [MoveAlongPath(zdot, zdot.path, run_time = 5), MoveAlongPath(onedot, onedot.path, run_time = 5)])

class RandomPolynomial(ComplexTransformationScene):
	CONFIG = {
		"horiz_end_color" : GOLD,
		"y_min" : -8,
		"y_max" : 8,
		"function" : lambda z : (z-(1+2j))**3 + (1+1j)*z + (2-3j),
		}
	
	def construct(self):
		self.add_transformable_plane(animate = True)
		self.apply_complex_function(self.function)
		self.wait(4)

class z_squared(ComplexTransformationScene):
	CONFIG = {
		"horiz_end_color" : GOLD,
		"y_min" : -8,
		"y_max" : 8,
		"function" : lambda z : z**2,
		}
	
	def construct(self):
		self.add_transformable_plane(animate = True)
		self.apply_complex_function(self.function)
		self.wait(4)

class z_cubed(ComplexTransformationScene):
	CONFIG = {
		"num_anchors_to_add_per_line" : 100,
		"horiz_end_color" : GOLD,
		"y_min" : -8,
		"y_max" : 8,
		"function" : lambda z : z**3,
		}
	
	def construct(self):
		self.add_transformable_plane(animate = True)
		self.apply_complex_function(self.function)
		self.wait(4)

class exp_z(ComplexTransformationScene):
	CONFIG = {
		"num_anchors_to_add_per_line" : 100,
		"horiz_end_color" : GOLD,
		"y_min" : -8,
		"y_max" : 8,
		"function" : lambda z : mpmath.exp(z),
		}
	
	def construct(self):
		self.add_transformable_plane(animate = True)
		self.apply_complex_function(self.function)
		self.wait(4)

