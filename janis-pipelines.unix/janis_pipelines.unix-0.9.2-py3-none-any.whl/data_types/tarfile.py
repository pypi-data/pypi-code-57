from janis_core import File


class TarFile(File):
    @staticmethod
    def name():
        return "TarFile"

    def doc(self):
        return "A tarfile, ending with .tar"


class TarFileGz(File):
    @staticmethod
    def name():
        return "CompressedTarFile"

    def doc(self):
        return "A gzipped tarfile"
