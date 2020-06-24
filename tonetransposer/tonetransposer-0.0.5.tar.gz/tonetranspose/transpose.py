import enum
import logging


def full_range(start, stop): return range(start, stop + 1)


class NoteNameType(enum.Enum):
    Flat = 1
    Sharp = 2
    Enharmonic = 3


class SortKeys(enum.Enum):
    KeyPattern = 1
    Count = 2
    WhiteCount = 3
    BlackCount = 4


class Direction(enum.Enum):
    Ascending = 1
    Descending = 2


class PianoKeys:
    def __init__(self, key_pattern, count, root_notes, notes_list):
        self.key_pattern = key_pattern
        self.count = count
        self.root_notes = root_notes
        self.notes_list = notes_list
        self.white_count = key_pattern.count('w')
        self.black_count = key_pattern.count('b')


class Tone:
    min_pitch = 1
    max_pitch = 12
    key_color = ["w", "b", "w", "b", "w", "w", "b", "w", "b", "w", "b", "w"]
    sharp_name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    flat_name = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    enharmonic_name = ["C", "Db_C#", "D", "Eb_D#", "E", "F", "Gb_F#", "G", "Ab_G#", "A", "Bb_A#", "B"]

    def __init__(self, pitch_number):
        if Tone.is_valid_pitch(pitch_number):
            self.pitch_number = pitch_number
            self.user_defined_note = ""
        else:
            logging.error("value for pitch number not valid: ", pitch_number)
            raise ValueError

    @staticmethod
    def get_notation_type(notes):
        if type(notes) == list:
            has_sharp = False
            has_flat = False
            for note in notes:
                if Tone.__get_note_name_type(note) == NoteNameType.Flat:
                    has_flat = True
                elif Tone.__get_note_name_type(note) == NoteNameType.Sharp:
                    has_sharp = True
            if has_sharp and not has_flat:
                return NoteNameType.Sharp
            elif has_flat and not has_sharp:
                return NoteNameType.Flat
            else:
                return NoteNameType.Enharmonic
        else:
            return Tone.__get_note_name_type(notes)

    @staticmethod
    def __get_note_name_type(note):
        if note in Tone.sharp_name and note not in Tone.flat_name:
            return NoteNameType.Sharp
        elif note in Tone.flat_name and note not in Tone.sharp_name:
            return NoteNameType.Flat
        else:
            return NoteNameType.Enharmonic

    @staticmethod
    def is_valid_note_name(notes):
        if type(notes) == list:
            for note in notes:
                if not Tone.__is_valid_note_name(note):
                    return False
        else:
            return Tone.__is_valid_note_name(notes)
        return True

    @staticmethod
    def __is_valid_note_name(note_name):
        return True if note_name in Tone.sharp_name or note_name in Tone.flat_name else False

    @staticmethod
    def is_valid_pitch(pitch_number):
        return Tone.min_pitch <= pitch_number <= Tone.max_pitch

    @staticmethod
    def get_instance_from_name(note_name):

        # This is the main static method to instantiate a Tone object
        # from a string input representing the note name e.g "C#"

        if note_name in Tone.sharp_name:
            tone = Tone(Tone.sharp_name.index(note_name) + 1)
        elif note_name in Tone.flat_name:
            tone = Tone(Tone.flat_name.index(note_name) + 1)
        else:
            logging.error("note name does not exist: ", note_name)
            raise ValueError
        tone.user_defined_note = note_name
        return tone

    def get_location_on_keyboard(self):
        return self.key_color[self.pitch_number - 1]

    def get_sharp_name(self):
        return self.sharp_name[self.pitch_number - 1]

    def get_flat_name(self):
        return self.flat_name[self.pitch_number - 1]

    def get_enharmonic(self):
        return self.enharmonic_name[self.pitch_number - 1]

    def get_note_name(self, note_name_type=None):
        if note_name_type == NoteNameType.Flat:
            return self.get_flat_name()
        elif note_name_type == NoteNameType.Sharp:
            return self.get_sharp_name()
        else:
            return self.get_enharmonic()


