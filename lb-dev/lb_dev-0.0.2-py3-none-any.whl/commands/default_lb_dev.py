import logging
import os
import sys
import stat
import re
from whichcraft import which
from subprocess import call
from string import Template

from lb_dev.constants import lb_dev_constants

from LbEnv import fixProjectCase
from LbEnv import ProjectEnv
from LbEnv.ProjectEnv import SearchPath
from LbEnv.ProjectEnv.version import expandVersionAlias
from LbEnv.ProjectEnv.lookup import MissingProjectError
from LbEnv.ProjectEnv.options import NightlyPathEntry, LHCbDevPathEntry
import LbEnv

log = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def default_lb_dev(project, dev, dev_dir, nightly_base, nightly, help_nightly_local, user_area, no_user_area, siteroot, platform, force_platform, list, list_versions, list_platforms, name, dest_dir, git, with_fortran):
    if dev:
        dev_dir = append_lhcb_dev_path(dev_dir)

    if nightly_base:
        check_if_has_only_dirs(nightly_base)

    if nightly:
        nightly, dev_dir, nightly_base = format_nightly_option(
            nightly, dev_dir, nightly_base)

    log.info('splitting project from version..')

    project = to_project_version_pair(project)

    try:
        project, version = project
    except ValueError:
        log.error('wrong number of arguments')
        print('ERROR: wrong number of arguments')
        return 1

    log.debug('project name and version after splitting are: {} and {}'.format(
        project, version))

    log.info('fixing project case..')

    project = fixProjectCase(project)

    log.debug(
        'project name and version after case-fixing are: {} and {}'.format(project, version))

    log.info('checking platform')

    platform = checkPlatform(platform) or "best"

    log.debug('platform after check is {}'.format(platform))

    log.info('expanding version alias if there is one..')

    version = expandVersionAlias(
        project, version, platform if platform != "best" else "any"
    )

    log.debug('version after alias expansion is {}'.format(version))

    if platform == "best":
        log.info('retrieving best supported platform..')
        platform = get_supported_platform(project, version)

    log.debug('platform is {}'.format(platform))

    handle_possible_errors(nightly, help_nightly_local, project, platform)

    if user_area and not no_user_area:
        dev_dir = append_user_release_area(dev_dir, user_area)

    # FIXME: we need to handle common options like --list in a single place
    handle_list_options(list, list_platforms, project, version, platform)

    log.info('naming and versioning new project..')
    name, new_project_name, new_project_version = name_and_version_new_project(
        name, project, version)

    log.debug('new_project_name and new_project_version: {} and {}'.format(
        new_project_name, new_project_version))

    devProjectDir = os.path.join(dest_dir, name)

    log.debug('dev project dir: "{}"'.format(devProjectDir))

    if os.path.exists(devProjectDir):
        log.error('directory "%s" already exist' % devProjectDir)
        print('ERROR: directory "%s" already exist' % devProjectDir)
        return 1

    # ensure that the project we want to use can be found

    # prepend dev dirs to the search path
    combined_paths = combine_dev_dir_with_project_env_paths(dev_dir)

    log.info(
        'looking for project directory for specified project, version and platform..')

    try:
        projectDir = find_project_dir(project, version, platform)

        log.info('projectDir is "{}"'.format(projectDir))

        log.info('checking project type..')
        use_cmake, use_cmt = check_project_type(projectDir, project, version)

        if not use_cmake and not use_cmt:
            log.error(
                "neither CMake nor CMT configuration found "
                "(are you using the right BINARY_TAG?)"
            )
            print(
                'ERROR: neither CMake nor CMT configuration found (are you using the right BINARY_TAG?)')
            exit(1)
    except SystemExit:
        if nightly:
            try:
                from LbEnv.ProjectEnv.lookup import InvalidNightlySlotError
                from LbEnv.ProjectEnv.script import localNightlyHelp

                sys.stderr.write(
                    localNightlyHelp(
                        os.path.basename(sys.argv[0]),
                        InvalidNightlySlotError(nightly[0], nightly[1], []),
                        project,
                        platform
                        if platform not in ("best", None)
                        else "$BINARY_TAG",
                        sys.argv[1:],
                    )
                )
            except ImportError:
                # old version of LbEnv
                # (before https://gitlab.cern.ch/lhcb-core/LbEnv/merge_requests/19)
                pass
        return 1

    # Create the dev project
    create_destination_directory(dest_dir)

    create_project_directory(devProjectDir, git)
    log.debug('creating directory "%s"', devProjectDir)

    log.debug('generating data dictionary')
    data = get_data_dictionary(project, version, combined_paths, use_cmake,
                               new_project_name, new_project_version, with_fortran, name, platform)

    # # FIXME: improve generation of searchPath files, so that they match the command line
    templateDir = os.path.join(os.path.dirname(
        __file__), "..", "templates", "lb-dev")

    templates = lb_dev_constants.TEMPLATES

    # generated files that need exec permissions
    execTemplates = set(["run"])

    data = add_nightly_info(data, nightly)

    log.debug('data: {}'.format(data.items()))

    # for backward compatibility, we create the CMT configuration and env helpers
    if use_cmt:
        templates += ["cmt/project.cmt"]
        os.makedirs(os.path.join(devProjectDir, "cmt"))

    log.info('creating templates..')
    create_templates(templates, data, templateDir,
                     devProjectDir, execTemplates,)

    dev_dir = to_SearchPath(dev_dir)

    if dev_dir and use_cmake:
        create_cmake(devProjectDir, dev_dir)

    if dev_dir and use_cmt:
        create_cmt(devProjectDir, dev_dir)

    # When the project name is not the same as the local project name, we need a
    # fake *Sys package for SetupProject (CMT only).
    if use_cmt and project != new_project_name:
        create_requirements_file(
            data, templateDir, devProjectDir, new_project_name)

        if use_cmake:  # add a CMakeLists.txt to it
            create_cmake_list(devProjectDir, new_project_name,
                              new_project_version)

    # add a default .clang-format file
    add_default_clang_format(projectDir, devProjectDir)

    if git:
        createGitIgnore(os.path.join(
            devProjectDir, ".gitignore"), selfignore=False)
        commitProjectCreation(devProjectDir)

    reportSuccess(name, dest_dir, devProjectDir, project, platform)


