import unittest
from tonetranspose.transpose import Transpose, NoteNameType, Tone, ToneGroup, Progression, SortKeys, Direction
import logging


def full_range(start, stop): return range(start, stop + 1)


class TestTone(unittest.TestCase):

    def setUp(self):
        pass

    def test_valid_note_name(self):
        self.assertEqual(True, Tone.is_valid_note_name("A"))
        self.assertEqual(True, Tone.is_valid_note_name("Bb"))
        self.assertEqual(True, Tone.is_valid_note_name("C#"))
        self.assertEqual(False, Tone.is_valid_note_name("B1b"))
        self.assertEqual(False, Tone.is_valid_note_name(1))
        self.assertEqual(True, Tone.is_valid_note_name(["C", "E", "G"]))
        self.assertEqual(False, Tone.is_valid_note_name(["C", "2", "G"]))

    def test_valid_pitch(self):
        self.assertEqual(False, Tone.is_valid_pitch(13))
        self.assertEqual(False, Tone.is_valid_pitch(0))
        self.assertEqual(False, Tone.is_valid_pitch(-1))
        for pitch in full_range(1, 12):
            self.assertEqual(True, Tone.is_valid_pitch(pitch))

    def test_tone_object(self):
        sharp_name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        flat_name = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        enharmonic_name = ["C", "Db_C#", "D", "Eb_D#", "E", "F", "Gb_F#", "G", "Ab_G#", "A", "Bb_A#", "B"]

        for pitch in full_range(1, 12):
            tone = Tone(pitch)
            self.assertEqual(tone.get_flat_name(), flat_name[pitch - 1])
            self.assertEqual(tone.get_sharp_name(), sharp_name[pitch - 1])
            self.assertEqual(tone.get_enharmonic(), enharmonic_name[pitch - 1])

    def test_tone_instance(self):
        note = "G"
        tone = Tone.get_instance_from_name(note)
        self.assertEqual(tone.get_enharmonic(), "G")

    def test_note_name_type(self):
        self.assertEqual(Tone.get_notation_type("C"), NoteNameType.Enharmonic)
        self.assertEqual(Tone.get_notation_type("F#"), NoteNameType.Sharp)
        self.assertEqual(Tone.get_notation_type("Db"), NoteNameType.Flat)
        self.assertEqual(Tone.get_notation_type(["D", "F#", "A"]), NoteNameType.Sharp)
        self.assertEqual(Tone.get_notation_type(["Bb", "Eb", "Ab"]), NoteNameType.Flat)
        self.assertEqual(Tone.get_notation_type(["Bb", "D", "F#"]), NoteNameType.Enharmonic)
        self.assertEqual(Tone.get_notation_type("??"), NoteNameType.Enharmonic)


class TestToneGroup(unittest.TestCase):

    def setUp(self):
        pass

    def tone_group_creation(self):
        tone_group = ToneGroup.get_instance("D", ["D", "F#", "A"])
        self.assertEqual(tone_group.to_string(NoteNameType.Sharp), "D, F#, A")
        self.assertEqual(tone_group.to_string(NoteNameType.Flat), "D, Gb, A")
        self.assertEqual(tone_group.to_string(NoteNameType.Enharmonic), "D, Gb_F#, A")
        self.assertEqual(tone_group.to_string(), "D, Gb_F#, A")
        self.assertEqual(tone_group.to_string(NoteNameType.Sharp), "D, F#, A")
        self.assertEqual(None, ToneGroup.get_instance("D", ["Dss", "F#", "A"]))


