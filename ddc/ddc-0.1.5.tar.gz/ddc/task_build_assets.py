from ddc.utils import stream_exec_cmd, md5


def start_build_assets(cwd: str, output_dir: str):
    all_output = []
    exit_code = -1
    image_tag: str = "ddc_local/tmp:" + md5(cwd)

    try:
        exit_code, mix_output = stream_exec_cmd(
            "docker build -t " + image_tag + " " + cwd
        )
        if exit_code:
            all_output.append("DDC: Build docker image")
            all_output.append(mix_output)
            raise StopIteration()

        docker_args = [
            "-v {output_dir}:/tmp/ddc_build_mount".format(output_dir=output_dir),
        ]

        all_output.append("Copy assets")
        exit_code, mix_output = stream_exec_cmd(
            "docker run --rm {docker_args} {image_tag} cp -R /usr/app_assets /tmp/ddc_build_mount".format(
                image_tag=image_tag,
                docker_args=" ".join(docker_args),
            )
        )
        all_output.append(mix_output)
    except StopIteration:
        pass
    finally:
        stream_exec_cmd("docker image rm " + image_tag)

    return exit_code, "\n".join(all_output)