def get_supported_platform(project, version):
    from LbEnv.ProjectEnv.lookup import listPlatforms
    from LbEnv.ProjectEnv.script import HOST_INFO
    from LbPlatformUtils import host_supports_tag

    try:
        platform = next(
            p
            for p in listPlatforms(project, version)
            if host_supports_tag(HOST_INFO, p)
        )

        return platform
    except StopIteration:
        log.error('none of the available platforms is supported: {!r}\n'.format(
            listPlatforms(project, version)))
        sys.stderr.write(
            "none of the available platforms is supported:"
            " {!r}\n".format(listPlatforms(project, version))
        )
        sys.exit(64)


def to_project_version_pair(project):
    log.debug('project before: "{}"'.format(project))
    if "/" in project:
        project = tuple(project.split("/", 1))
    else:
        project = (project, lb_dev_constants.DEFAULT_VERSION)
    log.debug('project after: "{}"'.format(project))

    return project


def checkPlatform(platform):
    '''
    Validate platform obtained from the parser to get the right value according
    to options, environment or system.
    '''
    try:
        # from LbEnv import defaultPlatform
        if not platform:
            btag = os.environ.get('BINARY_TAG')
            cconf = os.environ.get('CMTCONFIG')
            if btag and cconf and btag != cconf:
                log.error('inconsistent BINARY_TAG and CMTCONFIG values '
                          '(%s != %s), please unset CMTCONFIG or fix '
                          'the values' % (btag, cconf))
                return 1  # needed it parser.error does not call exit
            platform = btag or cconf or defaultPlatform()
        return platform
    except RuntimeError:
        log.error('unsupported system, check the environment or use '
                  '--platform to override the check')
        print('ERROR: unsupported system, check the environment or use --platform to override the check')
        return 1  # needed it parser.error does not call exit


def defaultPlatform():
    '''
    Return the default platform for the current host.
    '''
    from LbPlatformUtils import dirac_platform, can_run, requires

    host = dirac_platform()

    for line in resource_string('platforms.txt').splitlines():
        # remove comments and whitespaces
        platform = line.split('#', 1)[0].strip()
        if platform and can_run(host, requires(platform)):
            return platform

    raise RuntimeError('cannot find a valid platform for current host, '
                       'try lb-describe-platform')


def resource_string(name):
    '''
    Helper to get data stored with the package.
    '''
    import pkg_resources
    data = pkg_resources.resource_string(
        __name__, os.path.join('..', 'data', name))
    # FIXME compatibility py2-py3
    if sys.version_info >= (3, ):
        data = data.decode()
    return data


