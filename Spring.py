from manim import config
from manim import *

class Spring(Scene):

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
        shift_1 = 1.5*UP
        m_1, m_2, All_1 = self.spring_demo()
        func_1 = ParametricFunction(self.mode(0, -3, shift = shift_1), t_range = np.array([0, 0.5]))
        func_2 = ParametricFunction(self.mode(PI, 3, shift = shift_1), t_range = np.array([0, 0.5]))
        All_1.shift(shift_1)

        shift_2 = 1.5*DOWN
        m_3, m_4, All_2 = self.spring_demo()
        func_3 = ParametricFunction(self.mode(0, -3, shift=shift_2), t_range = np.array([0, 0.5]))
        func_4 = ParametricFunction(self.mode(0, 3, shift=shift_2), t_range = np.array([0, 0.5]))
        All_2.shift(shift_2)


        m_1eff = VGroup(Square(side_length=1.0, fill_opacity=1), Tex('$m$', color=BLACK)).shift(6*LEFT+shift_1)
        m_2eff = VGroup(Square(side_length=1.0, fill_opacity=1), Tex('$2m$', color=BLACK)).shift(6*LEFT+shift_2)

        Wall_3 = Line(UP + 4*LEFT, DOWN + 4*LEFT).shift(shift_1)
        Wall_4 = Line(UP + 4*LEFT, DOWN + 4*LEFT).shift(shift_2)
        k = Tex('$k$').shift(4.7*LEFT+shift_1+0.5*UP)
        k2 = Tex('$2k$').shift(4.7*LEFT+shift_1-0.5*UP)
        k3 = Tex('$2k$').shift(4.7*LEFT+shift_2+0.5*UP)
        k4 = Tex('$0$').shift(4.7*LEFT+shift_2-0.5*UP)
        spring3 = DashedLine(4*LEFT + 0.25*UP, 6*LEFT+0.25*UP, color = RED).shift(shift_1)
        spring4 = DashedLine(4*LEFT + 0.25*UP, 6*LEFT+0.25*UP, color = RED).shift(shift_2)
        spring5 = DashedLine(4*LEFT - 0.25*UP, 6*LEFT-0.25*UP, color = BLUE).shift(shift_1)
        spring6 = DashedLine(4*LEFT - 0.25*UP, 6*LEFT-0.25*UP, color = BLUE).shift(shift_2)
        self.add(Wall_3, Wall_4, spring3, spring4, spring5, spring6, m_1eff, m_2eff, k, k2, k3, k4)

        t_1 = Tex(r'$e^{i\omega_1 t}\begin{bmatrix} 1 \\ -1\end{bmatrix}$').shift(5*RIGHT + shift_1)
        t_2 = Tex(r'$e^{i\omega_2 t}\begin{bmatrix} 1 \\ +1\end{bmatrix}$').shift(5*RIGHT + shift_2)
        self.add(t_1, t_2)
        self.play(
            MoveAlongPath(m_3, func_3, rate_func = there_and_back), 
            MoveAlongPath(m_4, func_4, rate_func = there_and_back),
            MoveAlongPath(m_1, func_1, rate_func = there_and_back), 
            MoveAlongPath(m_2, func_2, rate_func = there_and_back), 
            run_time = 2
        )
        



        
        
        