class ToneGroup:
    __to_string = ""

    def __init__(self, root_tone, tone_list, tone_pattern, key_pattern, note_name_list):
        self.root_tone = root_tone
        self.tone_list = tone_list
        self.tone_pattern = tone_pattern
        self.key_pattern = key_pattern
        self.note_name_type = NoteNameType.Enharmonic
        self.note_name_list = note_name_list

    @staticmethod
    def get_instance(root_note, note_name_list):

        # This is the main method to instantiate a ToneGroup object
        # from a string input representing the root name, and a list of intervals
        # e.g "get_instance("C#",["C#","F","G#"])

        if not Tone.is_valid_note_name(note_name_list) or not Tone.is_valid_note_name(root_note):
            return
        root_tone = Tone.get_instance_from_name(root_note)
        tone_list = []
        tone_pattern = []
        key_pattern = ""
        for name in note_name_list:
            note_tone = Tone.get_instance_from_name(name)
            tone_list.append(note_tone)
            key_pattern += note_tone.get_location_on_keyboard()
            interval = note_tone.pitch_number - root_tone.pitch_number
            tone_pattern.append(interval)
        return ToneGroup(root_tone, tone_list, tone_pattern, key_pattern, note_name_list)

    def to_string(self, note_name_type=None):
        if self.tone_list:
            note_type = note_name_type if note_name_type is not None else self.note_name_type
            if self.__to_string == "" or note_type != self.note_name_type:
                self.__to_string = ', '.join((tone.get_note_name(note_type) for tone in self.tone_list))
                self.note_name_type = note_type
        return self.__to_string


