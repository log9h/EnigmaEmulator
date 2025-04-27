from typing import Optional, Dict, List
import string

class Rotor:
    def __init__(self, wiring: str, notch: str, ring_setting: int = 1, position: int = 1):
        """
        Args:
            wiring: The wiring configuration (e.g., "EKMFLGDQVZNTOWYHXUSPAIBRCJ")
            notch: The turnover notch position(s) (e.g., "Q")
            ring_setting: The ring setting (1-26)
            position: The initial position (1-26)
        """
        self.wiring = wiring.upper()
        self.notch = notch.upper()
        self.ring_setting = ring_setting
        self.position = position
        self.alphabet = string.ascii_uppercase

        self.forward_map = {k: v for k, v in zip(self.alphabet, self.wiring)}
        self.backward_map = {v: k for k, v in zip(self.alphabet, self.wiring)}

    def rotate(self) -> bool:
        self.position = (self.position % 26) + 1
        return self.position == (ord(self.notch[0]) - ord('A') + 1)

    def forward(self, char: str) -> str:
        idx = (ord(char) - ord('A') + self.position - self.ring_setting) % 26
        mapped_char = self.wiring[idx]
        return chr((ord(mapped_char) - ord('A') - self.position + self.ring_setting) % 26 + ord('A'))

    def backward(self, char: str) -> str:
        idx = (ord(char) - ord('A') + self.position - self.ring_setting) % 26
        mapped_char = self.alphabet[self.wiring.index(chr(idx + ord('A')))]
        return chr((ord(mapped_char) - ord('A') - self.position + self.ring_setting) % 26 + ord('A'))


class Reflector:
    def __init__(self, wiring: str):
        """
        Args:
            wiring: The wiring configuration (e.g., "YRUHQSLDPXNGOKMIEBFZCWVJAT")
        """
        self.wiring = wiring.upper()
        self.alphabet = string.ascii_uppercase
        self.mapping = {k: v for k, v in zip(self.alphabet, self.wiring)}

    def reflect(self, char: str) -> str:
        return self.mapping[char]


class Plugboard:
    def __init__(self, connections: Optional[Dict[str, str]] = None):
        """
        Args:
            connections: Dictionary of letter connections (e.g., {'A': 'B', 'C': 'D'})
        """
        self.alphabet = string.ascii_uppercase
        self.mapping = {c: c for c in self.alphabet}

        if connections:
            for k, v in connections.items():
                k = k.upper()
                v = v.upper()
                self.mapping[k] = v
                self.mapping[v] = k

    def process(self, char: str) -> str:
        return self.mapping[char]