class TestTranspose(unittest.TestCase):

    def setUp(self):
        pass

    def tone_group_summary_intervals(self):
        transpose = Transpose("C", ['C', 'E', 'G'])
        intervals = transpose.get_intervals()
        self.assertEqual(intervals, ['R', '3', '5'])

    def tone_group_summary_keys(self):
        transpose = Transpose("C", ['C', 'E', 'G'])
        summary_key = transpose.get_key_pattern_summary()
        self.assertEqual(len(summary_key), 6)

        keys = ["www", "bwb", "wbw", "bbb", "bww", "wbb"]
        for key in keys:
            if key not in summary_key:
                self.assertRaises(KeyError)

        for key in summary_key:
            if key not in keys:
                self.assertRaises(KeyError)

    def tone_group_summary_data(self):
        transpose = Transpose("C", ['C', 'E', 'G'])
        summary_keys = transpose.get_key_pattern_summary(NoteNameType.Flat)
        for summary_key in summary_keys:
            if summary_key.key_pattern == "www":
                self.assertEqual(summary_key.count, 3)
                self.assertEqual(summary_key.root_notes, "C,F,G")
            elif summary_key.key_pattern == "bwb":
                self.assertEqual(summary_key.count, 3)
                self.assertEqual(summary_key.root_notes, "Db,Eb,Ab")
            elif summary_key.key_pattern == "wbw":
                self.assertEqual(summary_key.count, 3)
                self.assertEqual(summary_key.root_notes, "D,E,A")
            elif summary_key.key_pattern == "bbb":
                self.assertEqual(summary_key.count, 1)
                self.assertEqual(summary_key.root_notes, "Gb")
            elif summary_key.key_pattern == "bww":
                self.assertEqual(summary_key.count, 1)
                self.assertEqual(summary_key.root_notes, "Bb")
            elif summary_key.key_pattern == "wbb":
                self.assertEqual(summary_key.count, 1)
                self.assertEqual(summary_key.root_notes, "B")

    def test_all_transpositions(self):
        transpose = Transpose("C", ['C', 'E', 'G'])
        transpositions = transpose.get_all_positions()
        for t in transpositions:
            pitch = t.root_tone.pitch_number
            if pitch == 1:
                self.assertEqual(t.to_string(), "C, E, G")
            elif pitch == 2:
                self.assertEqual(t.to_string(), "Db_C#, F, Ab_G#")
            elif pitch == 3:
                self.assertEqual(t.to_string(), "D, Gb_F#, A")
            elif pitch == 4:
                self.assertEqual(t.to_string(), "Eb_D#, G, Bb_A#")
            elif pitch == 5:
                self.assertEqual(t.to_string(), "E, Ab_G#, B")
            elif pitch == 6:
                self.assertEqual(t.to_string(), "F, A, C")
            elif pitch == 7:
                self.assertEqual(t.to_string(), "Gb_F#, Bb_A#, Db_C#")
            elif pitch == 8:
                self.assertEqual(t.to_string(), "G, B, D")
            elif pitch == 9:
                self.assertEqual(t.to_string(), "Ab_G#, C, Eb_D#")
            elif pitch == 10:
                self.assertEqual(t.to_string(), "A, Db_C#, E")
            elif pitch == 11:
                self.assertEqual(t.to_string(), "Bb_A#, D, F")
            elif pitch == 12:
                self.assertEqual(t.to_string(), "B, Eb_D#, Gb_F#")

    def test_interval_counts(self):
        notes = Transpose("D", ["A", "C", "F", "G", "B", "C", "G", "B", "C", "G", "B", "C"])
        counts1 = notes.get_intervals_counts(NoteNameType.Flat)
        self.assertEqual(str(counts1), "{'5': 1, 'b7': 4, 'b3': 1, '4': 3, '6': 3}")
        counts2 = notes.get_intervals_counts(NoteNameType.Sharp)
        self.assertEqual(str(counts2), "{'5': 1, '#6': 4, '#2': 1, '4': 3, '6': 3}")
        counts3 = notes.get_intervals_counts()
        self.assertEqual(str(counts3), "{'5': 1, 'b7_#6': 4, 'b3_#2': 1, '4': 3, '6': 3}")

    def test_get_transposition_by_key(self):
        transpose = Transpose("C", ['C', 'E', 'G'])
        self.assertEqual(transpose.get_transposition(3).root_tone.get_note_name(NoteNameType.Flat), "D")
        self.assertEqual(transpose.get_transposition(3).to_string(NoteNameType.Flat), "D, Gb, A")
        self.assertEqual(transpose.get_transposition_for_named_key("E").root_tone.get_note_name(NoteNameType.Sharp),
                         "E")
        self.assertEqual(transpose.get_transposition_for_named_key("E").to_string(NoteNameType.Sharp), "E, G#, B")
        self.assertEqual(transpose.get_transposition_for_named_key("C").root_tone.get_note_name(), "C")
        self.assertEqual(transpose.get_transposition_for_named_key("C").to_string(), "C, E, G")
        self.assertEqual(transpose.get_transposition_for_named_key("A").to_string(), "A, Db_C#, E")

    def test_transposition_creation(self):
        # Tests to see if creating the transpose object using the instance method (input of a tonegroup)
        # is the same as creating a transpose object by directly calling the constructor
        # (input of note_name, and list of tone notes)

        self.maxDiff = None
        note_type_list = [NoteNameType.Flat, NoteNameType.Sharp, NoteNameType.Enharmonic]
        root_notes_list = ["C", "Bb", "F#"]
        list_notes_list = [["C", "E", "G"], ["C", "E", "G#"], ["C", "Eb", "G"], ["C", "Eb", "G#"]]

        for note_type in note_type_list:
            for root_note_name in root_notes_list:
                for list_notes in list_notes_list:
                    transpose1 = Transpose(root_note_name, list_notes)
                    tone_group = ToneGroup.get_instance(root_note_name, list_notes)
                    transpose2 = Transpose.get_instance(tone_group)

                    self.assertEqual(type(transpose1.root), type(transpose2.root))
                    self.assertEqual(transpose1.root, transpose2.root)

                    self.assertEqual(type(transpose1.notes_list), type(transpose2.notes_list))
                    self.assertEqual(transpose1.notes_list, transpose2.notes_list)

                    p1 = transpose1.get_all_positions()
                    p2 = transpose2.get_all_positions()

                    self.assertEqual(len(p1), len(p2))
                    self.assertEqual(type(transpose1.get_all_positions()), type(transpose2.get_all_positions()))

                    self.assertEqual(len(p1), 12)
                    self.assertEqual(len(p2), 12)

                    for a, b in zip(p1, p2):
                        self.assertEqual(a.to_string(note_type), b.to_string(note_type))

                    d1 = transpose1.get_key_pattern_summary(note_type)
                    d2 = transpose2.get_key_pattern_summary(note_type)

                    self.assertEqual(len(d1), len(d2))

                    for keys1, keys2 in zip(d1, d2):
                        self.assertEqual(keys1.key_pattern, keys2.key_pattern)
                        self.assertEqual(keys1.count, keys2.count)
                        self.assertEqual(keys1.root_notes, keys2.root_notes)

                    self.assertEqual(type(transpose1.note_name_type), type(transpose1.note_name_type))
                    self.assertEqual(transpose1.note_name_type, transpose1.note_name_type)

    def test_sorting_key_patterns(self):
        transpose1 = Transpose("C", ["C", "Eb", "G", "Bb"])

        # test default sort order settings
        positions = transpose1.get_key_pattern_summary(NoteNameType.Flat)
        self.assertEqual(len(positions), 8)
        counter = 0
        expected = [("wwww", 3, "D,E,A"), ("wbwb", 2, "C,F"), ("bwbw", 2, "Db,Gb"), ("bbbb", 1, "Eb"), ("wbww", 1, "G"),
                    ("bwbb", 1, "Ab"), ("bbwb", 1, "Bb"), ("wwbw", 1, "B")]
        for k1 in positions:
            self.assertEqual(k1.key_pattern, expected[counter][0])
            self.assertEqual(k1.count, expected[counter][1])
            self.assertEqual(k1.root_notes, expected[counter][2])
            counter += 1

        # test sort by specified direction
        positions = transpose1.get_key_pattern_summary(NoteNameType.Flat, SortKeys.Count, Direction.Ascending)
        self.assertEqual(len(positions), 8)
        counter = 0
        expected = [("bbbb", 1, "Eb"), ("wbww", 1, "G"), ("bwbb", 1, "Ab"), ("bbwb", 1, "Bb"), ("wwbw", 1, "B"),
                    ("wbwb", 2, "C,F"), ("bwbw", 2, "Db,Gb"), ("wwww", 3, "D,E,A")]
        for k1 in positions:
            self.assertEqual(k1.key_pattern, expected[counter][0])
            self.assertEqual(k1.count, expected[counter][1])
            self.assertEqual(k1.root_notes, expected[counter][2])
            counter += 1

        # test sort by key pattern
        positions = transpose1.get_key_pattern_summary(NoteNameType.Flat, SortKeys.KeyPattern, Direction.Ascending)
        self.assertEqual(len(positions), 8)
        counter = 0
        expected = [("bbbb", 1, "Eb"), ("bbwb", 1, "Bb"), ("bwbb", 1, "Ab"), ("bwbw", 2, "Db,Gb"), ("wbwb", 2, "C,F"),
                    ("wbww", 1, "G"), ("wwbw", 1, "B"), ("wwww", 3, "D,E,A")]
        for k1 in positions:
            self.assertEqual(k1.key_pattern, expected[counter][0])
            self.assertEqual(k1.count, expected[counter][1])
            self.assertEqual(k1.root_notes, expected[counter][2])
            counter += 1


