from big_ol_pile_of_manim_imports import *
from math import sqrt, gcd

class Transformation(LinearTransformationScene):
	def construct(self):
		self.setup()
		
		matrix = [[3, 1], [0, 2]]
		
		a = matrix[0][0]
		b = matrix[0][1]
		c = matrix[1][0]
		d = matrix[1][1]
		
		print(matrix_to_tex_string(matrix))
		strmatrix = TexMobject(matrix_to_tex_string(matrix)).set_color(WHITE)
		
		self.add(strmatrix)
		strmatrix.to_edge(UL)
		strmatrix.shift(RIGHT)
		
		self.wait(2)
		self.apply_matrix(matrix)
		self.wait(5)

class TransformVector(LinearTransformationScene):
	def construct(self):
		self.setup()
		
		#matrix = [
		#	[1, -2], 
		#	[2, 1]
		#]
		
		#matrix = [[2, 2], [1, 3]]
		matrix = [[3, 0], [1, 2]]
		vector = [2, 1]
		
		a = matrix[0][0]
		b = matrix[0][1]
		c = matrix[1][0]
		d = matrix[1][1]
		
		x = vector[0]
		y = vector[1]
		
		result = [(a*x)+(c*y), +	(b*x)+(d*y)]
		
		strmatrix = TexMobject(matrix_to_tex_string(matrix)).set_color(WHITE)
		strvector = TexMobject(matrix_to_tex_string(vector)).set_color(YELLOW)
		strequals = TexMobject("=").set_color(WHITE)
		strresult = TexMobject(matrix_to_tex_string(result)).set_color(YELLOW)
		
		self.add(strmatrix)
		self.add(strvector, strequals, strresult)
		strmatrix.to_edge(UL)
		strmatrix.shift(RIGHT)
		strvector.next_to(strmatrix, RIGHT)
		strequals.next_to(strvector, RIGHT)
		strresult.next_to(strequals, RIGHT)
		
		self.wait(1)
		self.add_vector(vector)
		self.wait(2)
		self.apply_matrix(matrix)
		self.wait(5)

class Determinant(LinearTransformationScene):
	CONFIG = {
		"show_square" : True
	}
	
	def construct(self):
		self.setup()
		
		matrix = [[3, 1], [0, 2]]
		a = matrix[0][0]
		b = matrix[0][1]
		c = matrix[1][0]
		d = matrix[1][1]
		
		det = a*d - b*c
		
		strmatrix = TexMobject(
			matrix_to_tex_string([
				[str(a), str(b)],
				[str(c), str(d)],
			])
		).set_color(WHITE)
		
		strdet = TexMobject(
			("\\det\\left( %s \\right)="+str(det))%matrix_to_tex_string([
				[str(a), str(b)],
				[str(c), str(d)],
			])
		)
		
		self.add(strmatrix)
		strmatrix.to_edge(UL)
		self.add(strdet)
		strdet.to_edge(UR)
		
		self.wait(1)
		if self.show_square: self.add_unit_square() #TODO not be ugly and add "A --> 6*A"
		self.wait(2)
		self.apply_matrix(matrix)
		self.wait(5)

class Eigenvectors(LinearTransformationScene):
	def construct(self):
		self.setup()
		
		matrix = [[3, 1], [0, 2]]
		
		a = matrix[0][0]
		b = matrix[0][1]
		c = matrix[1][0]
		d = matrix[1][1]
		
		det = a*d - b*c
		
		T = a + d
		D = det
		
		E1 = T/2 + sqrt(T**2/4-D)
		E2 = T/2 - sqrt(T**2/4-D)
		
		if(round(E1) == E1):
			E1 = int(E1)
			g = gcd(b, E1-a)
			i = gcd(E1-d, c)
		if(round(E2) == E2):
			E2 = int(E2)
			h = gcd(b, E2-a)
			j = gcd(E2-d, c)
		
		if (b == 0 and c != 0):
			V1 = [(E1-d)/i, c/i]
			V2 = [(E2-d)/j, c/j]
		elif (c == 0 and b != 0):
			V1 = [b/g, (E1-a)/g]
			V2 = [b/h, (E2-a)/h]
		elif (c == 0 and b == 0):
			V1 = [1, 0]
			V2 = [0, 1]
		else:
			V1 = [b/g, (E1-a)/g]
			V2 = [b/h, (E2-a)/h]
		
		V1[0] = int(V1[0])
		V1[1] = int(V1[1])
		V2[0] = int(V2[0])
		V2[1] = int(V2[1])
		
		strmatrix = TexMobject(
			matrix_to_tex_string([
				[str(a), str(b)],
				[str(c), str(d)],
			])
		).set_color(WHITE)

		streigen = TexMobject(
			matrix_to_tex_string([
				[str(V1[0]), str(V2[0])],
				[str(V1[1]), str(V2[1])],
			])
		).set_color(PINK)
		
		strevals = TexMobject(str(E1) + " , " + str(E2)).set_color(PINK)
		
		EV1 = Vector(V1[0]*RIGHT + V1[1]*UP).set_color(PINK)
		EV2 = Vector(V2[0]*RIGHT + V2[1]*UP).set_color(PINK)
		
		self.add(strmatrix)
		strmatrix.to_edge(UL)
		strmatrix.shift(RIGHT)
		
		self.add(streigen, strevals)
		streigen.next_to(strmatrix, DOWN)
		strevals.next_to(streigen, 2*RIGHT)
		
		self.wait(1)
		self.add_vector(EV1)
		self.add_vector(EV2)
		self.wait(2)
		self.apply_matrix(matrix)
		self.wait(5)

