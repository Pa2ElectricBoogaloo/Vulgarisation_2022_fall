from manim import *

class Spring_Math(ThreeDScene):
    def construct(self):
        title = Title("Combinaison linéaire")
        quantum_state = Tex(r'$A\cos(\omega_2 t)\begin{bmatrix} 1 \\ 1\end{bmatrix} + B \cos(\omega_1 t)\begin{bmatrix} 1 \\ -1\end{bmatrix}$').shift(UP)
        quantum_state2 = Tex(r'$R\cos(\theta/2) e^{i \omega_2 t}\begin{bmatrix} 1 \\ 1\end{bmatrix} + R \sin(\theta/2) e^{i \omega_1 t}\begin{bmatrix} 1 \\ -1\end{bmatrix}$').shift(DOWN)
        quantum_state3 = Tex(r'$R e^{i \omega_2 t}\left(\cos(\theta/2) \begin{bmatrix} 1 \\ 1\end{bmatrix} + \sin(\theta/2) e^{i (\omega_1-\omega_2) t}\begin{bmatrix} 1 \\ -1\end{bmatrix}\right)$').shift(3*DOWN)
        self.add(title, quantum_state, quantum_state2, quantum_state3)