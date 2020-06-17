import click
import dateutil.parser
import json
import os
import shutil
import subprocess
import tempfile
import shlex
import time
import sys
import urllib
from prettytable import PrettyTable, PLAIN_COLUMNS
from datetime import date

from sdccli import helpers
from sdccli.printer import print_item, print_list
from sdccli.usecases.scanning import image as use_case


@click.group(short_help='Image operations')
def image():
    pass


@image.command(name='add', short_help="Add an image")
@click.argument('input_image', nargs=1)
@click.option('--force', is_flag=True, help="Force reanalysis of image")
@click.option('--dockerfile', type=click.Path(exists=True), metavar='<Dockerfile>',
              help="Submit image's dockerfile for analysis")
@click.option('--annotation', nargs=1, multiple=True)
@click.option('--noautosubscribe', is_flag=True,
              help="If set, instruct the engine to disable tag_update subscription for the added tag.")
@click.pass_obj
def add(cnf, input_image, force, dockerfile, annotation, noautosubscribe):
    """
    INPUT_IMAGE: Input image can be in the following formats: registry/repo:tag
    """
    dockerfile_contents = None
    if dockerfile:
        try:
            with open(dockerfile) as f:
                dockerfile_contents = f.read()
        except Exception as error:
            print("Error parsing dockerfile file (%s): %s" % (dockerfile, str(error)))
            sys.exit(1)

    annotations = helpers.annotation_arguments_to_map(annotation)
    annotations.update({"added-by": "sysdig-cli"})

    try:
        res = use_case.add_scanning_image(cnf.sdscanning,
                                          input_image,
                                          force=force,
                                          dockerfile=dockerfile_contents,
                                          annotations=annotations,
                                          autosubscribe=not noautosubscribe)
        cnf.formatter.format(res, "scanningImage")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@image.command(name='list', short_help="List all images")
@click.option('--full', is_flag=True, help="Show full row output for each image")
@click.option('--show-all', is_flag=True,
              help="Show all images in the system instead of just the latest for a given tag")
@click.pass_obj
def imagelist(cnf, full, show_all):
    try:
        res = use_case.list_scanning_images(cnf.sdscanning, show_all=show_all)
        cnf.formatter.format(res, "scanningImageList")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@image.command(name='get', short_help="Get an image")
@click.argument('input_image', nargs=1)
@click.option('--show-history', is_flag=True,
              help="Show history of images that match the input image, if input image is of the form registry/repo:tag")
@click.pass_obj
def get(cnf, input_image, show_history):
    """
    INPUT_IMAGE: Input image can be in the following formats: Image Digest, ImageID or registry/repo:tag
    """
    try:
        res = use_case.get_image_from_digest_id_or_repo(cnf.sdscanning, input_image, show_history)
        cnf.formatter.format(res, "scanningImage")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@image.command(name='content', short_help="Get contents of image")
@click.argument('input_image', nargs=1)
@click.argument('content_type', nargs=1, required=False)
@click.pass_obj
def query_content(cnf, input_image, content_type):
    """
    INPUT_IMAGE: Input image can be in the following formats: Image Digest, ImageID or registry/repo:tag

    CONTENT_TYPE: The content type can be one of the following types:

      - os: Operating System Packages

      - npm: Node.JS NPM Module

      - gem: Ruby GEM

      - files: Files
    """
    try:
        res = use_case.query_image_content(cnf.sdscanning, input_image, content_type)
        cnf.formatter.format((res, content_type), "scanningQueryImage")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@image.command(name='metadata', short_help="Get metadata about an image")
@click.argument('input_image', nargs=1)
@click.argument('metadata_type', nargs=1, required=False)
@click.pass_obj
def query_metadata(cnf, input_image, metadata_type):
    """
    INPUT_IMAGE: Input image can be in the following formats: Image Digest, ImageID or registry/repo:tag

    METADATA_TYPE: The metadata type can be one of the types returned by running without a type specified
    """
    try:
        res = use_case.query_image_metadata(cnf.sdscanning, input_image, metadata_type)
        cnf.formatter.format((res, metadata_type), "scanningQueryImage")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@image.command(name='vuln', short_help="Get image vulnerabilities")
@click.argument('input_image', nargs=1)
@click.argument('vuln_type', nargs=1, default='all')
@click.option('--vendor-only', default=True, type=bool,
              help="Show only vulnerabilities marked by upstream vendor as applicable (default=True)")