def createClangFormat(dest, overwrite=False):
    """Add `.clang-format` file.
    @param dest: destination filename
    @param overwrite: flag to decide if an already present file has to be kept
                      or not (default is False)
    """

    if overwrite or not os.path.exists(dest):
        log.debug("Creating '%s'", dest)
        with open(dest, "w") as f:
            f.writelines(open(os.path.join(DATA_DIR, "default.clang-format")))
        return True
    return False


def createGitIgnore(dest, overwrite=False, extra=None, selfignore=True):
    """Write a generic .gitignore file, useful for git repositories.
    @param dest: destination filename
    @param overwrite: flag to decide if an already present file has to be kept
                      or not (default is False)
    @param extra: list of extra patterns to add
    @param selfignore: if the .gitignore should include itself
    """
    import logging

    if overwrite or not os.path.exists(dest):
        logging.debug("Creating '%s'", dest)
        patterns = [
            "/InstallArea/",
            "/build.*/",
            "*.pyc",
            "*~",
            ".*.swp",
            "/.clang-format",
        ]
        if selfignore:
            patterns.insert(0, "/.gitignore")  # I like it as first entry
        if extra:
            patterns.extend(extra)

        with open(dest, "w") as f:
            f.write("\n".join(patterns))
            f.write("\n")
        return True
    return False


def format_nightly_option(nightly_value, dev_dir, nightly_base):
    log.debug('nightly, dev_dir, nightly_base before: "{}", "{}", "{}"'.format(
        nightly_value, dev_dir, nightly_base))

    slot, day = extract_nightly_slot_and_day(nightly_value)

    # Locate the requested slot in the know nightlies directories
    nightly_base = append_nightlies_directories(nightly_base)

    from LbEnv.ProjectEnv.lookup import (findNightlyDir,
                                         InvalidNightlySlotError)
    try:
        slot_dir = findNightlyDir(slot, day, nightly_base)

        nightly_base, slot, day = slot_dir.rsplit(os.sep, 2)
        nightly_path = NightlyPathEntry(nightly_base, slot, day)
        dev_dir = dev_dir + tuple([nightly_path.path])
        nightly = (slot, day, nightly_base)
    except InvalidNightlySlotError as err:
        # to be able to print a friendly message about local
        # installation of a nightly slot, we cannot exit while parsing
        # the arguments
        nightly = err

    log.debug('nightly, dev_dir, nightly_base after: "{}", "{}", "{}"'.format(
        nightly, dev_dir, nightly_base))
    return nightly, dev_dir, nightly_base


def extract_nightly_slot_and_day(nightly_value):
    try:
        slot, day = nightly_value.split('/', 1)
        day = format_day(day)
    except ValueError:
        slot, day = nightly_value, 'Today'

    return slot, day


def format_day(day):
    if lb_dev_constants.VALID_DAY_REGEX.match(day):
        day = day.capitalize()
    elif day.lower() == 'latest':
        day = 'latest'

    return day


def append_nightlies_directories(directories):
    from os import environ
    directories += tuple([
        environ.get('LHCBNIGHTLIES',
                    '/cvmfs/lhcbdev.cern.ch/nightlies'),
        environ.get('LCG_nightlies_area',
                    '/cvmfs/sft-nightlies.cern.ch/lcg/nightlies')
    ])

    return directories


def append_lhcb_dev_path(dev_dir):
    log.debug('dev_dir before: "{}"'.format(dev_dir))
    try:
        value = LHCbDevPathEntry()
        dev_dir = dev_dir + tuple([value])
    except ValueError:
        log.error('--dev used, but LHCBDEV is not defined')
        print('ERROR: --dev used, but LHCBDEV is not defined')

    log.debug('dev_dir after: "{}"'.format(dev_dir))

    return dev_dir


def check_if_has_only_dirs(iterable_of_directories):
    for path in iterable_of_directories:
        if not os.path.isdir(path):
            raise ValueError('"%s" is not a directory' % path)


def append_user_release_area(dev_dir, user_area):
    from LbEnv.ProjectEnv import EnvSearchPathEntry, SearchPathEntry

    if os.environ["User_release_area"] == user_area:
        dev_dir = tuple(["User_release_area"]) + dev_dir
    else:
        dev_dir = tuple([user_area]) + dev_dir

    return dev_dir


