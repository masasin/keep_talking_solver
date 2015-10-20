from solver import Bomb, SerialNumber


class TestSerialNumber(object):
    def test_serial_has_vowel(self):
        serial_yes = SerialNumber("IPZCV0")
        serial_no = SerialNumber("DS50L8")
        assert serial_yes.has_vowel()
        assert not serial_no.has_vowel()

    def test_serial_last_digit_odd(self):
        serial_odd = SerialNumber("IPZCV1")
        serial_even = SerialNumber("DS50L8")
        serial_odd_2 = SerialNumber("IPZC1V")
        serial_even_2 = SerialNumber("DS508L")
        assert serial_odd.last_odd()
        assert serial_odd_2.last_odd()
        assert not serial_even.last_odd()
        assert not serial_even_2.last_odd()

    def test_serial_last_digit_even(self):
        serial_odd = SerialNumber("IPZCV1")
        serial_even = SerialNumber("DS50L8")
        serial_odd_2 = SerialNumber("IPZC1V")
        serial_even_2 = SerialNumber("DS508L")
        assert serial_even.last_even()
        assert serial_even_2.last_even()
        assert not serial_odd.last_even()
        assert not serial_odd_2.last_even()


class TestBomb(object):
    def setup_method(self, method):
        self.bomb = Bomb("IPZCV0", 2, has_parallel=True)

    def test_initialization(self):
        assert self.bomb.n_strikes == 0

    def test_strike(self):
        self.bomb.strike()
        assert self.bomb.n_strikes == 1
        self.bomb.strike()
        assert self.bomb.n_strikes == 2

    def test_wires(self):
        assert self.bomb.wires("yby") == "SECOND"

    def test_button(self):
        assert self.bomb.button("detonate", "r") == "TAP"

    def test_keypad(self):
        assert self.bomb.keypad("six", "para", "an", "smile") == ["six", "para", "an", "smile"]
        assert self.bomb.keypad("six", "ae", "i", "psi") == ["six", "ae", "psi", "i"]

    def test_simon_says(self):
        pass
    
    def test_whos_on_first(self):
        pass

    def test_memory(self):
        pass

    def test_morse(self):
        pass

    def test_complicated(self):
        pass

    def test_sequences(self):
        pass

    def test_maze(self):
        assert (self.bomb.maze((4, 2), (5, 0), (2, 4)) == 
                ["left", "down", "left", "left", "left", "left", "down",
                 "right", "down", "right", "right", "down", "left"])

    def test_passwords(self):
        pass

    def test_venting(self):
        assert self.bomb.venting() == "YES"

    def test_capacitor(self):
        assert self.bomb.capacitor() == "HOLD DOWN LEVER"

    def test_knob(self):
        assert self.bomb.knob("000010") == "LEFT"
