from manim import *

class Bloch2(ThreeDScene):

    def update_spring(self, m_1, m_2):
        def updater(m, dt):
            center_1 = m_1.get_center()
            center_2 = m_2.get_center()
            m.put_start_and_end_on(center_1, center_2)
        return updater

    def update_spring_left(self, m_1, Wall_1):
        def updater(m, dt):
            center_1 = m_1.get_center()
            m.put_start_and_end_on(Wall_1.get_center(), center_1)
        return updater

    def update_spring_right(self, m_2, Wall_2):
        def updater(m, dt):
            center_2 = m_2.get_center()
            m.put_start_and_end_on(center_2, Wall_2.get_center())
        return updater

    def update_angle(self, m, dt): 
        m.become(Angle(self.Xaxis, self.Paxis, color = GREEN))
        


    def mode(self, phase, Start, shift = 0*DOWN):
        def motion(t):
            A=0.5
            return A*np.array((np.cos(TAU*t + phase) + Start, 0, 0)) + shift
        return motion

    def spring_demo(self):
        eq_1 = DashedLine(1.5*UP+1.5*LEFT, 1.5*DOWN+1.5*LEFT, color = GREEN)
        eq_2 = DashedLine(1.5*UP+1.5*RIGHT, 1.5*DOWN+1.5*RIGHT, color = GREEN)
        self.add(eq_1, eq_2)
        m_1 = VGroup(Square(side_length=1.0, fill_opacity=1), Tex('$m$', color=BLACK)).shift(1*LEFT)
        m_2 = VGroup(Square(side_length=1.0, fill_opacity=1), Tex('$m$', color=BLACK)).shift(1*RIGHT)
        
        center_1 = m_1.get_center()
        center_2 = m_2.get_center()
        Wall_1 = Line(UP + 3*LEFT, DOWN + 3*LEFT)
        Wall_2 = Line(UP + 3*RIGHT, DOWN + 3*RIGHT)
        spring = DashedLine(center_1, center_2, color = BLUE)
        spring_left = DashedLine(3*LEFT, center_1, color = RED)
        spring_right = DashedLine(center_2, 3*RIGHT, color = RED)

        self.add(Wall_1, Wall_2, spring, spring_left, spring_right)
        spring.add_updater(self.update_spring(m_1, m_2))
        spring_left.add_updater(self.update_spring_left(m_1, Wall_1))
        spring_right.add_updater(self.update_spring_right(m_2, Wall_2))
        
        All = VGroup(eq_1, eq_2, m_1, m_2, Wall_1, Wall_2, spring, spring_left, spring_right)

        return m_1, m_2, All

    def construct(self):
        
        circle_1 = Circle(radius=2.0, color=WHITE)
        circle_2 = DashedVMobject(Circle(radius=2.0, color=WHITE), num_dashes=30)
        Zaxis = Line(0*UP, np.array((0, 0, 2)))
        theta = PI/6
        Angle_demo_line = Line(0*UP, 2*np.array((np.sin(theta), 0, np.cos(theta))))
        angle = Arc(radius=.5, start_angle=PI/2, angle=-theta, arc_center=np.array([0., 0., 0.])).set_color(BLUE)

        circle_2.rotate(axis = np.array((1, 0, 0)), angle = PI/2)
        angle.rotate(axis = np.array((1, 0, 0)), angle = PI/2, about_point = 0*UP)
        
        Bloch_sphere=Sphere(center=(0,0,0), radius=2,resolution=(10, 10)).set_opacity(0.3) 
        Bloch_sphere.set_color(GRAY) 
        state_dot = Sphere(2*np.array((np.sin(theta), 0, np.cos(theta))), radius=0.1,resolution=(5, 5)).set_color(RED)
        Paxis = Line(Bloch_sphere.get_center(), np.array((2 * np.cos(PI/100), 2 * np.sin(PI/100), 0)))
        self.Paxis = Paxis
        
        Bloch = VGroup(circle_1, circle_2, Zaxis, Angle_demo_line, angle, Bloch_sphere, state_dot, self.Paxis)
        self.Xaxis = Line(Bloch_sphere.get_center(), np.array((2, 0, 0))).shift(3*DOWN)
        PAngle = Angle(self.Paxis, self.Xaxis, color = GREEN).shift(3*RIGHT)
        PAngle.add_updater(lambda m, dt : self.update_angle(m, dt))
        self.add(PAngle)
        self.add(self.Xaxis)

        quantum_state = MathTex(
            r'\cos(\theta/2) \begin{bmatrix} 1 \\ 1\end{bmatrix} + e^{i\phi}\sin(\theta/2) \begin{bmatrix} 1 \\ -1\end{bmatrix}',
            substrings_to_isolate=(r'\theta', '\phi')
            )
        quantum_state.set_color_by_tex(r"\theta", BLUE)
        quantum_state.set_color_by_tex("\phi", GREEN)
        quantum_state.shift(3*RIGHT)
        self.add_fixed_in_frame_mobjects(quantum_state)


        self.set_camera_orientation(phi=70* DEGREES, theta=0 * DEGREES)
        self.play(Rotate(Bloch.shift(3*DOWN), 
            angle = TAU, 
            axis = np.array((0, 0, 1))),
            run_time = 10,
            rate_func = linear
            )

        
        