class InverseMatrix(LinearTransformationScene):
	def construct(self):
		self.setup()
		
		#matrix = [[2, 2], [1, 3]]
		matrix = [
				[3, 1], 
				[0, 2]]
		#matrix = [[round(1/sqrt(2),3), round(1/sqrt(2),3)],[round(1/sqrt(2),3), round(-1/sqrt(2),3)]]
		
		a = matrix[0][0]
		b = matrix[0][1]
		c = matrix[1][0]
		d = matrix[1][1]
		
		det = a*d - b*c
		adjugatematrix = [[d, -b],[-c, a]]
		matrixinverse = [[d/det, -b/det],[-c/det, a/det]]
		
		strmatrix = TexMobject(matrix_to_tex_string(matrix)).set_color(WHITE)
		stradjugate = TexMobject(matrix_to_tex_string(adjugatematrix)).set_color(PINK)
		strdet = TexMobject("\\frac{1}{" + str(det) + "}").set_color(PINK)
		
		if round(det,3)==1:inverse = VGroup(stradjugate)
		elif round(det,3)==-1:inverse = VGroup(TexMobject("-"), stradjugate)
		else:inverse = VGroup(strdet, stradjugate)
		inverse.arrange(RIGHT)
		inverse.to_edge(UR)
		strmatrix.shift(LEFT)
		strmatrix.to_edge(UL)
		self.add(strmatrix, inverse)
		
		self.wait(5)
		self.apply_matrix(matrix)
		self.wait(5)
		self.apply_matrix(matrixinverse)
		self.wait(5)

class Solve2x2System(LinearTransformationScene):
	def construct(self):
		matrix = [
			[2, -1],
			[3, 1]]
		vector = [3, 7]
		
		a = matrix[0][0]
		b = matrix[0][1]
		c = matrix[1][0]
		d = matrix[1][1]
		x = vector[0]
		y = vector[1]
		
		det = a*d - b*c
		adjugatematrix = [[d, -b],[-c, a]]
		matrixinverse = [[d/det, -b/det],[-c/det, a/det]]
		result = [(adjugatematrix[0][0]*x + adjugatematrix[0][1]*y)/det, (adjugatematrix[1][0]*x + adjugatematrix[1][1]*y)/det]
		for i in range(len(result)):
			if round(result[i], 3)==round(result[i]): result[i] = int(result[i])
		
		
		equation1 = TextMobject(str(a) + "x + " + str(b) + "y = " + str(vector[0]))
		equation2 = TextMobject(str(c) + "x + " + str(d) + "y = " + str(vector[1]))
		
		equations = VGroup(equation1, equation2)
		equations.arrange(DOWN)
		equations.to_edge(UL)
		strmatrix = TexMobject(matrix_to_tex_string(matrix)).set_color(WHITE)
		strvars = TexMobject(matrix_to_tex_string(["x", "y"])).set_color(YELLOW)
		equals = TexMobject("=")
		strvector = TexMobject(matrix_to_tex_string([str(x), str(y)])).set_color(YELLOW)
		matrixeq = VGroup(strmatrix, strvars, equals, strvector)
		matrixeq.arrange(RIGHT)
		matrixeq.to_edge(UL)
		strinvmatrix = TexMobject(matrix_to_tex_string(matrix)+ "^{-1}").set_color(PINK)
		strvars2 = TexMobject(matrix_to_tex_string(["x", "y"])).set_color(YELLOW)
		equals2 = TexMobject("=")
		strvector2 = TexMobject(matrix_to_tex_string([str(x), str(y)])).set_color(YELLOW)
		invmatrixeq = VGroup(strvars2, equals2, strinvmatrix, strvector2)
		invmatrixeq.arrange(RIGHT)
		invmatrixeq.to_edge(UL)
		strvars3 = TexMobject(matrix_to_tex_string(["x", "y"])).set_color(YELLOW)
		equals3 = TexMobject("=")
		strresult = TexMobject(matrix_to_tex_string([str(result[0]), str(result[1])])).set_color(YELLOW)		
		resulteq = VGroup(strvars3, equals3, strresult)
		resulteq.arrange(RIGHT)
		resulteq.to_edge(UL)
		
		
		self.play(FadeIn(equations))
		self.wait(3)
		self.play(Transform(equations, matrixeq))
		self.wait(3)
		self.apply_matrix(matrix)
		self.wait(4)
		self.add_vector(vector)
		self.wait(2)
		self.play(Transform(equations, invmatrixeq))
		self.wait(3)
		self.apply_matrix(matrixinverse)
		self.wait(3)
		self.play(Transform(equations, resulteq))
		self.wait(5)

