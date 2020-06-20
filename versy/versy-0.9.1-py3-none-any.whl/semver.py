import semver as _semver


def semver(s):
    try:
        return _semver.VersionInfo.parse(s)
    except Exception:
        raise ValueError('"%s" was not a valid version number' % s)


def bump(version, action):
    if action == 'patch':
        return version.bump_patch()
    if action == 'minor':
        return version.bump_minor()
    if action == 'major':
        return version.bump_major()
    try:
        v = _semver(action)
    except ValueError:
        raise ValueError('Unknown action %s' % action)

    if v <= version:
        raise ValueError('%s <= current version %s' % (v, version))

    return v
