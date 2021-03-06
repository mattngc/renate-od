from crm_solver.atomic_db import AtomicDB
from crm_solver.atomic_db import RenateDB
import unittest
import numpy
import scipy
import utility.convert as uc
import pandas


class RenateDBTest(unittest.TestCase):
    EXPECTED_ATTR = ['energy', 'param', 'species', 'mass', 'atomic_dict', 'rate_type', 'velocity',
                     'atomic_levels', 'inv_atomic_dict', 'impurity_mass_normalization', 'charged_states']
    EXPECTED_ATOM = ['dummy', 'Li', 'Na', 'T', 'H', 'D']
    EXPECTED_ATOMIC_LEVELS = [3, 9, 8, 6, 6, 6]
    EXPECTED_ENERGY = '60'
    EXPECTED_VELOCITY = 1291547.1348
    EXPECTED_MASS = 1.15258e-26
    EXPECTED_ATOMIC_DICT = [{'1': 1, '0': 0, '2': 2},
                            {'2s': 0, '2p': 1, '3s': 2, '3p': 3, '3d': 4, '4s': 5, '4p': 6, '4d': 7, '4f': 8},
                            {'3s': 0, '3p': 1, '3d': 2, '4s': 3, '4p': 4, '4d': 5, '4f': 6, '5s': 7},
                            {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5},
                            {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5},
                            {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5}]
    EXPECTED_MASS_CORRECTION_DICT = {'charge-1': 1, 'charge-2': 4, 'charge-3': 7, 'charge-4': 9, 'charge-5': 11,
                                     'charge-6': 12, 'charge-7': 14, 'charge-8': 16, 'charge-9': 19, 'charge-10': 20,
                                     'charge-11': 23}
    EXPECTED_DEFAULT_ATOMIC_STATES = [['1', '0', '0', '1-0'],
                                      ['2p', '2s', '2s', '2p-2s'],
                                      ['3p', '3s', '3s', '3p-3s'],
                                      ['3', '2', '1', '3-2'],
                                      ['3', '2', '1', '3-2'],
                                      ['3', '2', '1', '3-2']]
    INPUT_PATH = 'beamlet/testimp0001.xml'
    INPUT_DATA_GETTING = ['temperature', 'spontaneous_transition', 'ionization_terms',
                          'impurity_transition', 'ion_transition', 'electron_transition']

    def test_all_attributes(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        for attr in self.EXPECTED_ATTR:
            assert hasattr(actual, attr)

    def test_projectile_energy(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        self.assertIsInstance(actual.energy, str)
        self.assertEqual(actual.energy, self.EXPECTED_ENERGY)

    def test_impurity_mass_correction_dictionary(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        self.assertIsInstance(actual.impurity_mass_normalization, dict)
        self.assertDictEqual(actual.impurity_mass_normalization, self.EXPECTED_MASS_CORRECTION_DICT)

    def test_projectile_mass(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        self.assertIsInstance(actual.mass, float)
        self.assertEqual(actual.mass, self.EXPECTED_MASS)

    def test_projectile_velocity(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        self.assertIsInstance(actual.velocity, float)
        self.assertAlmostEqual(actual.velocity, self.EXPECTED_VELOCITY, 3)

    def test_atomic_species(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        self.assertIsInstance(actual.species, str)
        self.assertIn(actual.species, self.EXPECTED_ATOM)
        self.assertIsInstance(actual.species, str)

    def test_atomic_levels(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        for index in range(len(self.EXPECTED_ATOM)):
            actual.param.getroot().find('body').find('beamlet_species').text = self.EXPECTED_ATOM[index]
            atom = RenateDB(actual.param, 'default', None)
            self.assertIsInstance(atom.atomic_levels, int)
            self.assertEqual(atom.atomic_levels, self.EXPECTED_ATOMIC_LEVELS[index])
            self.assertIsInstance(atom.atomic_dict, dict)
            self.assertDictEqual(atom.atomic_dict, self.EXPECTED_ATOMIC_DICT[index])
            self.assertIsInstance(atom.inv_atomic_dict, dict)

    def test_default_atomic_levels(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        for index in range(len(self.EXPECTED_ATOM)):
            actual.param.getroot().find('body').find('beamlet_species').text = self.EXPECTED_ATOM[index]
            atom = RenateDB(actual.param, 'default', None)
            fr, to, ground, trans = atom.set_default_atomic_levels()
            self.assertIsInstance(fr, str)
            self.assertEqual(fr, self.EXPECTED_DEFAULT_ATOMIC_STATES[index][0])
            self.assertIsInstance(to, str)
            self.assertEqual(to, self.EXPECTED_DEFAULT_ATOMIC_STATES[index][1])
            self.assertIsInstance(ground, str)
            self.assertEqual(ground, self.EXPECTED_DEFAULT_ATOMIC_STATES[index][2])
            self.assertIsInstance(trans, str)
            self.assertEqual(trans, self.EXPECTED_DEFAULT_ATOMIC_STATES[index][3])

    def test_atomic_data_getter(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        for index in range(len(self.INPUT_DATA_GETTING)):
            data = actual.get_from_renate_atomic(self.INPUT_DATA_GETTING[index])
            self.assertIsInstance(data, numpy.ndarray)

    def test_charged_state_library(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        self.assertIsInstance(actual.charged_states, tuple)
        for state in range(len(actual.charged_states)):
            self.assertIsInstance(actual.charged_states[state], str)
            self.assertEqual(actual.charged_states[state], 'charge-'+str(state+1))

    def test_renate_temperature(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        data = actual.get_from_renate_atomic('temperature')
        self.assertEqual(data.ndim, 1)

    def test_renate_spontaneous(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        data = actual.get_from_renate_atomic('spontaneous_transition')
        self.assertEqual(data.ndim, 2)
        self.assertEqual(data.shape, (actual.atomic_levels, actual.atomic_levels))

    def test_renate_electron_transitions(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        temp = actual.get_from_renate_atomic('temperature')
        data = actual.get_from_renate_atomic('electron_transition')
        self.assertEqual(data.ndim, 3)
        self.assertEqual(data.shape, (actual.atomic_levels, actual.atomic_levels, len(temp)))

    def test_renate_ion_transitions(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        temp = actual.get_from_renate_atomic('temperature')
        data = actual.get_from_renate_atomic('ion_transition')
        self.assertEqual(data.ndim, 3)
        self.assertEqual(data.shape, (actual.atomic_levels, actual.atomic_levels, len(temp)))

    def test_renate_impurity_transitions(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        temp = actual.get_from_renate_atomic('temperature')
        data = actual.get_from_renate_atomic('impurity_transition')
        self.assertEqual(data.ndim, 4)
        self.assertEqual(data.shape, (len(actual.charged_states)-1, actual.atomic_levels,
                                      actual.atomic_levels, len(temp)))

    def test_renate_ionization_terms(self):
        actual = RenateDB(None, 'default', self.INPUT_PATH)
        temp = actual.get_from_renate_atomic('temperature')
        data = actual.get_from_renate_atomic('ionization_terms')
        self.assertEqual(data.ndim, 3)
        self.assertEqual(data.shape, (len(actual.charged_states)+1, actual.atomic_levels, len(temp)))


class AtomicDBTest(unittest.TestCase):
    EXPECTED_ATTR = ['temperature_axis', 'spontaneous_trans', 'electron_impact_loss',
                     'ion_impact_loss', 'electron_impact_trans', 'ion_impact_trans']
    elements = ['1H+', '1D+', '3He+', '4He++', '9Be++++']
    q = [1, 1, 1, 2, 4]
    z = [1, 1, 2, 2, 4]
    a = [1, 2, 3, 4, 9]
    COMPONENTS = pandas.DataFrame([[-1] + q, [0] + z, [0] + a], index=['q', 'Z', 'A'],
                                  columns=['electron'] + ['ion' + str(i + 1) for i in
                                  range(len(elements))]).transpose()
    INPUT_DUMMY_PATH = 'beamlet/dummy0001.xml'
    INTERPOLATION_TEST_TEMPERATURE = [0, 1, 2, 2.5, 3, 8, 10]
    EXPECTED_ELECTRON_IMPACT_LOSS = uc.convert_from_cm2_to_m2(numpy.asarray(
                                                              [[11., 111., 211., 261., 311., 811., 1011.],
                                                               [21., 121., 221., 271., 321., 821., 1021.],
                                                               [31., 131., 231., 281., 331., 831., 1031.]]))
    EXPECTED_ELECTRON_IMPACT_TRANS = uc.convert_from_cm2_to_m2(numpy.asarray(
                                                               [[[0.,    0.,   0.,   0.,   0.,   0.,    0.],
                                                                 [12., 112., 212., 262., 312., 812., 1012.],
                                                                 [13., 113., 213., 263., 313., 813., 1013.]],
                                                                [[21., 121., 221., 271., 321., 821., 1021.],
                                                                 [0.,    0.,   0.,   0.,   0.,   0.,    0.],
                                                                 [23., 123., 223., 273., 323., 823., 1023.]],
                                                                [[31., 131., 231., 281., 331., 831., 1031.],
                                                                 [32., 132., 232., 282., 332., 832., 1032.],
                                                                 [0.,    0.,   0.,   0.,   0.,   0.,    0.]]]))
    EXPECTED_ION_IMPACT_LOSS = uc.convert_from_cm2_to_m2(numpy.asarray(
                                                         [[[12., 112., 212., 262., 312., 812., 1012.],
                                                           [12.,  62., 112., 137., 162., 412.,  512.],
                                                           [12., 45.333, 78.666, 95.333, 112., 278.666, 345.333],
                                                           [13., 113., 213., 263., 313., 813., 1013.],
                                                           [15., 115., 215., 265., 315., 815., 1015.]],
                                                          [[22., 122., 222., 272., 322., 822., 1022.],
                                                           [22.,  72., 122., 147., 172., 422.,  522.],
                                                           [22., 55.333, 88.666, 105.333, 122., 288.666, 355.333],
                                                           [23., 123., 223., 273., 323., 823., 1023.],
                                                           [25., 125., 225., 275., 325., 825., 1025.]],
                                                          [[32., 132., 232., 282., 332., 832., 1032.],
                                                           [32.,  82., 132., 157., 182., 432.,  532.],
                                                           [32., 65.333, 98.666, 115.333, 132., 298.666, 365.333],
                                                           [33., 133., 233., 283., 333., 833., 1033.],
                                                           [35., 135., 235., 285., 335., 835., 1035.]]]))
    EXPECTED_ION_IMPACT_TRANS = uc.convert_from_cm2_to_m2(numpy.asarray(
                                                          [[[[0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.]],
                                                            [[12.,   112.,  212.,  262.,  312.,  812.,  1012.],
                                                             [12.,    62., 112.,   137.,  162.,  412.,   512.],
                                                             [12., 45.333, 78.666, 95.333, 112., 278.666, 345.333],
                                                             [121., 1121., 2121., 2621., 3121., 8121., 10121.],
                                                             [123., 1123., 2123., 2623., 3123., 8123., 10123.]],
                                                            [[13.,   113.,  213.,  263.,  313.,  813.,  1013.],
                                                             [13.,    63.,  113.,  138.,  163.,  413.,   513.],
                                                             [13., 46.333, 79.666, 96.333, 113., 279.666, 346.333],
                                                             [131., 1131., 2131., 2631., 3131., 8131., 10131.],
                                                             [133., 1133., 2133., 2633., 3133., 8133., 10133.]]],
                                                           [[[21.,   121.,  221.,  271.,  321.,  821.,  1021.],
                                                             [21.,    71.,  121.,  146.,  171.,  421.,   521.],
                                                             [21., 54.333, 87.666, 104.333, 121., 287.666, 354.333],
                                                             [211., 1211., 2211., 2711., 3211., 8211., 10211.],
                                                             [213., 1213., 2213., 2713., 3213., 8213., 10213.]],
                                                            [[0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.]],
                                                            [[23.,   123.,  223.,  273.,  323.,  823.,  1023.],
                                                             [23.,    73.,  123.,  148.,  173.,  423.,   523.],
                                                             [23., 56.333, 89.666, 106.333, 123., 289.666, 356.333],
                                                             [231., 1231., 2231., 2731., 3231., 8231., 10231.],
                                                             [233., 1233., 2233., 2733., 3233., 8233., 10233.]]],
                                                           [[[31.,   131.,  231.,  281.,  331.,  831.,  1031.],
                                                             [31.,    81.,  131.,  156.,  181.,  431.,   531.],
                                                             [31., 64.333, 97.666, 114.333, 131., 297.666, 364.333],
                                                             [311., 1311., 2311., 2811., 3311., 8311., 10311.],
                                                             [313., 1313., 2313., 2813., 3313., 8313., 10313.]],
                                                            [[32.,   132.,  232.,  282.,  332.,  832.,  1032.],
                                                             [32.,    82.,  132.,  157.,  182.,  432.,   532.],
                                                             [32., 65.333, 98.666, 115.333, 132., 298.666, 365.333],
                                                             [321., 1321., 2321., 2821., 3321., 8321., 10321.],
                                                             [323., 1323., 2323., 2823., 3323., 8323., 10323.]],
                                                            [[0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.],
                                                             [0., 0., 0., 0., 0., 0., 0.]]]]))

    def test_all_attributes(self):
        actual = AtomicDB(components=self.COMPONENTS)
        for attr in self.EXPECTED_ATTR:
            assert hasattr(actual, attr)

    def test_inheritance(self):
        atomic_db = AtomicDB(data_path=self.INPUT_DUMMY_PATH, components=self.COMPONENTS)
        self.assertIsInstance(atomic_db, RenateDB)

    def test_spontaneous_trans(self):
        actual = AtomicDB(components=self.COMPONENTS)
        self.assertIsInstance(actual.spontaneous_trans, numpy.ndarray)
        self.assertEqual(actual.spontaneous_trans.ndim, 2)
        self.assertEqual(actual.atomic_levels, int(actual.spontaneous_trans.size ** 0.5))
        for to_level in range(actual.atomic_levels):
            for from_level in range(actual.atomic_levels):
                if from_level <= to_level:
                    self.assertEqual(actual.spontaneous_trans[to_level, from_level],
                                     0.0, msg='Spontaneous transition levels set wrong!!')

    def test_electron_impact_loss_terms(self):
        actual = AtomicDB(components=self.COMPONENTS)
        self.assertIsInstance(actual.electron_impact_loss, tuple)
        self.assertEqual(len(actual.electron_impact_loss), actual.atomic_levels)
        for index in range(actual.atomic_levels):
            self.assertIsInstance(actual.electron_impact_loss[index], scipy.interpolate.interp1d)

    def test_electron_impact_transition_terms(self):
        actual = AtomicDB(components=self.COMPONENTS)
        self.assertIsInstance(actual.electron_impact_trans, tuple)
        self.assertEqual(len(actual.electron_impact_trans), actual.atomic_levels)
        for from_level in range(actual.atomic_levels):
            self.assertIsInstance(actual.electron_impact_trans[from_level], tuple)
            self.assertEqual(len(actual.electron_impact_trans[from_level]), actual.atomic_levels)
            for to_level in range(actual.atomic_levels):
                self.assertIsInstance(actual.electron_impact_trans[from_level][to_level], scipy.interpolate.interp1d)

    def test_ion_impact_loss_terms(self):
        actual = AtomicDB(components=self.COMPONENTS)
        self.assertIsInstance(actual.ion_impact_loss, tuple)
        self.assertEqual(len(actual.ion_impact_loss), actual.atomic_levels)
        for from_level in range(actual.atomic_levels):
            self.assertIsInstance(actual.ion_impact_loss[from_level], tuple)
            self.assertEqual(len(actual.ion_impact_loss[from_level]), len(actual.components.T.keys())-1)
            for charge in range(len(actual.components.T.keys())-1):
                self.assertIsInstance(actual.ion_impact_loss[from_level][charge], scipy.interpolate.interp1d)

    def test_ion_impact_transition_terms(self):
        actual = AtomicDB(components=self.COMPONENTS)
        self.assertIsInstance(actual.ion_impact_trans, tuple)
        self.assertEqual(len(actual.ion_impact_trans), actual.atomic_levels)
        for from_level in range(actual.atomic_levels):
            self.assertIsInstance(actual.ion_impact_trans[from_level], tuple)
            self.assertEqual(len(actual.ion_impact_trans[from_level]), actual.atomic_levels)
            for to_level in range(actual.atomic_levels):
                self.assertIsInstance(actual.ion_impact_trans[from_level][to_level], tuple)
                self.assertEqual(len(actual.ion_impact_trans[from_level][to_level]), len(actual.components.T.keys())-1)
                for charge in range(len(actual.components.T.keys())-1):
                    self.assertIsInstance(actual.ion_impact_trans[from_level][to_level][charge],
                                          scipy.interpolate.interp1d)

    def test_electron_impact_loss_interpolator(self):
        actual = AtomicDB(data_path=self.INPUT_DUMMY_PATH, components=self.COMPONENTS)
        for level in range(actual.atomic_levels):
            rates = actual.electron_impact_loss[level](self.INTERPOLATION_TEST_TEMPERATURE)
            self.assertIsInstance(rates, numpy.ndarray)
            for element_index in range(len(rates)):
                self.assertAlmostEqual(self.EXPECTED_ELECTRON_IMPACT_LOSS[level]
                                       [element_index], rates[element_index], 5)

    def test_electron_impact_transition_interpolator(self):
        actual = AtomicDB(data_path=self.INPUT_DUMMY_PATH, components=self.COMPONENTS)
        for from_level in range(actual.atomic_levels):
            for to_level in range(actual.atomic_levels):
                rates = actual.electron_impact_trans[from_level][to_level](self.INTERPOLATION_TEST_TEMPERATURE)
                self.assertIsInstance(rates, numpy.ndarray)
                for element_index in range(len(rates)):
                    self.assertAlmostEqual(self.EXPECTED_ELECTRON_IMPACT_TRANS[from_level]
                                           [to_level][element_index], rates[element_index], 5)

    def test_ion_impact_loss_interpolator(self):
        actual = AtomicDB(data_path=self.INPUT_DUMMY_PATH, components=self.COMPONENTS)
        for level in range(actual.atomic_levels):
            for target in range(len(actual.components.T.keys())-1):
                rates = actual.ion_impact_loss[level][target](self.INTERPOLATION_TEST_TEMPERATURE)
                self.assertIsInstance(rates, numpy.ndarray)
                for element_index in range(len(rates)):
                    self.assertAlmostEqual(self.EXPECTED_ION_IMPACT_LOSS[level][target]
                                           [element_index], rates[element_index], 3)

    def test_ion_impact_transition_interpolator(self):
        actual = AtomicDB(data_path=self.INPUT_DUMMY_PATH, components=self.COMPONENTS)
        for from_level in range(actual.atomic_levels):
            for to_level in range(actual.atomic_levels):
                for target in range(len(actual.components.T.keys())-1):
                    rates = actual.ion_impact_trans[from_level][to_level][target](self.INTERPOLATION_TEST_TEMPERATURE)
                    self.assertIsInstance(rates, numpy.ndarray)
                    for element_index in range(len(rates)):
                        self.assertAlmostEqual(self.EXPECTED_ION_IMPACT_TRANS[from_level]
                                               [to_level][target][element_index], rates[element_index], 3)
