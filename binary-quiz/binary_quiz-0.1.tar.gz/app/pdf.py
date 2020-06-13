import os
import subprocess
import tempfile

POSTSCRIPT_FILEPATH = "tempfile.ps"


def make_pdf(
    problems: str, answers: str, output_path: str, include_answers: bool
) -> None:
    if include_answers:
        pdf_jobs = (("problems", problems), ("answers", answers))
    else:
        pdf_jobs = ("problems", problems)

    for job_name, text in pdf_jobs:
        if job_name == "answers":
            output_path = make_answers_path(output_path)
        with tempfile.NamedTemporaryFile(mode="w") as txt_file:
            write_to_txtfile(txt_file, text)
            make_postscript_file(txt_file)
            make_pdf_file(output_path)
        os.unlink(POSTSCRIPT_FILEPATH)


def make_answers_path(path):
    path, filename = os.path.split(path)
    new_filename = f"{filename.split('.pdf')[0]}-answers.pdf"
    return os.path.join(path, new_filename)


def write_to_txtfile(txt_file, text):
    txt_file.write(text)
    txt_file.flush()


def make_pdf_file(output_path):
    command = f"ps2pdf {POSTSCRIPT_FILEPATH} {output_path}"
    subprocess.call(command, shell=True)


def make_postscript_file(txt_file):
    command = f"enscript --columns=4 --no-header --output={POSTSCRIPT_FILEPATH} {txt_file.name}"
    subprocess.call(command, shell=True)
