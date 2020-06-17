import os
from ddc.utils import stream_exec_cmd, __build_path, get_lang_tests_dir, md5


def _run_test(cwd: str, lang: str, save_test_results: bool = False):
    """
    Замес с exit_code и StopIteration довольно серьезный и не надо рефакторить это,
    если ты четко не понимаешь зачем это сделано
    """
    all_output = []
    exit_code = -1
    image_tag: str = "ddc_local/tmp:" + md5(cwd)

    try:
        if lang == "py":
            if not os.path.exists(cwd + "/tests"):
                all_output.append("DDC: Directory /tests is not exists")
                exit_code = 1
                raise StopIteration()

            exit_code, mix_output = stream_exec_cmd(
                "docker build -t " + image_tag + " " + cwd
            )
            if exit_code:
                all_output.append("DDC: Build docker image for test")
                all_output.append(mix_output)
                raise StopIteration()

            rwmeta_path = __build_path("/.rwmeta/")

            docker_args = [
                "-v {rwmeta_path}:/root/.rwmeta".format(rwmeta_path=rwmeta_path),
                "-v {cwd}:/usr/app".format(cwd=cwd),
            ]

            meta_dev_token = os.environ.get("X-META-Developer-Settings")
            if meta_dev_token:
                # На серверах файлы с токенами не лешал, все делается через env
                docker_args.append(
                    "-e 'X-META-Developer-Settings=" + meta_dev_token + "'"
                )

            pytest_args = "--reruns 2"
            if save_test_results:
                pytest_args += (
                    # " -o junit_family=xunit2 --junitxml=/usr/app/test-reports/tests.xml"
                )
            exit_code, mix_output = stream_exec_cmd(
                "docker run --rm {docker_args} {image_tag} pytest ./tests {pytest_args}".format(
                    image_tag=image_tag,
                    docker_args=" ".join(docker_args),
                    pytest_args=pytest_args,
                )
            )

            all_output.append(mix_output)
            if exit_code:
                raise StopIteration()

        elif lang == "php":
            if not os.path.exists(cwd + "/tests"):
                all_output.append("DDC: Directory /tests is not exists")
                exit_code = 1
                raise StopIteration()

            exit_code, mix_output = stream_exec_cmd(
                "docker build -t " + image_tag + " " + cwd
            )
            if exit_code:
                all_output.append("DDC: Build docker image for test")
                all_output.append(mix_output)
                raise StopIteration()
            phpunit_args = "--configuration tests/phpunit.xml"
            docker_args = []
            exit_code, mix_output = stream_exec_cmd(
                "docker run --rm {docker_args} {image_tag} ./vendor/bin/phpunit {phpunit_args} ./tests".format(
                    image_tag=image_tag,
                    docker_args=" ".join(docker_args),
                    phpunit_args=phpunit_args,
                )
            )

            all_output.append(mix_output)
            if exit_code:
                raise StopIteration()
        else:
            all_output.append("No test for lang: " + lang)
    except StopIteration:
        pass
    finally:
        stream_exec_cmd("docker image rm " + image_tag)
    return exit_code, "\n".join(all_output)


def start_test(cwd: str, lang: str, save_test_results: bool = False):
    if lang == "auto":
        new_output = []
        exit_code = 0
        for item in get_lang_tests_dir(cwd):
            new_output.append(
                "Test lang: " + lang + ". Dir: " + item["dir_for_run_tests"]
            )
            exit_code, lang_output = _run_test(
                item["dir_for_run_tests"], item["lang"], save_test_results
            )
            new_output.append(lang_output)
            if exit_code == 0:
                new_output.append("OK")
            else:
                new_output.append("Failure...")
                break
        return exit_code, "\n".join(new_output)
    else:
        _run_test(cwd, lang, save_test_results)