def handle_possible_errors(nightly, help_nightly_local, project, platform):
    try:
        from LbEnv.ProjectEnv.lookup import InvalidNightlySlotError
        from LbEnv.ProjectEnv.script import localNightlyHelp

        if isinstance(nightly, InvalidNightlySlotError):
            sys.stderr.write(
                localNightlyHelp(
                    os.path.basename(sys.argv[0]),
                    nightly,
                    project,
                    platform
                    if platform not in ("best", None)
                    else "$BINARY_TAG",
                    sys.argv[1:],
                )
            )
            sys.exit(64)

        if help_nightly_local:
            if not nightly:
                log.error(
                    "--help-nightly-local must be specified in "
                    "conjunction with --nightly"
                )
                print(
                    "--help-nightly-local must be specified in "
                    "conjunction with --nightly"
                )

            sys.stdout.write(
                localNightlyHelp(
                    os.path.basename(sys.argv[0]),
                    InvalidNightlySlotError(nightly[0], nightly[1], []),
                    project,
                    platform
                    if platform not in ("best", None)
                    else "$BINARY_TAG",
                    [
                        a
                        for a in sys.argv[1:]
                        if not "--help-nightly-local".startswith(a)
                    ],
                    error=False,
                )
            )
            sys.exit()
    except ImportError:
        # old version of LbEnv
        # (before https://gitlab.cern.ch/lhcb-core/LbEnv/merge_requests/19)
        pass


def handle_list_options(list, list_platforms, project, version, platform):
    if list:
        from LbEnv.ProjectEnv.lookup import listVersions
        for entry in listVersions(project, platform):
            print("%s in %s" % entry)
        sys.exit(0)
    if list_platforms:
        from LbEnv.ProjectEnv.lookup import listPlatforms

        platforms = listPlatforms(project, version)
        if platforms:
            print("\n".join(platforms))
        sys.exit(0)


def name_and_version_new_project(name, project, version):
    if not name:
        name = "{}Dev_{}".format(project, version)
        new_project_name, new_project_version = project + "Dev", version
    else:
        new_project_name, new_project_version = name, "HEAD"

    return name, new_project_name, new_project_version


def combine_dev_dir_with_project_env_paths(dev_dir):
    dev_dir_paths = ()
    if dev_dir:    
        for path in dev_dir:
            dev_dir_paths = dev_dir_paths + tuple([path])

    projectEnvPaths = ()
    for path in ProjectEnv.path:
        projectEnvPaths = projectEnvPaths + tuple([path])

    combined_paths = dev_dir_paths + projectEnvPaths

    return combined_paths
        

def find_project_dir(project, version, platform):
    try:
        projectDir = ProjectEnv.lookup.findProject(
            project, version, platform, allow_empty_version=True)
        log.info("using %s %s from %s", project, version, projectDir)

        return projectDir
    except MissingProjectError as x:
        log.error(str(x))
        print('ERROR: {}'.format(str(x)))
        exit(1)


def check_project_type(projectDir, project, version):
    use_cmake = has_cmake(projectDir, project)  
    if not use_cmake:
        log.warning("%s %s does not seem like a CMake project",
                    project, version)

    use_cmt = os.path.exists(
        os.path.join(projectDir, os.pardir, os.pardir, "cmt", "project.cmt")
    )

    return use_cmake, use_cmt

def has_cmake(projectDir, project):
    return os.path.exists(os.path.join(projectDir, 'cmake', project + "ProjectConfig.cmake")) \
        or os.path.exists(os.path.join(projectDir, 'cmake', project + "Config.cmake")) \
        or os.path.exists(os.path.join(projectDir, project + "ProjectConfig.cmake")) \
        or os.path.exists(os.path.join(projectDir, project + "Config.cmake"))


def create_destination_directory(dest_dir):
    if not os.path.exists(dest_dir):
        log.debug('creating destination directory "%s"', dest_dir)
        os.makedirs(dest_dir)


def create_project_directory(directory, git):
    if git:
        call(["git", "init", "--quiet", directory])
    else:
        os.makedirs(directory)


