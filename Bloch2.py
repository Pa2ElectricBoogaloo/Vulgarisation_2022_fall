from manim import *

class Bloch3(ThreeDScene):

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


    def mode(self, phase, Start, shift = 0*DOWN):
        def motion(t):
            A=0.5
            return A*np.array((np.cos(TAU*t) + Start, 0, 0)) + shift + A*np.array((np.cos(2*(TAU*t) + phase), 0, 0)) 
        return motion

    def spring_demo(self):
        eq_1 = DashedLine(1.5*UP+1.5*LEFT, 1.5*DOWN+1.5*LEFT, color = GREEN)
        eq_2 = DashedLine(1.5*UP+1.5*RIGHT, 1.5*DOWN+1.5*RIGHT, color = GREEN)
        self.add_fixed_in_frame_mobjects(eq_1, eq_2)
        m_1 = VGroup(Square(side_length=1.0, fill_opacity=1), Tex('$m$', color=BLACK)).shift(1*LEFT)
        m_2 = VGroup(Square(side_length=1.0, fill_opacity=1), Tex('$m$', color=BLACK)).shift(1*RIGHT)
        self.add_foreground_mobjects(m_1, m_2)
        center_1 = m_1.get_center()
        center_2 = m_2.get_center()
        Wall_1 = Line(UP + 3*LEFT, DOWN + 3*LEFT)
        Wall_2 = Line(UP + 3*RIGHT, DOWN + 3*RIGHT)
        spring = DashedLine(center_1, center_2, color = BLUE)
        spring_left = DashedLine(3*LEFT, center_1, color = RED)
        spring_right = DashedLine(center_2, 3*RIGHT, color = RED)

        self.add_fixed_in_frame_mobjects(Wall_1, Wall_2, spring, spring_left, spring_right)
        spring.add_updater(self.update_spring(m_1, m_2))
        spring_left.add_updater(self.update_spring_left(m_1, Wall_1))
        spring_right.add_updater(self.update_spring_right(m_2, Wall_2))
        
        All = VGroup(eq_1, eq_2, m_1, m_2, Wall_1, Wall_2, spring, spring_left, spring_right)

        return m_1, m_2, All

    def construct(self):
        
        circle_1 = Circle(radius=2.0, color=WHITE)
        circle_2 = DashedVMobject(Circle(radius=2.0, color=WHITE), num_dashes=30)
        Zaxis = Line(0*UP, np.array((0, 0, 2)))
        theta = PI/2
        Angle_demo_line = Line(0*UP, 2*np.array((np.sin(theta), 0, np.cos(theta))))
        angle = Arc(radius=.5, start_angle=PI/2, angle=-theta, arc_center=np.array([0., 0., 0.]))

        circle_2.rotate(axis = np.array((1, 0, 0)), angle = PI/2)
        angle.rotate(axis = np.array((1, 0, 0)), angle = PI/2, about_point = 0*UP)
        
        Bloch_sphere=Sphere(center=(0,0,0), radius=2,resolution=(10, 10)).set_opacity(0.3) 
        Bloch_sphere.set_color(GRAY) 
        state_dot = Sphere(2*np.array((np.sin(theta), 0, np.cos(theta))), radius=0.3,resolution=(5, 5)).set_color(RED).set_opacity(2)
        Paxis = Line(Bloch_sphere.get_center(), np.array((2, 0, 0)))
        self.Paxis = DashedVMobject(Paxis)
        PAngle = Arc(radius=.5, start_angle=0, angle=0, arc_center=np.array([0., 0., 0.])).shift(3*RIGHT)
        
        Bloch = VGroup(circle_1, circle_2, Zaxis, Angle_demo_line, angle, Bloch_sphere, state_dot, self.Paxis).scale(0.5)
        

        quantum_state = Tex(r'$\dfrac{\sqrt{2}}{2} \begin{bmatrix} 1 \\ 1\end{bmatrix} + e^{i(\omega_1-\omega_2)t}\dfrac{\sqrt{2}}{2} \begin{bmatrix} 1 \\ -1\end{bmatrix}$')
        quantum_state.shift(3*RIGHT + 2*UP).scale(0.8)
        self.add_fixed_in_frame_mobjects(quantum_state)

        shift_1 = 1.5*DOWN
        m_1, m_2, All_1 = self.spring_demo()
        func_1 = ParametricFunction(self.mode(0, -3, shift = shift_1), t_range = np.array([0, 0.5]))
        func_2 = ParametricFunction(self.mode(PI, 3, shift = shift_1), t_range = np.array([0, 0.5]))
        func_3 = ParametricFunction(self.mode(0, -3, shift = shift_1), t_range = np.array([0.5, 1]))
        func_4 = ParametricFunction(self.mode(PI, 3, shift = shift_1), t_range = np.array([0.5, 1]))
        All_1.shift(shift_1)
        self.add_fixed_in_frame_mobjects(All_1)

        

        self.set_camera_orientation(phi=70* DEGREES, theta=0 * DEGREES)
        self.play(Rotate(Bloch.shift(3*DOWN + 2*np.array((0, 0, 1)), rate_func=linear),
            angle = TAU/2, 
            axis = np.array((0, 0, 1))),
            MoveAlongPath(m_1, func_1), 
            MoveAlongPath(m_2, func_2),
            run_time = 5, 
            )

        self.play(state_dot.animate.set_color(BLUE), run_time = 2)
        quantum_state2 = Tex(r'$\dfrac{\sqrt{2}}{2} \begin{bmatrix} 1 \\ 1\end{bmatrix} + \dfrac{\sqrt{2}}{2} \begin{bmatrix} 1 \\ -1\end{bmatrix}$')
        self.play(Create(quantum_state2))
        self.play(state_dot.animate.set_color(RED), run_time = 2)
        self.play(Uncreate(quantum_state2))

        self.play(Rotate(Bloch,
            angle = TAU/2, 
            axis = np.array((0, 0, 1)), rate_func = linear),
            MoveAlongPath(m_1, func_3), 
            MoveAlongPath(m_2, func_4),
            run_time = 5, 
            )

        self.play(state_dot.animate.set_color(BLUE), run_time = 2)
        self.play(state_dot.animate.set_color(RED), run_time = 2)
    
        

