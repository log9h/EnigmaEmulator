from components import *

class EnigmaPresets:
    @staticmethod
    def get_rotor(rotor_type: str, ring_setting: int = 1, position: int = 1) -> Rotor:
        rotors = {
            'I': ('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'),
            'II': ('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'),
            'III': ('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'),
            'IV': ('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'),
            'V': ('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'),
        }
        wiring, notch = rotors[rotor_type]
        return Rotor(wiring, notch, ring_setting, position)

    @staticmethod
    def get_reflector(reflector_type: str) -> Reflector:
        reflectors = {
            'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
            'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
            'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
        }
        return Reflector(reflectors[reflector_type])