class TestProgression(unittest.TestCase):
    def setUp(self):
        pass

    def test_root_notes(self):
        tone_group2 = ToneGroup.get_instance("D", ["D", "E", "A"])
        tone_group5 = ToneGroup.get_instance("G", ["G", "B", "D"])
        tone_group1 = ToneGroup.get_instance("C", ["C", "E", "G"])
        key = Tone.get_instance_from_name("C")
        progression = Progression(key, tone_group2, tone_group5, tone_group1)
        pos = progression.get_root_positions()
        pitch = 1
        for p in pos:
            if pitch == 1:
                self.assertEqual(p.to_string(NoteNameType.Flat), "D, G, C")
            elif pitch == 2:
                self.assertEqual(p.to_string(NoteNameType.Flat), "Eb, Ab, Db")
            elif pitch == 3:
                self.assertEqual(p.to_string(NoteNameType.Flat), "E, A, D")
            elif pitch == 4:
                self.assertEqual(p.to_string(NoteNameType.Flat), "F, Bb, Eb")
            elif pitch == 5:
                self.assertEqual(p.to_string(NoteNameType.Flat), "Gb, B, E")
            elif pitch == 6:
                self.assertEqual(p.to_string(NoteNameType.Flat), "G, C, F")
            elif pitch == 7:
                self.assertEqual(p.to_string(NoteNameType.Flat), "Ab, Db, Gb")
            elif pitch == 8:
                self.assertEqual(p.to_string(NoteNameType.Flat), "A, D, G")
            elif pitch == 9:
                self.assertEqual(p.to_string(NoteNameType.Flat), "Bb, Eb, Ab")
            elif pitch == 10:
                self.assertEqual(p.to_string(NoteNameType.Flat), "B, E, A")
            elif pitch == 11:
                self.assertEqual(p.to_string(NoteNameType.Flat), "C, F, Bb")
            elif pitch == 12:
                self.assertEqual(p.to_string(NoteNameType.Flat), "Db, Gb, B")
            pitch += 1


def run_tone_tests():
    test_tone = TestTone()
    test_tone.test_tone_instance()
    test_tone.test_valid_note_name()
    test_tone.test_valid_pitch()
    test_tone.test_note_name_type()


def run_transpose_tests():
    test_transpose = TestTranspose()
    test_transpose.tone_group_summary_intervals()
    test_transpose.tone_group_summary_keys()
    test_transpose.tone_group_summary_data()
    test_transpose.test_all_transpositions()
    test_transpose.test_interval_counts()
    test_transpose.test_get_transposition_by_key()
    test_transpose.test_transposition_creation()
    test_transpose.test_sorting_key_patterns()


def run_tone_group_tests():
    test_tone_group = TestToneGroup()
    test_tone_group.tone_group_creation()


def run_progression_tests():
    test_progression = TestProgression()
    test_progression.test_root_notes()


def run_all_tests():
    log = logging.getLogger("Transposer")
    logging.basicConfig(level=logging.INFO)
    log.info("Start testing")
    run_tone_tests()
    run_tone_group_tests()
    run_transpose_tests()
    run_progression_tests()
    log.info("End testing")


run_all_tests()
