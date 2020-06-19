import click
import yaml

import kaistack
from kaistack.components.component_store import ComponentStore
from kaistack.components.kubeflow_converter import create_workflow_template_from_component_spec


def convert_component(path):
    wf = create_workflow_template_from_component_spec(path)
    return wf


@click.command("upload-component")
@click.option("--path", required=True, help="The input file path")
@click.option("--service", help="The service endpoint")
@click.option("--name", help="The component name. If not set, it will by default use the name in the yaml")
@click.option("--source_url", help="The url of source code for the component")
@click.option("--help_link", help="The help link of the component")
@click.option("--convert", is_flag=True, default=False, help='If configured, will convert from kfp component spec. If not set, the progam will detect')
def upload_component(path, name, service, convert, help_link, source_url):
    spec = ''
    if not convert:
        # Sniff the file
        with open(path, 'r') as f:
            spec = f.read()
            convert = not spec.startswith("apiVersion")
    if convert:
        click.echo("Convert the spec")
        spec = yaml.dump(convert_component(path))

    apibase = service+"/kaistackapiserver"
    click.echo("Initialize component store. service:[{0}] api_base [{1}]".format(service, apibase))
    store = ComponentStore(service, apibase)
    try:
        try:
            store.create_component(spec, name, help_link=help_link, source_url=source_url)
            click.echo("Create component successfully")
        except kaistack.clients.openapi_clients.pipelinecomponents.exceptions.ApiException:
            store.update_component(spec, name, help_link=help_link, source_url=source_url)
            click.echo("Update component successfully")
    except kaistack.clients.openapi_clients.pipelinecomponents.exceptions.ApiException as e:
        click.echo("{0}".format(e))