class Bloch4(ThreeDScene):

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


    def mode(self, phase, Start, shift = 0*DOWN):
        def motion(t):
            A=0.5
            return A*np.array((np.cos(TAU*t + phase) + Start, 0, 0)) + shift
        return motion

    def spring_demo(self):
        eq_1 = DashedLine(1.5*UP+1.5*LEFT, 1.5*DOWN+1.5*LEFT, color = GREEN)
        eq_2 = DashedLine(1.5*UP+1.5*RIGHT, 1.5*DOWN+1.5*RIGHT, color = GREEN)
        m_1 = VGroup(Square(side_length=1.0, fill_opacity=1), Tex('$m$', color=BLACK)).shift(1*LEFT)
        m_2 = VGroup(Square(side_length=1.0, fill_opacity=1), Tex('$m$', color=BLACK)).shift(1*RIGHT)
        self.add_foreground_mobjects(m_1, m_2)
        center_1 = m_1.get_center()
        center_2 = m_2.get_center()
        Wall_1 = Line(UP + 4*LEFT, DOWN + 4*LEFT)
        Wall_2 = Line(UP + 4*RIGHT, DOWN + 4*RIGHT)
        spring = DashedLine(center_1, center_2, color = BLUE)
        spring_left = DashedLine(3*LEFT, center_1, color = RED)
        spring_right = DashedLine(center_2, 3*RIGHT, color = RED)

        self.add_fixed_in_frame_mobjects(Wall_1, Wall_2, spring, spring_left, spring_right)
        spring.add_updater(self.update_spring(m_1, m_2))
        spring_left.add_updater(self.update_spring_left(m_1, Wall_1))
        spring_right.add_updater(self.update_spring_right(m_2, Wall_2))
        
        All = VGroup(m_1, m_2, Wall_1, Wall_2, spring, spring_left, spring_right)

        return m_1, m_2, All

    def construct(self):
        circle_1 = Circle(radius=2.0, color=WHITE)
        circle_2 = DashedVMobject(Circle(radius=2.0, color=WHITE), num_dashes=30)
        Zaxis = Line(0*UP, np.array((0, 0, 2)))
        Zaxis2 = Line(0*UP, np.array((0, 0, -2)))
        theta = 0

        circle_2.rotate(axis = np.array((1, 0, 0)), angle = PI/2)
        
        Bloch_sphere=Sphere(center=(0,0,0), radius=2,resolution=(10, 10)).set_opacity(0.3) 
        Bloch_sphere.set_color(GRAY) 
        state_dot = Sphere(2*np.array((np.sin(theta), 0, np.cos(theta))), radius=0.3,resolution=(5, 5)).set_color(RED).set_opacity(2)
        state_dot2 = Sphere(2*np.array((0, 0, -1)), radius=0.3,resolution=(5, 5)).set_color(RED).set_opacity(2)

        Bloch2 = VGroup(circle_1.copy(), circle_2.copy(), Bloch_sphere.copy(), state_dot2, Zaxis2).scale(0.5)
        Bloch = VGroup(circle_1, circle_2, Bloch_sphere, state_dot, Zaxis).scale(0.5)
        

        quantum_state = Tex(r'$\begin{bmatrix} 1 \\ 1\end{bmatrix} =\cos(0) \begin{bmatrix} 1 \\ 1\end{bmatrix} + \sin(0) \begin{bmatrix} 1 \\ -1\end{bmatrix}$')
        quantum_state.shift(3*RIGHT + 3*UP).scale(0.8)
        self.add_fixed_in_frame_mobjects(quantum_state)

        shift_1 = -1*DOWN + 3*RIGHT
        m_1, m_2, All_1 = self.spring_demo()
        func_1 = ParametricFunction(self.mode(0, -1.5, shift = shift_1), t_range = np.array([0, 0.5]))
        func_2 = ParametricFunction(self.mode(0, 1.5, shift = shift_1), t_range = np.array([0, 0.5]))
        All_1.shift(shift_1).scale(0.5)
        self.add_fixed_in_frame_mobjects(All_1)

        quantum_state = Tex(r'$\begin{bmatrix} 1 \\ 1\end{bmatrix} =\cos(0) \begin{bmatrix} 1 \\ 1\end{bmatrix} + \sin(0) \begin{bmatrix} 1 \\ -1\end{bmatrix}$')
        quantum_state.shift(3*RIGHT + 3*UP).scale(0.8)
        self.add_fixed_in_frame_mobjects(quantum_state)

        shift_2 = 2.5*DOWN + 3*RIGHT
        m_3, m_4, All_2 = self.spring_demo()
        func_3 = ParametricFunction(self.mode(0, -1.7, shift = shift_2), t_range = np.array([0, 0.5]))
        func_4 = ParametricFunction(self.mode(PI, 1.7, shift = shift_2), t_range = np.array([0, 0.5]))
        All_2.shift(shift_2).scale(0.5)
        self.add_fixed_in_frame_mobjects(All_2)

        quantum_state2 = Tex(r'$\begin{bmatrix} 1 \\ -1\end{bmatrix} =\cos(\pi/2) \begin{bmatrix} 1 \\ 1\end{bmatrix} + \sin(\pi/2) \begin{bmatrix} 1 \\ -1\end{bmatrix}$')
        quantum_state2.shift(3*RIGHT - 1*UP).scale(0.8)
        self.add_fixed_in_frame_mobjects(quantum_state2)


        self.set_camera_orientation(phi=70* DEGREES, theta=0 * DEGREES)
        self.play(Rotate(Bloch.shift(3*DOWN + 2*np.array((0, 0, 1))),
            angle = TAU, 
            axis = np.array((0, 0, 1)), rate_func = linear),
            Rotate(Bloch2.shift(3*DOWN - 2.2*np.array((0, 0, 1))),
            angle = TAU, 
            axis = np.array((0, 0, 1)), rate_func = linear),
            MoveAlongPath(m_1, func_1, rate_func=there_and_back), 
            MoveAlongPath(m_2, func_2, rate_func=there_and_back),
            MoveAlongPath(m_3, func_3, rate_func=there_and_back), 
            MoveAlongPath(m_4, func_4, rate_func=there_and_back),
            run_time = 5,
            )

        

        
        
        
        