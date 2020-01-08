from big_ol_pile_of_manim_imports import *

class FourierCirclesScene(Scene):
	CONFIG = {
		"n_circles": 10,
		"big_radius": 2,
		"colors": [
			BLUE_D,
			BLUE_C,
			BLUE_E,
			GREY_BROWN,
		],
		"circle_style": {
			"stroke_width": 2,
		},
		"base_frequency": 1,
		"slow_factor": 0.25,
		"center_point": ORIGIN,
		"parametric_function_step_size": 0.001,
	}

	#
	def get_freqs(self):
		n = self.n_circles
		all_freqs = list(range(n // 2, -n // 2, -1))
		all_freqs.sort(key=abs)
		return all_freqs

	def get_coefficients(self):
		return [complex(0) for x in range(self.n_circles)]

	def get_color_iterator(self):
		return it.cycle(self.colors)

	def get_circles(self, freqs=None, coefficients=None):
		circles = VGroup()
		color_iterator = self.get_color_iterator()
		self.center_tracker = VectorizedPoint(self.center_point)

		if freqs is None:
			freqs = self.get_freqs()
		if coefficients is None:
			coefficients = self.get_coefficients()

		last_circle = None
		for freq, coefficient in zip(freqs, coefficients):
			if last_circle:
				center_func = last_circle.get_start
			else:
				center_func = self.center_tracker.get_location
			circle = self.get_circle(
				coefficient=coefficient,
				freq=freq,
				color=next(color_iterator),
				center_func=center_func,
			)
			circles.add(circle)
			last_circle = circle
		return circles

	def get_circle(self, coefficient, freq, color, center_func):
		radius = abs(coefficient)
		phase = np.log(coefficient).imag
		circle = Circle(
			radius=radius,
			color=color,
			**self.circle_style,
		)
		circle.radial_line = Line(
			circle.get_center(),
			circle.get_start(),
			color=WHITE,
			**self.circle_style,
		)
		circle.add(circle.radial_line)
		circle.freq = freq
		circle.phase = phase
		circle.rotate(phase)
		circle.coefficient = coefficient
		circle.center_func = center_func
		circle.add_updater(self.update_circle)
		return circle

	def update_circle(self, circle, dt):
		circle.rotate(
			self.slow_factor * circle.freq * dt * TAU
		)
		circle.move_to(circle.center_func())
		return circle

	def get_rotating_vectors(self, circles):
		return VGroup(*[
			self.get_rotating_vector(circle)
			for circle in circles
		])

	def get_rotating_vector(self, circle):
		vector = Vector(RIGHT, color=WHITE)
		vector.add_updater(lambda v: v.put_start_and_end_on(
			*circle.radial_line.get_start_and_end()
		))
		return vector

	def get_circle_end_path(self, circles, color=YELLOW):
		coefs = [c.coefficient for c in circles]
		freqs = [c.freq for c in circles]
		center = circles[0].get_center()

		path = ParametricFunction(
			lambda t: center + reduce(op.add, [
				complex_to_R3(
					coef * np.exp(TAU * 1j * freq * t)
				)
				for coef, freq in zip(coefs, freqs)
			]),
			t_min=0,
			t_max=1,
			color=color,
			step_size=self.parametric_function_step_size,
		)
		return path

	# TODO, this should be a general animated mobect
	def get_drawn_path(self, circles, **kwargs):
		path = self.get_circle_end_path(circles, **kwargs)
		broken_path = CurvesAsSubmobjects(path)
		broken_path.curr_time = 0

		def update_path(path, dt):
			alpha = path.curr_time * self.slow_factor
			n_curves = len(path)
			for a, sp in zip(np.linspace(0, 1, n_curves), path):
				b = alpha - a
				if b < 0:
					width = 0
				else:
					width = 2 * (1 - (b % 1))
				sp.set_stroke(YELLOW, width=width)
			path.curr_time += dt
			return path

		broken_path.add_updater(update_path)
		return broken_path

	def get_y_component_wave(self,
							 circles,
							 left_x=1,
							 color=PINK,
							 n_copies=2,
							 right_shift_rate=5):
		path = self.get_circle_end_path(circles)
		wave = ParametricFunction(
			lambda t: op.add(
				right_shift_rate * t * LEFT,
				path.function(t)[1] * UP
			),
			t_min=path.t_min,
			t_max=path.t_max,
			color=color,
		)
		wave_copies = VGroup(*[
			wave.copy()
			for x in range(n_copies)
		])
		wave_copies.arrange(RIGHT, buff=0)
		top_point = wave_copies.get_top()
		wave.creation = ShowCreation(
			wave,
			run_time=(1 / self.slow_factor),
			rate_func=linear,
		)
		cycle_animation(wave.creation)
		wave.add_updater(lambda m: m.shift(
			(m.get_left()[0] - left_x) * LEFT
		))

		def update_wave_copies(wcs):
			index = int(
				wave.creation.total_time * self.slow_factor
			)
			wcs[:index].match_style(wave)
			wcs[index:].set_stroke(width=0)
			wcs.next_to(wave, RIGHT, buff=0)
			wcs.align_to(top_point, UP)
		wave_copies.add_updater(update_wave_copies)

		return VGroup(wave, wave_copies)

	def get_wave_y_line(self, circles, wave):
		return DashedLine(
			circles[-1].get_start(),
			wave[0].get_end(),
			stroke_width=1,
			dash_length=DEFAULT_DASH_LENGTH * 0.5,
		)

	# Computing Fourier series
	def get_coefficients_of_path(self, path, n_samples=10000, freqs=None):
		if freqs is None:
			freqs = self.get_freqs()
		dt = 1 / n_samples
		ts = np.arange(0, 1, dt)
		samples = np.array([
			path.point_from_proportion(t)
			for t in ts
		])
		samples -= self.center_point
		complex_samples = samples[:, 0] + 1j * samples[:, 1]

		result = []
		for freq in freqs:
			riemann_sum = np.array([
				np.exp(-TAU * 1j * freq * t) * cs
				for t, cs in zip(ts, complex_samples)
			]).sum() * dt
			result.append(riemann_sum)
		
		return result

class Fourier(FourierCirclesScene):
	CONFIG = {
		"n_circles": 500,
		"center_point": ORIGIN,
		"slow_factor": 0.1,
		"run_time": 30,
		"tex": "\\pi",
		"start_drawn": False,
	}

	def construct(self):
		path = self.get_path()
		coefs = self.get_coefficients_of_path(path)

		circles = self.get_circles(coefficients=coefs)
		for k, circle in zip(it.count(1), circles):
			circle.set_stroke(width=max(
				1 / np.sqrt(k),
				1,
			))

		# approx_path = self.get_circle_end_path(circles)
		drawn_path = self.get_drawn_path(circles)
		if self.start_drawn:
			drawn_path.curr_time = 1 / self.slow_factor

		self.add(path)
		self.add(circles)
		self.add(drawn_path)
		self.wait(self.run_time)

	def get_path(self):
		tex_mob = TexMobject(self.tex)
		tex_mob.set_height(6)
		path = tex_mob.family_members_with_points()[0]
		path.set_fill(opacity=0)
		path.set_stroke(WHITE, 1)
		return path