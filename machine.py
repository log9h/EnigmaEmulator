from components import *
from presets import *

class EnigmaMachine:
    def __init__(
            self,
            rotors: List[Rotor],
            reflector: Reflector,
            plugboard: Plugboard
    ):
        """
        Args:
            rotors: List of rotors (from left to right as seen from the operator)
            reflector: The reflector to use
            plugboard: The plugboard configuration
        """
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def set_rotor_positions(self, positions: List[int]):
        for rotor, pos in zip(self.rotors, positions):
            rotor.position = pos

    def set_ring_settings(self, settings: List[int]):
        for rotor, setting in zip(self.rotors, settings):
            rotor.ring_setting = setting

    def rotate_rotors(self):
        rotate_next = self.rotors[-1].rotate()

        # Check for double stepping and other notches
        for i in range(len(self.rotors) - 2, -1, -1):
            if rotate_next:
                rotate_next = self.rotors[i].rotate()

                # Double stepping mechanism
                if i == 1 and self.rotors[i].position == (ord(self.rotors[i].notch[0]) - ord('A') + 2) % 26:
                    rotate_next = True
            else:
                break

    def encrypt_char(self, char: str) -> str:
        # Convert to uppercase and validate
        char = char.upper()
        if char not in string.ascii_uppercase:
            return char

        self.rotate_rotors()

        # 1. char -> plugboard
        char = self.plugboard.process(char)

        # 2. char -> rotors (right to left)
        for rotor in reversed(self.rotors):
            char = rotor.forward(char)

        # 3. char -> reflector
        char = self.reflector.reflect(char)

        # 4. char -> rotors (left to right)
        for rotor in self.rotors:
            char = rotor.backward(char)

        # 5. char -> plugboard
        char = self.plugboard.process(char)

        return char

    def encrypt(self, text: str) -> str:
        return ''.join([self.encrypt_char(c) for c in text])


# Example usage
if __name__ == "__main__":
    # Create components for an Enigma M3 machine
    rotor1 = EnigmaPresets.get_rotor('III', ring_setting=1, position=1)
    rotor2 = EnigmaPresets.get_rotor('II', ring_setting=1, position=1)
    rotor3 = EnigmaPresets.get_rotor('I', ring_setting=1, position=1)
    reflector = EnigmaPresets.get_reflector('B')
    plugboard = Plugboard({'A': 'B', 'C': 'D', 'E': 'F'})

    # Create the machine
    enigma = EnigmaMachine(
        rotors=[rotor1, rotor2, rotor3],
        reflector=reflector,
        plugboard=plugboard
    )

    # Set initial rotor positions
    enigma.set_rotor_positions([1, 1, 1])

    # Encrypt a message
    message = "HELLOWORLD"
    encrypted = enigma.encrypt(message)
    print(f"Original: {message}")
    print(f"Encrypted: {encrypted}")

    # Reset the machine to decrypt
    enigma.set_rotor_positions([1, 1, 1])
    decrypted = enigma.encrypt(encrypted)
    print(f"Decrypted: {decrypted}")