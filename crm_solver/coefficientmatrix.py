import numpy
from crm_solver import inputs
from crm_solver.rates import Rates


class CoefficientMatrix:
    def __init__(self, inputs):
        self.inputs = inputs
        self.rates = Rates(self.inputs)
        self.matrix = self.assemble()

    def assemble(self):
        coefficient_matrix = numpy.zeros(
            (self.inputs.number_of_levels, self.inputs.number_of_levels, len(self.inputs.steps)))
        for from_level in range(self.inputs.number_of_levels):
            for to_level in range(self.inputs.number_of_levels):
                for step in range(len(self.inputs.steps)):
                    if to_level == from_level:
                        electron_terms = sum(self.rates.electron_neutral_collisions[from_level, :from_level, step]) + sum(
                            self.rates.electron_neutral_collisions[from_level, from_level + 1:self.inputs.number_of_levels, step]) + \
                            self.rates.electron_loss_collisions[0, from_level, step]
                        ion_terms = sum(self.rates.proton_neutral_collisions[from_level, :from_level, step]) + sum(
                            self.rates.proton_neutral_collisions[from_level, from_level + 1:self.inputs.number_of_levels, step]) + \
                            self.rates.electron_loss_collisions[1, from_level, step]
                        photon_terms = sum(self.rates.einstein_coeffs[:, from_level]) / self.rates.velocity
                        coefficient_matrix[from_level, from_level, step] = -self.inputs.density[step] * electron_terms \
                                                      - self.inputs.density[step] * ion_terms \
                                                      - photon_terms
                    else:
                        coefficient_matrix[from_level, to_level, step] = self.inputs.density[step] \
                                                      * self.rates.electron_neutral_collisions[to_level, from_level, step] \
                                                      + self.inputs.density[step] \
                                                      * self.rates.proton_neutral_collisions[to_level, from_level, step] \
                                                      + self.rates.einstein_coeffs[from_level, to_level] / self.rates.velocity
        return coefficient_matrix