@click.pass_obj
def query_vuln(cnf, input_image, vuln_type, vendor_only):
    """
    INPUT_IMAGE: Input image can be in the following formats: Image Digest, ImageID or registry/repo:tag

    VULN_TYPE: VULN_TYPE: Vulnerability type can be one of the following types:

      - os: CVE/distro vulnerabilities against operating system packages

      - non-os: NPM, Gem, Java Archive (jar, ear, war) and Python PIP CVEs

      - all: combination report containing both 'os' and 'non-os' vulnerability records (default)
    """
    try:
        res = use_case.query_image_vuln(cnf.sdscanning, input_image, vuln_type, vendor_only=vendor_only)
        cnf.formatter.format((res, vuln_type), "scanningVulnImage")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@image.command(name='evaluation', short_help="Check latest policy evaluation for an image")
@click.option("--show-history", is_flag=True, help="Show all previous policy evaluations")
@click.option("--detail", is_flag=True, help="Show detailed policy evaluation report")
@click.option("--tag", help="Specify which TAG is evaluated for a given image ID or Image Digest")
@click.option("--policy", help="Specify which POLICY to use for evaluate (defaults currently active policy)")
@click.argument('input_image', nargs=1)
@click.pass_obj
def check(cnf, input_image, show_history, detail, tag, policy):
    """
    INPUT_IMAGE: Input image can be in the following formats: Image Digest, ImageID or registry/repo:tag
    """
    try:
        res = use_case.check_image_evaluation(
            cnf.sdscanning, input_image,
            show_history=show_history,
            detail=detail,
            tag=tag,
            policy=policy)
        cnf.formatter.format((res, detail), "scanningEvaluationImage")
    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@image.command(name='pdf-report', short_help="Get the scan report for an image in pdf")
@click.option("--tag", help="Specify which TAG is evaluated for a given image ID or Image Digest")
@click.option("--date", help="Specify a date for the report")
@click.argument('input_image', nargs=1)
@click.argument('pdf_path', nargs=1)
@click.pass_obj
def pdf_report(cnf, input_image, pdf_path, tag, date):
    """
    INPUT_IMAGE: Input image can be in the following formats: Image Digest, ImageID or registry/repo:tag

    PDF_PATH: The name of the pdf that will be generated with the report
    """
    try:
        res = use_case.get_pdf_report(
            cnf.sdscanning,
            input_image,
            tag=tag,
            date=dateutil.parser.parse(date).strftime("%Y-%m-%dT%XZ") if date else None
        )
        with open(pdf_path, 'wb') as f:
            f.write(res)
        print("PDF %s saved" % pdf_path)

    except Exception as ex:
        print(f"Error: {str(ex)}")
        sys.exit(1)


@image.command(name='inline-scan', short_help="Analyze local docker images")
@click.option("--pull-image", is_flag=True, help="Specify this option to pull image locally before scanning")
@click.option("--verbose", is_flag=True, help="Specify this option to see the full detail of the scan report as json")
@click.option("--image-id", nargs=1, default='123', type=click.STRING,
              help="Specify this option to set image id for local image")
@click.option("--digest-id", nargs=1, default='sha256:123', type=click.STRING,
              help="Specify this option to set digest (sha256:<64 hex val>) for local image")
