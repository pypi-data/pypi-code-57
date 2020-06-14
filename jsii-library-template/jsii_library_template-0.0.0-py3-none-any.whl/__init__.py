"""
# jsii-library-template

Template for a jsii library project.

## Configuration

1. Edit `.projenrc.js` and go through all the fields to update for your project.
2. Add the following GitHub secrets to your project (see [jsii-release](https://github.com/eladb/jsii-release) for instructions):

   * `NPM_TOKEN`
   * `MAVEN_USERNAME`, `MAVEN_PASSWORD`, `MAVEN_GPG_PRIVATE_KEY`, `MAVEN_GPG_PRIVATE_KEY_PASSPHRASE`, `MAVEN_STAGING_PROFILE_ID`,
   * `TWINE_USERNAME`, `TWINE_PASSWORD`
   * `NUGET_API_KEY`

## Usage

This is a [projen](https://github.com/eladb/projen) project. This means that all project configuration is derived from [.projenrc.js](./.projenrc.js) and generated on-demand.

After cloning this repo, run:

```
  npx projen
```

In order to bootstrap project configuration files, like `package.json`.

Then, you can use `yarn` for your workflow:

| Command          | Description                                       |
|------------------|---------------------------------------------------|
|`yarn install`    |Install dependencies                               |
|`yarn compile`    |Compile to JavaScript                              |
|`yarn watch`      |Watch for changes and compile                      |
|`yarn test`       |Run tests                                          |
|`yarn run package`|Create `dist` with bundles for all languages       |
|`yarn build`      |Compile + test + package                           |
|`yarn bump`       |Bump a new version (based on conventional commits) |
|`yarn release`    |Bump + push                                        |
|`yarn compat`     |Run API compatibility check against latest         |
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *


class Hello(metaclass=jsii.JSIIMeta, jsii_type="jsii-library-template.Hello"):
    """Hello class.

    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(Hello, self, [])

    @jsii.member(jsii_name="world")
    def world(self) -> str:
        """Hey there!

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "world", [])


__all__ = [
    "Hello",
]

publication.publish()
