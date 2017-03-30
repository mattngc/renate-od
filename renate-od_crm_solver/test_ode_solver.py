from unittest import TestCase
from ode_solver import ode_solver
import numpy
import math


class TestOde_solver(TestCase):
    pop = numpy.zeros(2)
    pop[0] = 1
    c = numpy.zeros((2, 2))
    c[0, 1] = 2
    c[0, 0] = 1
    initial_condition = numpy.zeros(2)
    initial_condition[0] = 1
    initial_condition[1] = 0
    interval = 100
    number_of_steps = 5
    steps = numpy.linspace(0, interval, number_of_steps)
    coefficient_matrix = numpy.zeros((2, 2))
    coefficient_matrix[0, 0] = -2
    coefficient_matrix[0, 1] = 0
    coefficient_matrix[1, 0] = 0
    coefficient_matrix[1, 1] = 5
    onedim_matrix=numpy.zeros((1,1))
    onedim_matrix[0,0]=2
    onedim_init=numpy.zeros(1)
    onedim_init[0]=1


    def test_set_up_equation(self):
        s = ode_solver.set_up_equation(variable_vector=self.initial_condition, calculation_point=self.steps,coefficient_matrix=self.coefficient_matrix)
        self.assertEqual(2, s.size)

    def test_size_of_solution(self):
        s = ode_solver.calculate_solution(ode_solver.set_up_equation,self.initial_condition,self.steps,coefficient_matrix=self.coefficient_matrix)
        self.assertEqual(s.size, self.number_of_steps * self.initial_condition.size)

    def test_1d_analytical(self):
        solution=ode_solver.analytical_solution(self.onedim_init,self.steps,self.onedim_matrix)
        for i in range(self.steps.size):
            self.assertEqual(solution[i],self.onedim_init*numpy.exp(self.onedim_matrix*self.steps[i]))

    def test_diagonal_numerical(self):
        solution = ode_solver.calculate_solution(ode_solver.set_up_equation,self.initial_condition, self.steps, self.coefficient_matrix)
        for i in range(self.steps.size):
            for j in range(self.initial_condition.size):
                self.assertAlmostEqual(solution[i, j], (self.initial_condition[j] * numpy.exp(self.coefficient_matrix[j, j] * self.steps[i])), 6)

    def test_diagonal_analytical(self):
        solution=ode_solver.analytical_solution(self.initial_condition,self.steps,self.coefficient_matrix)
        for i in range(self.steps.size):
            for j in range(self.initial_condition.size):
                self.assertAlmostEqual(solution[i,j],(self.initial_condition[j]*numpy.exp(self.coefficient_matrix[j,j]*self.steps[i])),100)

    def test_numerical_to_analytical(self):
        numerical=ode_solver.calculate_solution(ode_solver.set_up_equation,self.initial_condition, self.steps,self.coefficient_matrix)
        analytical=ode_solver.analytical_solution(self.initial_condition,self.steps,self.coefficient_matrix)
        for i in range(len(self.steps)):
            for j in range(self.initial_condition.size):
                self.assertAlmostEqual(numerical[i,j],analytical[i,j],6)

    def test_almostequal(self):
        self.assertAlmostEqual(1,1.004,2)