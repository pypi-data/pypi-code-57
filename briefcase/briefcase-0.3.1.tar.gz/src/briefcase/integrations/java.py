import shutil
import subprocess
from pathlib import Path

from requests import exceptions as requests_exceptions

from briefcase.exceptions import BriefcaseCommandError, NetworkFailure


def verify_jdk(command):
    """
    Verify that a Java 8 JDK exists.

    If ``JAVA_HOME`` is set, try that version. If it is a JRE, or its *not*
    a Java 8 JDK, download one.

    On macOS, also try invoking /usr/libexec/java_home. If that location points
    to a Java 8 JDK, use it.

    Otherwise, download a JDK from AdoptOpenJDK and unpack it into the
    ``~.briefcase`` path.

    :param command: The command that needs to perform the verification check.
    :returns: The value for ``JAVA_HOME``
    """
    java_home = command.os.environ.get('JAVA_HOME', '')
    install_message = None

    # macOS has a helpful system utility to determine JAVA_HOME. Try it.
    if not java_home and command.host_os == 'Darwin':
        try:
            # If no JRE/JDK is installed, /usr/libexec/java_home
            # raises an error.
            java_home = command.subprocess.check_output(
                ['/usr/libexec/java_home'],
                universal_newlines=True,
                stderr=subprocess.STDOUT,
            ).strip('\n')
        except subprocess.CalledProcessError:
            # No java on this machine.
            pass

    if java_home:
        try:
            # If JAVA_HOME is defined, try to invoke javac.
            # This verifies that we have a JDK, not a just a JRE.
            output = command.subprocess.check_output(
                [
                    str(Path(java_home) / 'bin' / 'javac'),
                    '-version',
                ],
                universal_newlines=True,
                stderr=subprocess.STDOUT,
            )
            # This should be a string of the form "javac 1.8.0_144\n"
            version_str = output.strip('\n').split(' ')[1]
            vparts = version_str.split('.')
            if len(vparts) == 3 and vparts[:2] == ['1', '8']:
                # It appears to be a Java 8 JDK.
                return Path(java_home)
            else:
                # It's not a Java 8 JDK.
                java_home = None
                install_message = """
*************************************************************************
** WARNING: JAVA_HOME does not point to a Java 8 JDK                   **
*************************************************************************

    Android requires a Java 8 JDK, but the location pointed to by the
    JAVA_HOME environment variable:

     {java_home}

    isn't a Java 8 JDK (it appears to be Java {version_str}).

    Briefcase will use its own JDK instance.

*************************************************************************

""".format(java_home=java_home, version_str=version_str)

        except FileNotFoundError:
            java_home = None
            install_message = """
*************************************************************************
** WARNING: JAVA_HOME does not point to a JDK                          **
*************************************************************************

    The location pointed to by the JAVA_HOME environment variable:

     {java_home}

    does not appear to be a JDK. It may be a Java Runtime Environment.

    Briefcase will use its own JDK instance.

*************************************************************************

""".format(java_home=java_home)

        except subprocess.CalledProcessError:
            java_home = None
            install_message = """
*************************************************************************
** WARNING: Unable to invoke the Java compiler                         **
*************************************************************************

   Briefcase received an unexpected error when trying to invoke javac,
   the Java compiler, at the location indicated by the JAVA_HOME
   environment variable.

   Briefcase will continue by downloading and using its own JDK.

   Please report this as a bug at:

     https://github.com/beeware/briefcase/issues/new


   In your report, please including the output from running:

     {java_home}/bin/javac -version

   from the command prompt.

*************************************************************************

""".format(java_home=java_home)

        except IndexError:
            java_home = None
            install_message = """
*************************************************************************
** WARNING: Unable to determine the version of Java that is installed  **
*************************************************************************

   Briefcase was unable to interpret the version information returned
   by the Java compiler at the location indicated by the JAVA_HOME
   environment variable.

   Briefcase will continue by downloading and using its own JDK.

   Please report this as a bug at:

     https://github.com/beeware/briefcase/issues/new


   In your report, please including the output from running:

     {java_home}/bin/javac -version

   from the command prompt.

*************************************************************************

""".format(java_home=java_home)

    # If we've reached this point, any user-provided JAVA_HOME is broken;
    # use the Briefcase one.
    java_home = command.dot_briefcase_path / 'tools' / 'java'

    # The macOS download has a weird layout (inherited from the official Oracle
    # release). The actual JAVA_HOME is deeper inside the directory structure.
    if command.host_os == 'Darwin':
        java_home = java_home / 'Contents' / 'Home'

    if (java_home / 'bin').exists():
        # Using briefcase cached Java version
        return java_home

    # We only display the warning messages on the pass where we actually
    # install the JDK.
    if install_message:
        print(install_message)

    print("Obtaining a Java 8 JDK...")

    # As of April 10 2020, 8u242-b08 is the current AdoptOpenJDK
    # https://adoptopenjdk.net/releases.html
    jdk_release = '8u242'
    jdk_build = 'b08'
    jdk_platform = {
        'Darwin': 'mac',
        'Windows': 'windows',
        'Linux': 'linux',
    }.get(command.host_os)
    extension = {
        'Windows': 'zip',
    }.get(command.host_os, 'tar.gz')

    jdk_url = (
        'https://github.com/AdoptOpenJDK/openjdk8-binaries/'
        'releases/download/jdk{jdk_release}-{jdk_build}/'
        'OpenJDK8U-jdk_x64_{jdk_platform}_hotspot_{jdk_release}{jdk_build}.{extension}'
    ).format(
        jdk_release=jdk_release,
        jdk_build=jdk_build,
        jdk_platform=jdk_platform,
        extension=extension,
    )

    try:
        jdk_zip_path = command.download_url(
            url=jdk_url,
            download_path=command.dot_briefcase_path / "tools",
        )
    except requests_exceptions.ConnectionError:
        raise NetworkFailure("download Java 8 JDK")
    try:
        command.shutil.unpack_archive(
            str(jdk_zip_path),
            extract_dir=str(command.dot_briefcase_path / "tools")
        )
    except (shutil.ReadError, EOFError):
        raise BriefcaseCommandError(
            """\
Unable to unpack AdoptOpenJDK ZIP file. The download may have been interrupted
or corrupted.

Delete {jdk_zip_path} and run briefcase again.""".format(
                jdk_zip_path=jdk_zip_path
            )
        )
    jdk_zip_path.unlink()  # Zip file no longer needed once unpacked.

    # The tarball will unpack into ~.briefcase/tools/jdk8u242-b08
    # (or whatever name matches the current release).
    # We turn this into ~.briefcase/tools/java so we have a consistent name.
    java_unpack_path = command.dot_briefcase_path / "tools" / "jdk{jdk_release}-{jdk_build}".format(
        jdk_release=jdk_release,
        jdk_build=jdk_build,
    )
    java_unpack_path.rename(command.dot_briefcase_path / "tools" / "java")
    print()

    return java_home
