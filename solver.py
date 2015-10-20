# (C) 2015  Jean Nassar
# Released under the GNU General Public License, version 3
"""
Solver for *Keep Talking and Nobody Explodes*.

Based on *Bomb Defusal Manual*, v1r2, verification code 241. [#]_

References
----------
.. [#] Bomb Defusal Manual, Version 1, Verification Code 241, Revision 2.
       http://www.bombmanual.com/manual/1/html/index.html

"""
class SerialNumber(object):
    """
    Class for the serial number.

    Parameters
    ----------
    number : str
        The serial number of the bomb.

    Attributes
    ----------
    number : str
        The serial number of the bomb.
    digits : list of int
        The sequence of digits in the serial number.

    """
    def __init__(self, number):
        self.number = number
        self.digits = [int(i) for i in self.number if i.isdigit()]

    def has_vowel(self):
        """
        Check if the serial number contains any vowels.

        Returns
        -------
        bool
            True if the serial number contains a vowel.

        """
        for letter in "aeiou":
            if letter in self.number.lower():
                return True
        else:
            return False

    def last_odd(self):
        """
        Check if the last digit in the serial number is odd.

        Returns
        -------
        bool
            True if the last digit is odd.

        """
        return self.digits[-1] % 2

    def last_even(self):
        """
        Check if the last digit in the serial number is even.

        Returns
        -------
        bool
            True if the last digit is odd.

        """
        return not self.last_odd()


