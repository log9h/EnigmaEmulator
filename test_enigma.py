import unittest
from components import *
from machine import *
from presets import *


class TestRotor(unittest.TestCase):
    def setUp(self):
        self.rotor = Rotor(wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch="Q")

    def test_initial_position(self):
        self.assertEqual(self.rotor.position, 1)

    def test_rotation(self):
        self.rotor.rotate()
        self.assertEqual(self.rotor.position, 2)
        for _ in range(24):  # (total 25 rotations)
            self.rotor.rotate()
        self.assertEqual(self.rotor.position, 26)
        self.rotor.rotate()  # expected wrap around
        self.assertEqual(self.rotor.position, 1)

    def test_forward_mapping(self):
        self.assertEqual(self.rotor.forward('A'), 'E')
        self.assertEqual(self.rotor.forward('B'), 'K')
        self.assertEqual(self.rotor.forward('C'), 'M')

    def test_backward_mapping(self):
        self.assertEqual(self.rotor.backward('E'), 'A')
        self.assertEqual(self.rotor.backward('K'), 'B')
        self.assertEqual(self.rotor.backward('M'), 'C')

    def test_ring_setting(self):
        rotor = Rotor(wiring="EKMFLGDQVZNTOWYHXUSPAIBRCJ", notch="Q", ring_setting=2)
        self.assertEqual(rotor.forward('A'), 'K')
        self.assertEqual(rotor.backward('J'), 'W')


class TestReflector(unittest.TestCase):
    def setUp(self):
        self.reflector = Reflector(wiring="YRUHQSLDPXNGOKMIEBFZCWVJAT")

    def test_reflection(self):
        # Test known reflections for Reflector B
        self.assertEqual(self.reflector.reflect('A'), 'Y')
        self.assertEqual(self.reflector.reflect('B'), 'R')
        self.assertEqual(self.reflector.reflect('Y'), 'A')
        self.assertEqual(self.reflector.reflect('R'), 'B')


class TestPlugboard(unittest.TestCase):
    def setUp(self):
        self.plugboard = Plugboard(connections={'A': 'B', 'C': 'D'})

    def test_plugboard_mapping(self):
        self.assertEqual(self.plugboard.process('A'), 'B')
        self.assertEqual(self.plugboard.process('B'), 'A')
        self.assertEqual(self.plugboard.process('C'), 'D')
        self.assertEqual(self.plugboard.process('D'), 'C')
        self.assertEqual(self.plugboard.process('E'), 'E') # Unconnected


class TestEnigmaMachine(unittest.TestCase):
    def setUp(self):
        rotors = [
            EnigmaPresets.get_rotor('III', position=1),
            EnigmaPresets.get_rotor('II', position=1),
            EnigmaPresets.get_rotor('I', position=1)
        ]
        reflector = EnigmaPresets.get_reflector('B')
        plugboard = Plugboard()
        self.machine = EnigmaMachine(rotors, reflector, plugboard)

    def test_single_letter_encryption(self):
        self.machine.set_rotor_positions([1, 1, 1])  # AAA
        self.assertEqual(self.machine.encrypt_char('A'), 'F')

    def test_message_encryption(self):
        self.machine.set_rotor_positions([1, 1, 1])  # AAA
        encrypted = self.machine.encrypt("HELLOWORLD")
        self.assertEqual(encrypted, "MFNCZBBFZM")

    def test_decryption(self):
        self.machine.set_rotor_positions([1, 1, 1])  # AAA
        encrypted = self.machine.encrypt("HELLOWORLD")

        self.machine.set_rotor_positions([1, 1, 1])
        decrypted = self.machine.encrypt(encrypted)
        self.assertEqual(decrypted, "HELLOWORLD")

    def test_rotor_stepping(self):
        self.machine.set_rotor_positions([1, 1, 1])  # AAA

        self.machine.encrypt_char('A') # expected AAB after
        self.assertEqual(self.machine.rotors[0].position, 1)
        self.assertEqual(self.machine.rotors[1].position, 1)
        self.assertEqual(self.machine.rotors[2].position, 2)

    def test_double_stepping(self):
        self.machine.set_rotor_positions([1, 5, 22])
        self.machine.encrypt_char('A')

        self.assertEqual(self.machine.rotors[0].position, 1)
        self.assertEqual(self.machine.rotors[1].position, 5)
        self.assertEqual(self.machine.rotors[2].position, 23)


class TestEnigmaPresets(unittest.TestCase):
    def test_rotor_presets(self):
        rotor_i = EnigmaPresets.get_rotor('I')
        self.assertEqual(rotor_i.forward('A'), 'E')
        self.assertEqual(rotor_i.notch, 'Q')

        rotor_ii = EnigmaPresets.get_rotor('II')
        self.assertEqual(rotor_ii.forward('A'), 'A')
        self.assertEqual(rotor_ii.notch, 'E')

    def test_reflector_presets(self):
        reflector_b = EnigmaPresets.get_reflector('B')
        self.assertEqual(reflector_b.reflect('A'), 'Y')
        self.assertEqual(reflector_b.reflect('Y'), 'A')


if __name__ == '__main__':
    unittest.main()