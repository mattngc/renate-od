from crm_solver.inputs import Inputs
from crm_solver.coefficientmatrix import CoefficientMatrix
from crm_solver.ode import Ode
import matplotlib.pyplot


class Solve:
    @staticmethod
    def solve_numerically(inputs):
        inp = inputs
        coeffmatrix = CoefficientMatrix(inp)
        ode_init = Ode(coefficient_matrix=coeffmatrix.matrix, initial_condition=inp.initial_condition, steps=inp.steps)
        numerical = ode_init.calculate_solution()
        return numerical

    def plot_populations(self):
        inp = Inputs()
        coeffmatrix = CoefficientMatrix()
        ode_init = Ode(coefficient_matrix=coeffmatrix.matrix, initial_condition=inp.initial_condition, steps=inp.steps)
        solutions=self.solve_numerically()
        for i in range(inp.number_of_levels):
            matplotlib.pyplot.plot(inp.steps, solutions[:, i], label=str(i))
            matplotlib.pyplot.yscale('log', nonposx='clip')
            matplotlib.pyplot.ylim((0, 1))
        matplotlib.pyplot.legend(loc='best')
        matplotlib.pyplot.xlabel('x')
        matplotlib.pyplot.grid()
        matplotlib.pyplot.show()

    def plot(self):
        inp = Inputs()
        coeffmatrix = CoefficientMatrix(inp)
        ode_init = Ode(coefficient_matrix=coeffmatrix.matrix, initial_condition=inp.initial_condition, steps=inp.steps)
        solutions = self.solve_numerically(inputs=inp)
        for i in range(inp.number_of_levels):
            matplotlib.pyplot.plot(inp.steps, solutions[:, i], label='lev'+str(i)+' scen1')
            matplotlib.pyplot.yscale('log', nonposx='clip')
            matplotlib.pyplot.ylim((0, 1))
        matplotlib.pyplot.legend(loc='center', bbox_to_anchor=(1,0.5), ncol=1)
        matplotlib.pyplot.xlabel('x')
        matplotlib.pyplot.grid()
        matplotlib.pyplot.show()


Solve.plot(Solve)