def get_data_dictionary(project, version, combined_paths, use_cmake, new_project_name, new_project_version, with_fortran, name, platform):
    return dict(
        project=project,
        version=version,
        search_path=" ".join(['"%s"' % p for p in combined_paths]),
        search_path_repr=repr(combined_paths),
        search_path_env=os.pathsep.join(combined_paths),
        # we use cmake if available
        build_tool=("cmake" if use_cmake else "cmt"),
        PROJECT=project.upper(),
        local_project=new_project_name,
        local_version=new_project_version,
        with_fortran=" FORTRAN" if with_fortran else "",
        cmt_project=name,
        datadir=DATA_DIR,
        platform=platform,
    )


def add_nightly_info(data, nightly):
    if nightly:
        data["slot"], data["day"], data["base"] = nightly
        # make sure the nightly build base path is an absolute path
        data["base"] = os.path.abspath(data["base"])
    else:
        data["slot"] = data["day"] = data["base"] = ""

    return data


def create_templates(templates, data, templateDir, devProjectDir, execTemplates):
    for templateName in templates:
        t = Template(open(os.path.join(templateDir, templateName)).read())
        log.debug('creating "%s"', templateName)
        dest = os.path.join(devProjectDir, templateName)
        with open(dest, "w") as f:
            f.write(t.substitute(data))
        if templateName in execTemplates:
            mode = stat.S_IMODE(
                os.stat(dest).st_mode) | stat.S_IXUSR | stat.S_IXGRP
            os.chmod(dest, mode)


def to_SearchPath(iterable):
    return SearchPath(iterable)


def create_cmake(devProjectDir, dev_dir):
    log.debug('creating "%s"', "searchPath.cmake")
    dest = os.path.join(devProjectDir, "searchPath.cmake")
    with open(dest, "w") as f:
        f.write("# Search path defined from lb-dev command line\n")
        f.write(dev_dir.toCMake())


def create_cmt(devProjectDir, dev_dir):
    for shell in ("sh", "csh"):
        build_env_name = "build_env." + shell
        log.debug('creating "%s"', build_env_name)
        dest = os.path.join(devProjectDir, build_env_name)
        with open(dest, "w") as f:
            f.write("# Search path defined from lb-dev command line\n")
            f.write(dev_dir.toCMT(shell))


def create_requirements_file(data, templateDir, devProjectDir, new_project_name):
    t = Template(open(os.path.join(templateDir, "cmt/requirements_")).read())
    templateName = os.path.join(new_project_name + "Sys", "cmt/requirements")
    os.makedirs(os.path.dirname(os.path.join(devProjectDir, templateName)))
    log.debug('creating "%s"', templateName)
    open(os.path.join(devProjectDir, templateName), "w").write(t.substitute(data))


def create_cmake_list(devProjectDir, new_project_name, new_project_version):
    with open(
        os.path.join(devProjectDir, new_project_name +
                     "Sys", "CMakeLists.txt"),
        "w",
    ) as cml:
        cml.write(
            "gaudi_subdir({0} {1})\n".format(
                new_project_name + "Sys", new_project_version
            )
        )


def add_default_clang_format(projectDir, devProjectDir):
    upstream_style_file = os.path.join(
        projectDir, os.pardir, os.pardir, os.pardir, os.pardir, ".clang-format"
    )
    dev_style_file = os.path.join(devProjectDir, os.pardir, ".clang-format")
    if os.path.exists(upstream_style_file):
        with open(dev_style_file, "w") as f:
            f.write("# Copied from {}\n".format(upstream_style_file))
            f.writelines(open(upstream_style_file))
    else:
        # use default
        createClangFormat(dev_style_file)


def commitProjectCreation(devProjectDir):
    call(["git", "add", "."], cwd=devProjectDir)
    call(
        [
            "git",
            "commit",
            "--quiet",
            "-m",
            "initial version of satellite project\n\n"
            "generated with:\n\n"
            "    %s\n" % " ".join(sys.argv),
        ],
        cwd=devProjectDir,
    )


def reportSuccess(name, dest_dir, devProjectDir, project, platform):
    # Success report
    msg = """
Successfully created the local project {0} for {4} in {1}

To start working:

  > cd {2}
  > git lb-use {3}
  > git lb-checkout {3}/vXrY MyPackage

then

  > make
  > make test

and optionally (CMake only)

  > make install

To build for another platform call

  > make platform=<platform id>

You can customize the configuration by editing the files 'build.conf' and 'CMakeLists.txt'
(see https://twiki.cern.ch/twiki/bin/view/LHCb/GaudiCMakeConfiguration for details).
"""

    print(msg.format(name, dest_dir, devProjectDir, project, platform))
