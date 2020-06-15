import io
import os
import uuid
from django.core.exceptions import ValidationError

from ai_kit_file_management.models import File as FileModel, generate_unique_file_name
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase
from model_bakery import baker


class FileModelTest(TestCase):
    """
    Test class for testing the File model functions
    """

    @classmethod
    def setUpTestData(cls):
        cls.test_user = baker.make(get_user_model(), email="a@example.com")
        cls.test_file = File(io.BytesIO(b""), "test.png")
        cls.test_file_name = "test_name.png"

    def tearDown(self):
        """
        Cleaning method for preventing saving files while testing
        """
        for file in FileModel.objects.all():
            if file.file:
                if os.path.isfile(file.file.path):
                    os.remove(file.file.path)

    def test_model_save(self):
        """
        Tests if the overwritten save method properly fills the size, format and name attribute.
        And if a unique filename has been generated.
        todo add check for format
        """
        test_instance = FileModel(file=self.test_file, creator=self.test_user)
        test_instance.save()

        self.assertEqual(
            test_instance.size,
            self.test_file.size,
            msg="Size should equal the size of the file itself",
        )
        self.assertEqual(
            test_instance.name,
            self.test_file.name,
            msg="Name should equal the name of the file itself",
        )
        self.assertNotEqual(
            test_instance.file.name,
            self.test_file.name,
            msg="A unique dirname should have been generated",
        )
        uuid.UUID(os.path.dirname(test_instance.file.name))
        # Should not raise, since the filename should be valid uuid

    def test_model_save_name_given(self):
        """
        Tests if the name properly is filled correctly when a name is given
        """
        test_instance = FileModel(
            file=self.test_file, creator=self.test_user, name=self.test_file_name
        )
        test_instance.save()

        self.assertEqual(
            test_instance.name,
            self.test_file_name,
            msg="name should be equal to the given name",
        )

    def test_model_save_invalid_format(self):
        """
        Tests if the save method raises an Error when the format is not allowed
        """
        test_file = File(io.BytesIO(b""), "test.bin")
        test_file_name = "test_name.bin"
        test_instance = FileModel(
            file=test_file, creator=self.test_user, name=test_file_name
        )

        with self.assertRaises(
            ValidationError, msg=".bin file format should not be allowed"
        ):
            test_instance.save()

    def test_generate_unique_file_name(self):
        """
        Tests if the generate_unique_file_name function returns a string that contains a filename and a file extension
        """

        filename = generate_unique_file_name(self.test_file, self.test_file_name)
        self.assertEqual(type(filename), str, msg="Function should return a string")

        _, file_extension = os.path.splitext(filename)
        self.assertGreater(
            len(file_extension), 0, msg="Filename should have an extension"
        )
