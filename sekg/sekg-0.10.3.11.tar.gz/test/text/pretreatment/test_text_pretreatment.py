import unittest

from sekg.text.pretreatment.complete_subject import CompleteSubject
from sekg.text.spacy_pipeline.pipeline import PipeLineFactory
from sekg.text.pretreatment.coreference_resolution import ReferenceResolution


class MyTestCase(unittest.TestCase):
    def test_reference_resolution(self):
        r = ReferenceResolution()
        s = """A mutable sequence of characters. This class provides an API compatible with StringBuffer, but with no guarantee of synchronization. This class is designed for use as a drop-in replacement for StringBuffer in places where the string buffer was being used by a single thread (as is generally the case). Where possible, it is recommended that this class be used in preference to StringBuffer as it will be faster under most implementations.
        The principal operations on a StringBuilder are the append and insert methods, which are overloaded so as to accept data of any type. Each effectively converts a given datum to a string and then appends or inserts the characters of that string to the string builder. The append method always adds these characters at the end of the builder; the insert method adds the characters at a specified point.

        For example, if z refers to a string builder object whose current contents are "start", then the method call z.append("le") would cause the string builder to contain "startle", whereas z.insert(4, "le") would alter the string builder to contain "starlet".

        In general, if sb refers to an instance of a StringBuilder, then sb.append(x) has the same effect as sb.insert(sb.length(), x).

        Every string builder has a capacity. As long as the length of the character sequence contained in the string builder does not exceed the capacity, it is not necessary to allocate a new internal buffer. If the internal buffer overflows, it is automatically made larger.

        Instances of StringBuilder are not safe for use by multiple threads. If such synchronization is required then it is recommended that StringBuffer be used."""
        context = {"qn": "java.lang.StringBuilder"}
        remove_result_text, change_list = r.remove_reference_with_context(context, s)
        print(remove_result_text)

        # self.assertEqual(True, False)

    def test_spacy_token(self):
        nlp = PipeLineFactory.full_pipeline()
        query = """Hash table based implementation of the Map interface. This implementation provides all of the optional map operations, and permits null values and the null key. (The HashMap class is roughly equivalent to Hashtable, except that it is unsynchronized and permits nulls.) This class makes no guarantees as to the order of the map; in particular, it does not guarantee that the order will remain constant over time."""
        doc = nlp(query)
        result = []
        for sent in doc.sents:
            result.append(sent.text)
            print(sent.text)
        print(result)

    def test_complete_subject(self):
        complete_subject_tool = CompleteSubject()
        s = """A mutable sequence of characters."""
        context = {"qn": "java.lang.StringBuilder"}
        candidate_verb_set = {"get"}

        s2 = complete_subject_tool.complete_subject_by_name_for_doc(s, candidate_subject_name=context["qn"],
                                                                    candidate_verb_set=candidate_verb_set)
        print(s2)
        s3 = """java.lang.StringBuilder is a mutable sequence of characters."""
        self.assertEqual(s2, s3)

    def test_complete_subject_2(self):
        complete_subject_tool = CompleteSubject()

        s_list = [
            "there can be several Font objects associated with a font face, each differing in size, style, transform and font features.",
            "sort a given number list.",
            "String is a pieces of text that can not be modified.",
            "A very thread-safe, mutable sequence of characters.",
            "A string buffer is like a String, but can't be modified.",
            "A string buffer is like a String, but can not be modified.",
            "A string buffer is like a String, but can not be modified in any time.",
            "A thread-safe, mutable sequence of characters. A string buffer is like a String, but can be modified. At any point in time it contains some particular sequence of characters, but the length and content of the sequence can be changed through certain method calls. String buffers are safe for use by multiple threads. The methods are synchronized where necessary so that all the operations on any particular instance behave as if they occur in some serial order that is consistent with the order of the method calls made by each of the individual threads involved. The principal operations on a StringBuffer are the append and insert methods, which are overloaded so as to accept data of any type. Each effectively converts a given datum to a string and then appends or inserts the characters of that string to the string buffer. The append method always adds these characters at the end of the buffer; the insert method adds the characters at a specified point. Every string buffer has a capacity. As long as the length of the character sequence contained in the string buffer does not exceed the capacity, it is not necessary to allocate a new internal buffer array. If the internal buffer overflows, it is automatically made larger. As of release JDK 5, this class has been supplemented with an equivalent class designed for use by a single thread, StringBuilder. The StringBuilder class should generally be used in preference to this one, as it supports all of the same operations but it is faster, as it performs no synchronization.",
            "API is a thread-safe, mutable sequence of characters.",
            "StringBuffer is a thread-safe, mutable sequence of characters. ",
            "A string buffer is like a String, but can be modified for single thread.",
            "A string buffer is like a String, but can be modified when the thread is multiple thread.",
            "A string buffer is like a String, but can be modified if the thread is multiple thread.",
            "A mutable sequence of characters. This class provides an API compatible with StringBuffer, but with no guarantee of synchronization. This class is designed for use as a drop-in replacement for StringBuffer in places where the string buffer was being used by a single thread (as is generally the case). Where possible, it is recommended that this class be used in preference to StringBuffer as it will be faster under most implementations.",
            "A string buffer is like a String, but can be modified for multiple threads.",
            "This method parse String to int.",
            "check if the sentence is valid.",
            "return true if the list not empty",
            "append text to list.",
            "parse String to int.",
            "return true if the sentence is valid",
            "a helper interface to run the nested event loop.",
            "a thread-safe, mutable sequence of characters.",
            "Objects that implement this interface are created with the fast-fail EventQueue.createSecondaryLoop() method.",
            "Constructs a new object for Color.",
            "builds a new object for school.",
            "It is safe to use StringBuffer.",
            "When the enter() method is called, the current thread is blocked until the loop is terminated by the exit() method.",
            "Appendables are not necessarily safe for multithreaded access. ",
            "An object to which char sequences and values can be appended",
        ]
        context = {"qn": "java.lang.StringBuilder"}
        candidate_verb_set = {"get"}

        for each in s_list:
            s2 = complete_subject_tool.complete_subject_by_name_for_doc(each, candidate_subject_name=context["qn"],
                                                                        candidate_verb_set=candidate_verb_set)
            print(s2)

    def test_one(self):
        complete_subject_tool = CompleteSubject()
        context = {"qn": "java.lang.StringBuilder"}
        candidate_verb_set = {"get"}
        each = "parse String to int."
        s2 = complete_subject_tool.complete_subject_by_name_for_doc(each, candidate_subject_name=context["qn"],
                                                                    candidate_verb_set=candidate_verb_set)
        print(s2)


if __name__ == '__main__':
    unittest.main()