class Transpose:

    # Transpose object can be instantiated in two different ways
    # Method 1: Call the object via the constructor
    # transpose = Transpose("C",["C","E","G"])
    #
    # Method 2: Create a Tone object and pass it to the static factory method
    # tone_group = ToneGroup.get_instance("D", ["D", "E", "A"])
    # transpose = Transpose.get_instance(tone_group)

    def __init__(self, root, notes_list):
        self.root = root
        self.notes_list = notes_list
        self.__transposed_list = []
        self.__piano_key_list = []
        self.__intervals_list = []
        self.note_name_type = NoteNameType.Enharmonic

    @staticmethod
    def get_instance(tone_group):
        return Transpose(tone_group.root_tone.user_defined_note, tone_group.note_name_list)

    @staticmethod
    def __get_interval(root_pitch, steps):
        if Tone.is_valid_pitch(root_pitch):
            transposed_pitch = (Tone.max_pitch + steps) + root_pitch if steps < 0 else root_pitch + steps
            return transposed_pitch if transposed_pitch <= Tone.max_pitch else transposed_pitch - Tone.max_pitch
        else:
            raise ValueError

    def get_all_positions(self):

        # Main method to get all the transpositions in a list that can be iterated through

        self.__transposed_list = []
        tone_group = ToneGroup.get_instance(self.root, self.notes_list)
        for pitch_number in full_range(Tone.min_pitch, Tone.max_pitch):
            if pitch_number == tone_group.root_tone.pitch_number:
                self.__transposed_list.append(tone_group)
            else:
                root_tone = Tone(pitch_number)
                transposed = []
                note_name_list = []
                key_pattern = ""
                for part in tone_group.tone_pattern:
                    transposed_pitch_number = self.__get_interval(pitch_number, part)
                    transposed_tone = Tone(transposed_pitch_number)
                    note_name_list.append(transposed_tone.get_note_name())
                    transposed.append(transposed_tone)
                    key_pattern += transposed_tone.get_location_on_keyboard()
                self.__transposed_list.append(ToneGroup(root_tone, transposed,
                                                        tone_group.tone_pattern, key_pattern, note_name_list))

        return self.__transposed_list

    def get_key_pattern_summary(self, note_name_type=None, sort_keys=SortKeys.Count,
                                direction=Direction.Descending):

        # Main method to get all shapes on a piano from a transposition in all 12 keys

        note_type = self.__get_valid_note_name_type(note_name_type)
        self.__piano_key_list = []
        piano_key_dict = {}
        tone_positions = self.get_all_positions()
        for position in tone_positions:
            if position.key_pattern not in piano_key_dict:
                tone_list = [position]
                piano_key_dict[position.key_pattern] = tone_list
            else:
                piano_key_dict[position.key_pattern].append(position)

        for key in piano_key_dict:
            root_names = ",".join([x.root_tone.get_note_name(note_type) for x in piano_key_dict[key]])
            piano_keys = PianoKeys(key, len(piano_key_dict[key]), root_names, piano_key_dict[key])
            self.__piano_key_list.append(piano_keys)

        if self.__piano_key_list:
            self.__sort_piano_key_list(sort_keys, direction)

        return self.__piano_key_list

    def __sort_piano_key_list(self, sort_keys, direction):
        if self.__piano_key_list:
            direction = True if direction == Direction.Descending else False
            if sort_keys == SortKeys.KeyPattern:
                self.__piano_key_list.sort(key=lambda piano_key: piano_key.key_pattern, reverse=direction)
            elif sort_keys == SortKeys.WhiteCount:
                self.__piano_key_list.sort(key=lambda piano_key: piano_key.white_count, reverse=direction)
            elif sort_keys == SortKeys.BlackCount:
                self.__piano_key_list.sort(key=lambda piano_key: piano_key.black_count, reverse=direction)
            else:
                self.__piano_key_list.sort(key=lambda piano_key: piano_key.count, reverse=direction)

    def print_key_pattern(self, note_name_type=None, sort_keys=SortKeys.Count,
                          direction=Direction.Descending):

        # shortcut to view the different shapes on a piano for a group of tones
        # transposed in all 12 musical keys

        note_type = self.__get_valid_note_name_type(note_name_type)
        key_patterns = self.get_key_pattern_summary(note_type, sort_keys, direction)
        if key_patterns:
            for keys in key_patterns:
                print(keys.key_pattern, "|", keys.count, "|", keys.root_notes)

    def print_positions(self, note_name_type=None):

        # shortcut to view a group of tones transposed in all 12 musical keys

        positions = self.get_all_positions()
        note_type = self.__get_valid_note_name_type(note_name_type)
        if positions:
            for position in positions:
                print(position.root_tone.get_note_name(note_type), "|", position.to_string(note_type))

    @staticmethod
    def get_interval_label(distance_root_to_note, note_name_type=None):
        labels_flat = {0: "R", 1: "b2", 2: "2", 3: "b3", 4: "3", 5: "4", 6: "b5", 7: "5", 8: "b6", 9: "6", 10: "b7",
                       11: "7", 12: "R"}
        labels_sharp = {0: "R", 1: "#R", 2: "2", 3: "#2", 4: "3", 5: "4", 6: "#4", 7: "5", 8: "#5", 9: "6", 10: "#6",
                        11: "7", 12: "R"}
        labels_enharmonic = {0: "R", 1: "b2_#R", 2: "2", 3: "b3_#2", 4: "3", 5: "4", 6: "b5_#4", 7: "5", 8: "b6_#5",
                             9: "6", 10: "b7_#6", 11: "7", 12: "R"}

        if note_name_type is None:
            note_name_type = NoteNameType.Enharmonic

        distance = distance_root_to_note if distance_root_to_note >= 0 else (
                Tone.max_pitch + distance_root_to_note)
        if (Tone.min_pitch - 1) <= distance <= Tone.max_pitch:

            if note_name_type == NoteNameType.Sharp:
                return labels_sharp[distance]
            elif note_name_type == NoteNameType.Flat:
                return labels_flat[distance]
            else:
                return labels_enharmonic[distance]
        else:
            return distance_root_to_note

    def get_intervals(self, note_name_type=None):
        note_type = NoteNameType.Enharmonic if note_name_type is None else note_name_type
        if not self.__intervals_list or note_type is not self.note_name_type:
            self.__intervals_list = []
            self.note_name_type = note_type
            root_tone = Tone.get_instance_from_name(self.root)
            for note in self.notes_list:
                tone = Tone.get_instance_from_name(note)
                self.__intervals_list.append(
                    self.get_interval_label(tone.pitch_number - root_tone.pitch_number, note_type))
        return self.__intervals_list

    def print_intervals(self, note_name_type=None):
        print(self.get_intervals(self.__get_valid_note_name_type(note_name_type)))

    def __get_valid_note_name_type(self, note_name_type):
        return note_name_type if note_name_type is not None else self.note_name_type

    def get_intervals_counts(self, note_name_type=None):
        note_type = NoteNameType.Enharmonic if note_name_type is None else note_name_type
        interval_list = self.get_intervals(note_type)
        dict_count = {}
        if interval_list:
            for interval in interval_list:
                if interval in dict_count:
                    dict_count[interval] = dict_count[interval] + 1
                else:
                    dict_count[interval] = 1
            return dict_count

    def get_transposition(self, pitch_number):
        if not Tone.is_valid_pitch(pitch_number):
            raise ValueError
        if not self.__transposed_list:
            self.get_all_positions()
        return self.__transposed_list[pitch_number - 1]

    def get_transposition_for_named_key(self, key):
        tone = Tone.get_instance_from_name(key)
        if not self.__transposed_list:
            self.get_all_positions()
        return self.__transposed_list[tone.pitch_number - 1]


class Progression:
    def __init__(self, key, *tone_groups):
        self.key = key
        self.tone_groups = tone_groups

    def get_root_positions(self, note_group_type=None):
        # Retrieves the root notes from a series of ToneGroups in all positions
        # so you can see the interval pattern of the progression in all keys

        note_type = NoteNameType.Enharmonic if note_group_type is None else note_group_type
        root_notes = []
        for tone_group in self.tone_groups:
            root_notes.append(tone_group.root_tone.get_note_name(note_type))
        transpose = Transpose(self.key.get_note_name(note_type), root_notes)
        positions = transpose.get_all_positions()
        return positions