@click.option("--report-path", nargs=1, type=click.STRING, help="Specify this option to set path for PDF scan report")
@click.argument('image', nargs=1)
@click.pass_obj
def inline_scan(cnf, pull_image, verbose, image, digest_id, image_id, report_path):
    """
    INPUT_IMAGE: Input image can be in the following formats: registry/repo:tag || repo:tag || repo

    """
    inline_scan_image = 'docker.io/anchore/inline-scan:v0.6.1'
    docker_name = 'inline-scan'
    tempfile.tempdir = "/tmp"
    local_save_dir = tempfile.mkdtemp(prefix="sysdig-")
    try:
        # Save image provided in the inp param to tarball
        repo_name, base_image_name, base_image_tag = get_base_image_info(image)
        file_name = base_image_name + ':' + base_image_tag + '.tar '
        if ':' not in image:
            image = image + ':' + base_image_tag

        if 'sha256:' not in digest_id:
            raise NameError('Incorrect format for digest provided, should be sha256:<64 hex val> : ' + str(digest_id))

        if report_path is not None:
            if report_path.endswith('/'):
                raise NameError(
                    'Incorrect format for report path provided, should not end with trailing slash : ' + str(
                        report_path))

            if not os.path.isdir(report_path):
                raise NameError('Report path is not a valid directory : ' + str(report_path))

        print('Image being processed: ' + image)
        ok, res = cnf.sdscanning.get_anchore_users_account()
        if ok:
            user_name = res['name']
        else:
            raise PermissionError('Incorrect token/url provided for secure backend.')

        # Pulling images of inline-scan and images being scanned
        pull_images(inline_scan_image, image, pull_image)

        if image_id == '123':
            image_id = get_image_id(image)
        if digest_id == 'sha256:123':
            digest_id = get_repo_digest_id(image, repo_name, base_image_name, base_image_tag)

        print("Repo name : " + str(repo_name))
        print("Base image name : " + str(base_image_name))
        print("Tag name : " + str(base_image_tag))
        print("Image id : " + str(image_id))
        print("Digest id : " + str(digest_id))

        # Create the docker container for inline scan
        digest_id_sha = 'sha256:' + digest_id
        docker_cmd = ' analyze -d ' + digest_id_sha + ' -i ' + image_id + ' -u ' + user_name
        docker_create = 'docker create ' + ' --name ' + docker_name + ' ' + inline_scan_image + docker_cmd + ' ' + image

        ok, res = get_scan_result(cnf, image_id, image, verbose)

        # Check to see if the image is present in the BE, if not scan the local image
        if not ok:
            scan_image(cnf, image, base_image_name, base_image_tag, image_id, digest_id, file_name, local_save_dir,
                       docker_create, docker_name)
            # Fetch final scan result for given image
            ok, res = get_scan_result(cnf, image_id, image, verbose, 300, 1)

        if ok:
            scan_status = get_scan_status(str(res))
            print('Status is ' + scan_status)

            # To check if report option is invoked
            if report_path is not None:
                get_pdf_scan_result(cnf, digest_id_sha, image, report_path)

            if scan_status == 'fail':
                get_scan_result(cnf, image_id, image, True, 300, 1)
                sys.exit(1)

            # To check if verbose option message needs to be printed
            if report_path is None:
                print_linked_scan_result(cnf, digest_id_sha, image)
        else:
            raise RuntimeError('Unable to fetch the image scan result from Sysdig Secure: ' + str(res))

        print('Image analysis complete.')

    except Exception as e:
        print('Image analysis failed with error : ' + str(e))
        sys.exit(1)
    finally:
        cleanup_inline_scan(local_save_dir, docker_name)


def scan_image(cnf, image, base_image_name, base_image_tag, image_id, digest_id, file_name, local_save_dir,
               docker_create, docker_name):
    print(docker_create)
    subprocess.call(shlex.split(docker_create))

    docker_save = 'docker save ' + image + ' -o ' + local_save_dir + "/" + file_name
    print(docker_save)
    subprocess.call(shlex.split(docker_save))

    # Set chmod on the /tmp/sysdig directory
    permissions_cmd = 'chmod +r ' + local_save_dir + "/" + file_name
    print(permissions_cmd)
    subprocess.call(shlex.split(permissions_cmd))

    # Copy images to the inline scan docker container in the fixed location
    container_location = '/anchore-engine'
    docker_copy = 'docker cp ' + local_save_dir + '/' + file_name + docker_name + ':' + container_location + '/' + file_name
    print(docker_copy)
    subprocess.call(shlex.split(docker_copy))

    # Start the container for inline scan
    docker_start = 'docker start -ia ' + docker_name
    print(docker_start)
    subprocess.call(shlex.split(docker_start))

    # Fetch output file from the container and copy to local
    output_location = '/image-analysis-archive.tgz'
    output_file = '/' + base_image_name + ':' + base_image_tag + '-archive.tgz'
    docker_copy = 'docker cp ' + docker_name + ':' + container_location + output_location + ' ' + local_save_dir + output_file
    print(docker_copy)
    subprocess.call(shlex.split(docker_copy))

    # Post the output file to /import endpoint
    post_file_location = local_save_dir + output_file
    print(post_file_location)
    ok, res = post_analysis_file(cnf, post_file_location, image_id, digest_id, image)
    if ok:
        print('Analysis file successfully uploaded to Sysdig Secure.')
    else:
        raise RuntimeError('Unable to upload the analysis file to Sysdig Secure: ' + str(res))


def post_analysis_file(cnf, file_location, image_id, digest_id, image_name, retries=1, sleep_seconds=0):
    ok, res = retry_api_call(retries, sleep_seconds, cnf.sdscanning.import_image, file_location, image_id, digest_id,
                             image_name)
    return ok, res


def get_scan_result(cnf, image_id, full_tag, detail, retries=1, sleep_seconds=0):
    ok, res = retry_api_call(retries, sleep_seconds, cnf.sdscanning.get_image_scan_result_by_id, image_id, full_tag,
                             detail)
    if not detail:
        print('Scan Result : ')
    else:
        print('Detailed Scan Result: ')
    print(str(res))
    return ok, res


def get_pdf_scan_result(cnf, image_digest, full_tag, pdf_path, retries=1, sleep_seconds=0):
    print("Detailed Scan Results PDF: ")
    success, detailed_result = retry_api_call(retries, sleep_seconds, cnf.sdscanning.get_latest_pdf_report_by_digest,
                                              image_digest, full_tag)
    file_name = pdf_path + '/' + generate_file_name(full_tag)
    if success:
        with open(file_name, 'wb') as f:
            f.write(detailed_result)
        print("PDF saved : %s" % file_name)
    return success