class Bomb(object):
    """
    The bomb to be defused.

    Parameters
    ----------
    serial_number : SerialNumber
        The serial number of the bomb.
    n_batteries : int
        The number of batteries on the bomb.
    has_parallel : bool
        Whether the bomb has a parallel port.
    frk : bool
        Whether the bomb has a FRK indicator.
    car : bool
        Whether the bomb has a CAR indicator.

    Attributes
    ----------
    serial_number : string
        The serial number of the bomb.
    n_batteries : int
        The number of batteries on the bomb.
    has_parallel : bool
        Whether the bomb has a parallel port.
    frk : bool
        Whether the bomb has a FRK indicator.
    car : bool
        Whether the bomb has a CAR indicator.
    n_strikes : int
        The number of strikes the team has committed.

    """
    def __init__(self, serial_number, n_batteries, has_parallel=False, frk=False, car=False):
        self.serial_number = SerialNumber(serial_number)
        self.n_batteries = n_batteries
        self.has_parallel = has_parallel
        self.frk = frk
        self.car = car
        self.n_strikes = 0

    def strike(self):
        """
        Register a strike.

        """
        self.n_strikes += 1

    def wires(self, wires):
        """
        Solve a *Wires* module.

        Parameters
        ----------
        wires : str
            A string containing the code for the wire colours.

            **Colours :**

            - black : k
            - blue : b
            - red : r
            - white : w
            - yellow : y

            Therefore, a module containing three modules with white, blue, and
            black, would be input as "wbk".

        Returns
        -------
        to_cut : str
            The wire to cut, ordinal from left to right starting with one.

        """
        wires = wires.lower()
        ordinal = ["FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH"]
        if len(wires) == 3:
            if "r" not in wires:
                to_cut = "SECOND"
            elif wires[-1] == "w":
                to_cut = "THIRD"
            elif wires.count("b") > 1:
                to_cut = ordinal[2 - wires[::-1].index("b")]
            else:
                to_cut = "THIRD"
        elif len(wires) == 4:
            if wires.count("r") > 1 and self.serial_number.last_odd():
                to_cut = ordinal[2 - wires[::-1].index("r")]
            elif ((wires[-1] == "y"and wires.count("r") == 0)
                  or wires.count("b") == 1):
                to_cut = "FIRST"
            elif wires.count("y") > 1:
                to_cut = "FOURTH"
            else:
                to_cut = "SECOND"
        elif len(wires) == 5:
            if wires[-1] == "k" and self.serial_number.last_odd():
                to_cut = "FOURTH"
            elif wires.count("r") == 1 and wires.count("y") > 1:
                to_cut = "FIRST"
            elif wires.count("k") == 0:
                to_cut = "SECOND"
            else:
                to_cut = "FIRST"
        else:
            if wires.count("y") == 0 and self.serial_number.last_odd():
                to_cut = "THIRD"
            elif wires.count("y") == 0 and wires.count("w") > 1:
                to_cut = "FOURTH"
            elif wires.count("r") == 0:
                to_cut = "SIXTH"
            else:
                to_cut = "FOURTH"
        return to_cut

    def button(self, text, colour):
        """
        Solve a *Button* module.

        Parameters
        ----------
        text : str
            The text on the button.
        colour : char
            The colour of the button.

            **Colours :**

            - blue : b
            - red : r
            - white : w
            - yellow : y
            - none : n

        Returns
        -------
        str
            Instruction for the operator

        """
        def release():
            """
            Determine the number at which to release the button.

            Returns
            -------
            The number at which to release the button.

            """
            colour = input("Strip colour: ").lower()
            if colour == "b":
                number = "FOUR"
            elif colour == "y":
                number = "FIVE"
            else:
                number = "ONE"
            return number

        text = text.lower()
        if text == "abort" and colour == "b":
            to_hold = True
        elif self.n_batteries > 1 and text == "detonate":
            to_hold = False
        elif colour == "w" and self.car:
            to_hold = True
        elif self.n_batteries > 2 and self.frk:
            to_hold = False
        elif colour == "y":
            to_hold = True
        elif text == "hold" and colour == "r":
            to_hold = False
        else:
            to_hold = True

        if to_hold:
            return "HOLD until the timer contains a {n}".format(n=release())
        else:
            return "PRESS and immediately RELEASE"

    def keypad(self, *keys):
        """
        Solve a *Keypads* module.

        Parameters
        ----------
        keys : str
            The names of the buttons. The order does not matter. Use as many as
            needed.

            The columns, from left to right, are:

            - [q, at, lambda, zigzag, an, h, crescent]
            - [eh, q, crescent, wu, star, h, question]
            - [copyright, ot, wu, zhe, hoe, lambda, star]
            - [six, para, keyblade, an, zhe, question, smile]
            - [psi, smile, keyblade, crescent, para, xi, blackstar]
            - [six, eh, neq, ae, psi, i, omega]

        Returns
        -------
        str
            The order in which the buttons are to be pressed.

        """
        columns = [
            ['q', 'at', 'lambda', 'zigzag', 'an', 'h', 'crescent'],
            ['eh', 'q', 'crescent', 'wu', 'star', 'h', 'question'],
            ['copyright', 'ot', 'wu', 'zhe', 'hoe', 'lambda', 'star'],
            ['six', 'para', 'keyblade', 'an', 'zhe', 'question', 'smile'],
            ['psi', 'smile', 'keyblade', 'crescent', 'para', 'xi', 'blackstar'],
            ['six', 'eh', 'neq', 'ae', 'psi', 'i', 'omega']
        ]

        working_column = None
        keyset = set(keys)
        output = []
        for column in columns:
            if len(set(column).intersection(keyset)) == 4:
                working_column = column
                break
        for key in working_column:
            if key in keys:
                output.append(key)
        return output

    def simon(self):
        """
        Solve a *Simon Says* module.

        Run the solver, then input a colour every time. The solver will
        generate the appropriate response. If a strike is incurred during the
        loop, simply halt the operation of the program, run `strike`, and try
        again.

        **Colours :**

        - blue : b
        - green : g
        - red : r
        - yellow : y

        """
        map_with_vowel = {
            0: {"r": "b",
                "b": "r",
                "g": "y",
                "y": "g"},
            1: {"r": "y",
                "b": "g",
                "g": "b",
                "y": "r"},
            2: {"r": "g",
                "b": "r",
                "g": "y",
                "y": "b"}
        }
        map_with_no_vowel = {
            0: {"r": "b",
                "b": "y",
                "g": "g",
                "y": "r"},
            1: {"r": "r",
                "b": "b",
                "g": "y",
                "y": "g"},
            2: {"r": "y",
                "b": "g",
                "g": "b",
                "y": "r"}
        }
        colour_map = map_with_vowel if self.serial_number.has_vowel() else map_with_no_vowel
        try:
            while True:
                colour = input("Colour: ")
                print(colour_map[n_strikes][colour])
        except KeyboardInterrupt:
            pass

    def whos(self):
        """
        Solve a *Who's on First* problem.

        Run the solver. On each iteration, input the letters on the display.
        The operator shall then relay the label of the appropriate button.
        Mission control would then speak a list of the words, one at a time,
        until a match is found. The operator presses the matching button.

        """
        responses = {
            "READY": ("YES, OKAY, WHAT, MIDDLE, LEFT, PRESS, RIGHT, BLANK, "
                      "READY, NO, FIRST, UHHH, NOTHING, WAIT"),
            "FIRST": ("LEFT, OKAY, YES, MIDDLE, NO, RIGHT, NOTHING, UHHH, "
                      "WAIT, READY, BLANK, WHAT, PRESS, FIRST"),
            "NO": ("BLANK, UHHH, WAIT, FIRST, WHAT, READY, RIGHT, YES, "
                   "NOTHING, LEFT, PRESS, OKAY, NO, MIDDLE"),
            "BLANK": ("WAIT, RIGHT, OKAY, MIDDLE, BLANK, PRESS, READY, "
                      "NOTHING, NO, WHAT, LEFT, UHHH, YES, FIRST"),
            "NOTHING": ("UHHH, RIGHT, OKAY, MIDDLE, YES, BLANK, NO, PRESS, "
                        "LEFT, WHAT, WAIT, FIRST, NOTHING, READY"),
            "YES": ("OKAY, RIGHT, UHHH, MIDDLE, FIRST, WHAT, PRESS, READY, "
                    "NOTHING, YES, LEFT, BLANK, NO, WAIT"),
            "WHAT": ("UHHH, WHAT, LEFT, NOTHING, READY, BLANK, MIDDLE, NO, "
                     "OKAY, FIRST, WAIT, YES, PRESS, RIGHT"),
            "UHHH": ("READY, NOTHING, LEFT, WHAT, OKAY, YES, RIGHT, NO, PRESS, "
                     "BLANK, UHHH, MIDDLE, WAIT, FIRST"),
            "LEFT": ("RIGHT, LEFT, FIRST, NO, MIDDLE, YES, BLANK, WHAT, UHHH, "
                     "WAIT, PRESS, READY, OKAY, NOTHING"),
            "RIGHT": ("YES, NOTHING, READY, PRESS, NO, WAIT, WHAT, RIGHT, "
                      "MIDDLE, LEFT, UHHH, BLANK, OKAY, FIRST"),
            "MIDDLE": ("BLANK, READY, OKAY, WHAT, NOTHING, PRESS, NO, WAIT, "
                       "LEFT, MIDDLE, RIGHT, FIRST, UHHH, YES"),
            "OKAY": ("MIDDLE, NO, FIRST, YES, UHHH, NOTHING, WAIT, OKAY, LEFT, "
                     "READY, BLANK, PRESS, WHAT, RIGHT"),
            "WAIT": ("UHHH, NO, BLANK, OKAY, YES, LEFT, FIRST, PRESS, WHAT, "
                     "WAIT, NOTHING, READY, RIGHT, MIDDLE"),
            "PRESS": ("RIGHT, MIDDLE, YES, READY, PRESS, OKAY, NOTHING, UHHH, "
                      "BLANK, LEFT, FIRST, WHAT, NO, WAIT"),
            "YOU": ("SURE, YOU ARE, YOUR, YOU'RE, NEXT, UH HUH, UR, HOLD, "
                    "WHAT?, YOU, UH UH, LIKE, DONE, U"),
            "YOU ARE": ("YOUR, NEXT, LIKE, UH HUH, WHAT?, DONE, UH UH, HOLD, "
                        "YOU, U, YOU'RE, SURE, UR, YOU ARE"),
            "YOUR": ("UH UH, YOU ARE, UH HUH, YOUR, NEXT, UR, SURE, U, YOU'RE, "
                     "YOU, WHAT?, HOLD, LIKE, DONE"),
            "YOU'RE": ("YOU, YOU'RE, UR, NEXT, UH UH, YOU ARE, U, YOUR, WHAT?, "
                       "UH HUH, SURE, DONE, LIKE, HOLD"),
            "UR": ("DONE, U, UR, UH HUH, WHAT?, SURE, YOUR, HOLD, YOU'RE, "
                   "LIKE, NEXT, UH UH, YOU ARE, YOU"),
            "U": ("UH HUH, SURE, NEXT, WHAT?, YOU'RE, UR, UH UH, DONE, U, YOU, "
                  "LIKE, HOLD, YOU ARE, YOUR"),
            "UH HUH": ("UH HUH, YOUR, YOU ARE, YOU, DONE, HOLD, UH UH, NEXT, "
                       "SURE, LIKE, YOU'RE, UR, U, WHAT?"),
            "UH UH": ("UR, U, YOU ARE, YOU'RE, NEXT, UH UH, DONE, YOU, UH HUH, "
                      "LIKE, YOUR, SURE, HOLD, WHAT?"),
            "WHAT?": ("YOU, HOLD, YOU'RE, YOUR, U, DONE, UH UH, LIKE, YOU ARE, "
                      "UH HUH, UR, NEXT, WHAT?, SURE"),
            "DONE": ("SURE, UH HUH, NEXT, WHAT?, YOUR, UR, YOU'RE, HOLD, LIKE, "
                     "YOU, U, YOU ARE, UH UH, DONE"),
            "NEXT": ("WHAT?, UH HUH, UH UH, YOUR, HOLD, SURE, NEXT, LIKE, "
                     "DONE, YOU ARE, UR, YOU'RE, U, YOU"),
            "HOLD": ("YOU ARE, U, DONE, UH UH, YOU, UR, SURE, WHAT?, YOU'RE, "
                     "NEXT, HOLD, UH HUH, YOUR, LIKE"),
            "SURE": ("YOU ARE, DONE, LIKE, YOU'RE, YOU, HOLD, UH HUH, UR, "
                     "SURE, U, WHAT?, NEXT, YOUR, UH UH"),
            "LIKE": ("YOU'RE, NEXT, U, UR, HOLD, DONE, UH UH, WHAT?, UH HUH, "
                     "YOU, LIKE, SURE, YOU ARE, YOUR")
        }
        try:
            while True:
                display = input("Display: ")
                if display == "ur":
                    print("TOP LEFT")
                elif display in ("first", "okay", "c"):
                    print("TOP RIGHT")
                elif display in ("yes", "nothing", "led", "they are"):
                    print("MIDDLE LEFT")
                elif display in ("blank", "read", "red", "you", "your", "you're", "their"):
                    print("MIDDLE RIGHT")
                elif display in ("", "reed", "leed", "they're"):
                    print("BOTTOM LEFT")
                else:
                    print("BOTTOM RIGHT")

                label = input("Button label: ")
                print(responses[label.upper()])

        except KeyboardInterrupt:
            pass

    def memory(self):
        """
        Solve a *Memory* module.

        Run the solver. The operator should relay the number on the screen.
        Mission control instructs with regards to the button to be pressed.
        Note that this can be either the label, or the position of the button.

        Once a button is pressed, the operator confirms its number and
        position, which is then input into the solver.

        """
        class Solution(object):
            """
            A solution container.

            """
            def __init__(self):
                self.position = None
                self.label = None

        def solve_stage(stage, display):
            """
            Solve a given stage.

            Appends a solution to the `pressed` array.

            Parameters
            ----------
            stage : int
                The stage to be solved.
            display : str
                The text on the module display.

            """
            soln = Solution()
            if stage == 1:
                if display in ("1", "2"):
                    soln.position = "SECOND"
                elif display == "3":
                    soln.position = "THIRD"
                else:
                    soln.position = "FOURTH"
            elif stage == 2:
                if display in ("2", "4"):
                    soln.position = pressed[0].position
                elif display == "1":
                    soln.label = "FOUR"
                else:
                    soln.position = "FIRST"
            elif stage == 3:
                if display == "1":
                    soln.label = pressed[1].label
                elif display == "2":
                    soln.label = pressed[0].label
                elif display == "3":
                    soln.position = "THIRD"
                elif display == "4":
                    soln.value = "FOUR"
            elif stage == 4:
                if display in ("3", "4"):
                    soln.position = pressed[1].position
                elif display == "1":
                    soln.position = pressed[0].position
                else:
                    soln.position = "FIRST"
            else:
                if display == "1":
                    soln.label = pressed[0].label
                elif display == "2":
                    soln.label = pressed[1].label
                elif display == "3":
                    soln.label = pressed[3].label
                else:
                    soln.label = pressed[2].label

            if soln.position is None:
                print(soln.label)
                soln.position = input("Button position: ")
            else:
                print(soln.position)
                soln.label = input("Button label: ")
            pressed.append(soln)

        pressed = []
        try:
            for i in range(1, 6):
                print("Stage {}:".format(i))
                display = input("Display: ")
                solve_stage(i, display)
                print("-" * 20)
        except KeyboardInterrupt:
            pass

    def morse(self):
        """
        Solve a *Morse Code* problem.

        If the operator knows morse code, they can relay the letter directly.
        Otherwise, they may speak the dits (dots) and dahs (dashes) out loud.
        Mission control would enter them one at a time and the solver will
        interpret them.

        Returns
        -------
        str
            The frequency to be selected.

        """
        decrypt = {
            ".-"  : "A",   "-...": "B",   "-.-.": "C",
            "-.." : "D",   "."   : "E",   "..-.": "F",
            "--." : "G",   "....": "H",   ".."  : "I",
            ".---": "J",   "-.-" : "K",   ".-..": "L",
            "--"  : "M",   "-."  : "N",   "---" : "O",
            ".--.": "P",   "--.-": "Q",   ".-." : "R",
            "..." : "S",   "-"   : "T",   "..-" : "U",
            "...-": "V",   ".--" : "W",   "-..-": "X",
            "-.--": "Y",   "--..": "Z",
        }
        frequency = {
            "shell": "3.505",
            "halls": "3.515",
            "slick": "3.522",
            "trick": "3.532",
            "boxes": "3.535",
            "leaks": "3.542",
            "strobe": "3.545",
            "bistro": "3.552",
            "flick": "3.555",
            "bombs": "3.565",
            "break": "3.572",
            "brick": "3.575",
            "steak": "3.582",
            "sting": "3.592",
            "vector": "3.595",
            "beats": "3.600"
        }
        active = set(frequency.keys())
        try:
            for i in range(6):
                char = input("Letter or morse: ")
                if char.isalnum():
                    letter = char
                else:
                    letter = decrypt[char].lower()
                working_active = active.copy()
                for word in active:
                    if word[i] != letter:
                        working_active.remove(word)
                active = working_active
                if len(active) == 1:
                    return frequency[active.pop()], " Mhz"
        except KeyboardInterrupt:
            pass

    def complicated(self):
        """
        Solve a *Complicated Wires* module.

        Run the solver. For each wire, input whether the LED is on ("1") or off
        ("0"), the wire colour, and whether a star is ("1") or is not ("0")
        drawn. The colours are shown below.

        **Colours :**

        - blue : b
        - red : r
        - striped : s
        - none : n

        For each wire, wait until mission control declares whether or not to
        cut the wire before proceeding.

        """
        def decide(letter):
            """Print out whether or not to cut a wire."""
            if letter == "C":
                to_cut = True
            elif letter == "D":
                to_cut = False
            elif letter == "S":
                to_cut = True if self.serial_number.last_even() else False
            elif letter == "P":
                to_cut = True if self.has_parallel else False
            else:
                to_cut = True if self.n_batteries >= 2 else False
            if to_cut:
                print("CUT")
            else:
                print("DO NOT CUT")

        instructions = ["C", "C", "S", "D",  # 0000 to 0011
                        "S", "C", "S", "P",  # 0100 to 0111
                        "D", "B", "P", "P",  # 1000 to 1011
                        "B", "B", "S", "D"]  # 1100 to 1111

        try:
            idx = 1
            while True:
                led, colour, star = input("Wire {}. led, colour, star: ".format(idx))
                if colour == "r":
                    blue = "0"
                    red = "1"
                elif colour == "b":
                    blue = "1"
                    red = "0"
                elif colour == "s":
                    blue = "1"
                    red = "1"
                else:
                    blue = "0"
                    red = "0"
                case = int("".join((led, red, blue, star)), 2)
                letter = instructions[case]
                decide(letter)
                idx += 1
        except KeyboardInterrupt:
            pass

    def sequences(self):
        """
        Solve a *Wire Sequences* module.

        Run the solver. For each step, enter the colour of the wire, and its
        connection. The solver prints the decision for each wire.

        **Colours :**

        - blue : b
        - black : k
        - red : r

        """
        counts = {"r": 0, "b": 0, "k": 0}
        cuts = {
            "r": ["c", "b", "a", "ac", "b", "ac", "abc", "ab", "b"],
            "b": ["b", "ac", "b", "a", "b", "bc", "c", "ac", "a"],
            "k": ["abc", "ac", "b", "ac", "b", "bc", "ab", "c", "c"]
        }
        try:
            while True:
                colour, connection = input("Colour and connection: ")
                print("CUT" if connection in cuts[colour][counts[colour]]
                      else "DO NOT CUT")
                counts[colour] += 1
        except KeyboardInterrupt:
            pass

    def maze(self, indicator, start, target):
        """
        Solve a *Maze* module.

        The coordinates take the form of a tuple. The origin is at the top-left
        corner of the maze. The first element denotes the x-direction, with
        positive being to the right. The second element denotes the
        y-direction, with positive being downwards. Note that all tuples start
        at zero.

        Parameters
        ----------
        indicator : (int, int)
            The location of one indicator.
        start : (int, int)
            The starting location of the user.
        target : (int, int)
            The location of the target.

        Returns
        -------
        instructions : list of str
            A list of directions to take one at a time.

        """
        if indicator == (0, 1) or indicator == (5, 2):
            maze = [
                ["rd", "lr", "ld", "rd", "lr", "l"],
                ["ud", "rd", "ul", "ur", "lr", "ld"],
                ["ud", "ur", "ld", "rd", "lr", "uld"],
                ["ud", "r", "ulr", "lu", "r", "uld"],
                ["urd", "lr", "ld", "rd", "l", "ud"],
                ["ur", "l", "ur", "ul", "r", "ul"]
            ]
        elif indicator == (4, 1) or indicator == (1, 3):
            maze = [
                ["r", "lrd", "l", "rd", "lrd", "l"],
                ["rd", "ul", "rd", "ul", "ur", "ld"],
                ["ud", "rd", "ul", "rd", "lr", "uld"],
                ["urd", "ul", "rd", "ul", "d", "ud"],
                ["ud", "d", "ud", "rd", "ul", "ud"],
                ["u", "ur", "ul", "ur", "lr", "lu"]
            ]
        elif indicator == (3, 3) or indicator == (5, 3):
            maze = [
                ["dr", "lr", "ld", "d", "dr", "dl"],
                ["u", "d", "ud", "ur", "lu", "ud"],
                ["dr", "uld", "ud", "rd", "ld", "ud"],
                ["ud", "ud", "ud", "ud", "ud", "ud"],
                ["ud", "ur", "ul", "ud", "ud", "ud"],
                ["ur", "lr", "lr", "ul", "ur", "ul"]
            ]
        elif indicator == (0, 0) or indicator == (0, 3):
            maze = [
                ["rd", "ld", "r", "lr", "lr", "ld"],
                ["ud", "ud", "dr", "lr", "lr", "uld"],
                ["ud", "ur", "lu", "rd", "l", "ud"],
                ["ud", "r", "lr", "lru", "lr", "lud"],
                ["udr", "lr", "lr", "lr", "ld", "ud"],
                ["ur", "lr", "l", "r", "ul", "u"]
            ]
        elif indicator == (4, 2) or indicator == (3, 5):
            maze = [
                ["r", "lr", "lr", "lr", "lrd", "ld"],
                ["rd", "lr", "lr", "lrd", "lu", "u"],
                ["udr", "ld", "r", "ul", "rd", "ld"],
                ["ud", "ur", "lr", "ld", "u", "ud"],
                ["ud", "rd", "lr", "ulr", "l", "ud"],
                ["u", "ur", "lr", "lr", "lr", "lu"]
            ]
        elif indicator == (4, 0) or indicator == (2, 4):
            maze = [
                ["d", "dr", "ld", "r", "ldr", "ld"],
                ["ud", "ud", "ud", "rd", "ul", "ud"],
                ["udr", "ul", "u", "ud", "rd", "ul"],
                ["ur", "ld", "dr", "udl", "ud", "d"],
                ["rd", "ul", "u", "ud", "ur", "uld"],
                ["ur", "lr", "lr", "ul", "r", "ul"]
            ]
        elif indicator == (1, 0) or indicator == (1, 5):
            maze = [
                ["dr", "lr", "lr", "ld", "dr", "ld"],
                ["ud", "rd", "l", "ur", "lu", "ud"],
                ["ur", "ul", "rd", "l", "rd", "ul"],
                ["dr", "ld", "udr", "lr", "ul", "d"],
                ["ud", "u", "ur", "lr", "ld", "ud"],
                ["ur", "lr", "lr", "lr", "ulr", "ul"]
            ]
        elif indicator == (3, 0) or indicator == (2, 3):
            maze = [
                ["d", "dr", "lr", "ld", "dr", "ld"],
                ["udr", "ulr", "l", "ur", "ul", "ud"],
                ["ud", "dr", "lr", "lr", "ld", "ud"],
                ["ud", "ur", "ld", "r", "ulr", "ul"],
                ["ud", "d", "ur", "lr", "lr", "l"],
                ["ur", "ulr", "lr", "lr", "lr", "l"]
            ]
        else:
            maze = [
                ["d", "dr", "lr", "lr", "ldr", "ld"],
                ["ud", "ud", "rd", "l", "ud", "ud"],
                ["udr", "ulr", "ul", "rd", "ul", "ud"],
                ["ud", "d", "dr", "ul", "r", "uld"],
                ["ud", "ud", "ud", "dr", "dl", "u"],
                ["ur", "ul", "ur", "ul", "ur", "l"]
            ]

        visited = []
        branches = []
        moves = []
        i, j = start
        while (i, j) != target:
            print(i, j)
            visited.append((i, j))
            moves.append((i, j))
            val = maze[j][i]
            n_possible = len(val)
            if "u" in val and (i, j-1) in visited:
                n_possible -= 1
            if "d" in val and (i, j+1) in visited:
                n_possible -= 1
            if "l" in val and (i-1, j) in visited:
                n_possible -= 1
            if "r" in val and (i+1, j) in visited:
                n_possible -= 1

            if n_possible > 1:
                branches.append((i, j))

            if "u" in val and (i, j-1) not in visited:
                j -= 1
            elif "d" in val and (i, j+1) not in visited:
                j += 1
            elif "l" in val and (i-1, j) not in visited:
                i -= 1
            elif "r" in val and (i+1, j) not in visited:
                i += 1
            else:
                i, j = branches.pop()
                moves = moves[:moves.index((i, j))]

        moves.append(target)
        instructions = []
        for current, move in zip(moves, moves[1:]):
            if move[1] < current[1]:
                instructions.append("up")
            elif move[1] > current[1]:
                instructions.append("down")
            elif move[0] < current[0]:
                instructions.append("left")
            else:
                instructions.append("right")
        return instructions

    def passwords(self, initial):
        """
        Solve a *Passwords* module.

        Run the solver. For each position, input all the possible letters
        which can be entered. Mission control would obtain a shrinking list
        of possible passwords.

        Parameters
        ----------
        initial : str
            The initial sequence of letters.

        """
        all_passwords = (
            "about", "after", "again", "below", "could",
            "every", "first", "found", "great", "house",
            "large", "learn", "never", "other", "place",
            "plant", "point", "right", "small", "sound",
            "spell", "still", "study", "their", "there",
            "these", "thing", "think", "three", "water",
            "where", "which", "world", "would", "write"
        )
        active = set()
        for pos, letter in enumerate(initial):
            for word in all_passwords:
                if word[pos] == letter:
                    active.add(word)
        print("Active words: {}".format(active))
        for i in range(5):
            possibilities = input("All possible in position {}: ".format(i))
            working_active = active.copy()
            for word in active:
                if word[i] not in possibilities:
                    working_active.remove(word)
            active = working_active
            print("Active words: {}".format(active))

    def venting(self):
        """Solve a *Venting Gas* module."""
        return "YES"

    def capacitor(self):
        """Solve a *Capacitor Discharge* module."""
        return "HOLD DOWN LEVER"

    def knob(self, top_row):
        """
        Solve a *Knob* module.

        In some cases, the status of the bottom LEDs may need to be provided.

        Parameters
        ----------
        top_row : str
            The status of the LEDs on the top row, from left to right. "1"
            denotes a lit LED, and "0" denotes one which is off.

        Returns
        -------
        str
            The direction relative to "UP" in which to move the knob.

        """
        if top_row == "101010":
            bottom_row = input("Bottom row: ")
            if bottom_row == "011011":
                return "UP"
            else:
                return "DOWN"
        else:
            if top_row == "001011":
                return "UP"
            elif top_row == "011001":
                return "DOWN"
            elif top_row == "000010":
                return "LEFT"
            else:
                return "RIGHT"
