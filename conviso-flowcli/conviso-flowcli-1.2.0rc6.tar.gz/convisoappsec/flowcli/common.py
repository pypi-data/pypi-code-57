import click
from pipes import quote
import io


class DeployFormatter(object):
    DEFAULT = 'default'
    ENV_VARS = 'env_vars'

    def __init__(self, deploy):
        self.deploy = deploy
        self.format_strategies = {
            self.DEFAULT: self.default_format,
            self. ENV_VARS: self.env_vars_format,
        }

    def format_as(self, format):
        if format not in self.format_strategies:
            raise ValueError(
                "Allowed deploy formats[{0}]. Given {1}".format(
                  "|".join(FORMATS),
                  format,
                )
            )

        strategy = self.format_strategies[format]
        return strategy()

    @classmethod
    def FORMATS(cls):
        return [
            cls.DEFAULT,
            cls.ENV_VARS,
       ]

    def env_vars_format(self):
        to_env_vars_translation_args = [
            # (env_var_name, attrib_name, attrib_default_val)
            ('FLOW_DEPLOY_ID', 'id', ''),
            ('FLOW_DEPLOY_CREATED_AT', 'created_at', ''),
            ('FLOW_DEPLOY_CURRENT_VERSION_TAG', 'current_tag', ''),
            ('FLOW_DEPLOY_PREVIOUS_VERSION_TAG', 'previous_tag', ''),
            ('FLOW_DEPLOY_CURRENT_VERSION_COMMIT', 'current_commit', ''),
            ('FLOW_DEPLOY_PREVIOUS_VERSION_COMMIT', 'previous_commit', ''),
        ]


        env_vars = {}

        for arg in to_env_vars_translation_args:
            env_var_name, attrib_name, attrib_default_val = arg

            env_var_val = env_vars[env_var_name] = self.deploy.get(
                attrib_name, attrib_default_val
            )

            env_vars[env_var_name] = str(env_var_val)

        buffer = io.StringIO()

        for var_name, var_val in env_vars.items():
            line_fmt = "{name}={value}"
            line = line_fmt.format(
              name=quote(var_name),
              value=quote(var_val),
            )


            print(line, file=buffer)

        buffer.seek(0)
        return buffer.read()


    def default_format(self):
        default_fmt = '''
Created deploy:
  current_version.commit={current_commit}
  current_version.tag={current_tag}
  previous_version.commit={previous_commit}
  previous_version.tag={previous_tag}
        '''

        return default_fmt.format(
            **self.deploy
        )


def notify_created_deploy(deploy):
    formatter = DeployFormatter(deploy)
    click.echo(formatter.default_format())