def generate_file_name(full_tag):
    _, _, image = full_tag.rpartition('/')
    return "{date}-{image}-scan-results.pdf".format(date=date.today(), image=image)


def print_linked_scan_result(cnf, image_digest, full_tag):
    secure_url = cnf.sdscanning.url
    encoded_tag = urllib.parse.quote(full_tag, safe='')
    print("View the full result @ " + str(secure_url) + "/#/scanning/scan-results/" + str(encoded_tag)
          + "/" + str(image_digest) + "/summaries")
    print("You can also run the script with --report-path <path> option for more info.")


def retry_api_call(retry_count, sleep_seconds, api_function, *func_args, **func_kwargs):
    ok = False
    res = '{"api_call": "none"}'
    for i in range(0, retry_count):
        ok, res = api_function(*func_args, **func_kwargs)
        if ok:
            break
        time.sleep(sleep_seconds)
    return ok, res


def get_scan_status(json_res):
    pass_str = "'status': 'pass'"
    scan_status = 'fail'
    if json_res.find(pass_str) != -1:
        return 'pass'
    return scan_status


def pull_images(inline_scan_image, image, pull_image):
    docker_pull = 'docker pull '
    inline_image_pull = docker_pull + inline_scan_image
    print(inline_image_pull)
    subprocess.call(shlex.split(inline_image_pull))

    # Check to see if image to be scanned exists
    docker_inspect = 'docker inspect ' + image
    if pull_image:
        scan_image_pull = docker_pull + image
        print(scan_image_pull)
        subprocess.check_call(shlex.split(scan_image_pull))

    subprocess.check_output(shlex.split(docker_inspect))


def get_image_id(image):
    docker_inspect = 'docker inspect --format="{{.ID}}" ' + str(image) + ' | cut -d : -f 2 | tr -d "\n"'
    image_id = os.popen(docker_inspect).read()
    return image_id


def get_repo_digest_id(image, repo_name, base_image_name, base_image_tag):
    docker_inspect = 'docker inspect --format="{{.RepoDigests}}" ' + str(image)
    print(docker_inspect)
    op = os.popen(docker_inspect).read()
    # Check if the local image has a repo digest value
    digest = parse_repo_digest(repo_name, base_image_name, base_image_tag, op)
    print(digest)

    # If repo digest is not present, then generate new digest
    if digest is None:
        digest_gen = ' | sha256sum | sed -E "s/-//g" | sed -E "s/ //g" | tr -d "\n"'
        digest = os.popen(docker_inspect + digest_gen).read()
    return digest


def parse_repo_digest(repo_name, base_image_name, base_image_tag, digests):
    full_name = repo_name + "/" + base_image_name + ":" + base_image_tag
    full_image_name = base_image_name + ":" + base_image_tag

    if digests is not None:
        for digest in digests.split():
            if full_name in digest or full_image_name in digest or base_image_name:
                return digest.split(':')[1].replace(']', '')
    return None


def get_base_image_info(full_image_name):
    if "/" not in full_image_name:
        full_image_name = "localhost/" + full_image_name
    if ":" not in full_image_name:
        full_image_name += ":latest"
    repo, image_name = full_image_name.rsplit("/", 1)
    img, tag = image_name.split(":")
    return repo, img, tag


def cleanup_inline_scan(local_save_dir, docker_name):
    print("Inline scan cleanup starting.")
    # Remove the tmp directory if it exists already
    if os.path.exists(local_save_dir):
        shutil.rmtree(local_save_dir)

    # Remove only the inline scan specifically
    docker_name_check = 'docker ps -aq --filter name=' + docker_name + ''
    op = os.popen(docker_name_check).read()
    # Check if the image to be cleaned up exists before removing it
    if op != '':
        docker_remove = 'docker rm ' + op
        print(docker_remove)
        subprocess.call(shlex.split(docker_remove))
    print("Inline scan cleanup completed.")


@image.command(name='del', short_help="Delete an image")
@click.argument('input_image', nargs=-1, required=True)
@click.option('--force', is_flag=True,
              help="Force deletion of image by cancelling any subscription/notification settings prior to image delete")
@click.pass_obj
def delete(cnf, input_image, force):
    """
    INPUT_IMAGE: Input image can be in the following formats: Image Digest, ImageID or registry/repo:tag
    """
    for image in input_image:
        ok, res = cnf.sdscanning.delete_image(image, force=force)

        if not ok:
            print("Error: " + str(res))
            sys.exit(1)

    print("Success")
