def create_server(spec_dir, custom_home=None,
                  port=8080, debug=False):
    import connexion
    import os
    import yaml

    app = connexion.FlaskApp(
        __name__, port=port,
        specification_dir=spec_dir, debug=debug
    )

    @app.route('/')
    def health_check():
        if custom_home is not None:
            return custom_home()
        else:
            return home()

    for spec in os.listdir(spec_dir):
        app.add_api(specification=spec, validate_responses=debug)

    framework_dir = os.path.abspath(__file__).replace('/core/server.py', '/')

    for root, folders, files in os.walk(framework_dir):
        if 'schemas' in root and 'template' not in root:
            for spec_file in [i for i in files if 'yaml' in i]:
                with open(os.path.join(root, spec_file), 'rt') as f:
                    spec = yaml.safe_load(f)
                app.add_api(specification=spec, validate_responses=debug)
    return app


def home():
    return dict(status='ok')


def say_hello():
    from stratus_api.core.requests import get_request_access_token
    token = get_request_access_token()
    return dict(response='hello {token}'.format(token=token))
