import boto3
from botocore.handlers import json_decode_template_body
import json


def dict_to_cfn_params(dict_params) -> list:
    """Description:
        Converts a `dict` to CloudFormation parameters

    Args:
        dict_params: Dictionary that needs to be converted to CloudFormation parameters

    Example:
        Example usage:

            >>> from onnmisc.aws.cfn import dict_to_cfn_params
            >>> params = {
                'AccountId': '123456789012',
                'ExternalId': '098765432109',
                }
            >>>
            >>> cfn_params = dict_to_cfn_params(params)
            >>> pprint(cfn_params)
            [{'ParameterKey': 'AccountId', 'ParameterValue': '123456789012'},
            {'ParameterKey': 'ExternalId', 'ParameterValue': '098765432109'}]

    Returns:
        List of CloudFormation parameters
    """
    cfn_params = []

    for key, value in dict_params.items():
        entry = {
            'ParameterKey': key,
            'ParameterValue': value,
        }

        cfn_params.append(entry)

    return cfn_params


def get_template(stack_name) -> dict:
    """Description:
        Extracts CloudFormation templates from existing stack

    Args:
        stack_name: Name of the CloudFormation stack

    Example:
        Example usage:

            >>> from onnmisc.aws.cfn import get_template
            >>> from pprint import pprint
            >>>
            >>> template = get_template('demo_template')
            >>> pprint(template)
            {'Resources': {'Instance': {'Properties': {'ImageId': 'ami-0d1deba769f118333',
                                           'InstanceType': 't2.medium',
                                           'NetworkInterfaces': [{'AssociatePublicIpAddress': True,
                                           ...

    Returns:
        CloudFormation template as a dict
    """
    cf_client = boto3.client('cloudformation')

    # workaround for https://github.com/boto/botocore/issues/1889
    cf_client.meta.events.unregister('after-call.cloudformation.GetTemplate', json_decode_template_body)
    original_cfn_template = cf_client.get_template(StackName=stack_name)['TemplateBody']
    cfn_template_removed_newline = original_cfn_template.replace('\n', '')
    dict_template = json.loads(cfn_template_removed_newline)

    return dict_template


def cfn_outputs_to_dict(cfn_outputs) -> dict:
    """Description:
        Converts CloudFormation outputs to a dict

    Args:
        cfn_outputs: CloudFormation outputs

    Example:
        Example usage:

            >>> from onnmisc.aws.cfn import cfn_outputs_to_dict
            >>> import boto3
            >>>
            >>> client = boto3.client('cloudformation')
            >>> stack = client.describe_stacks(StackName='demo')
            >>> outputs = stack['Stacks'][0]['Outputs']
            >>> output_dict = outputs_to_dict(outputs)
            >>> print(output_dict)
            {'VpcId': 'vpc-h4vfg234322', 'PublicSubnetId': 'subnet-k64564ghfhf'}

    Returns:
        CloudFormation outputs as a dict
    """
    output = {}
    for entry in cfn_outputs:
        key = entry['OutputKey']
        value = entry['OutputValue']
        output[key] = value

    return output


def cfn_tags_to_dict(cfn_tags) -> dict:
    """Description:
        Converts CloudFormation tags to a dict

    Args:
        cfn_tags: CloudFormation tags

    Example:
        Example usage:

            >>> from onnmisc.aws.cfn import cfn_tags_to_dict
            >>> import boto3
            >>>
            >>> client = boto3.client('cloudformation')
            >>> described_cfn = client.describe_stacks(StackName='demo')
            >>> get_cfn_tags = described_cfn['Stacks'][0]['Tags']
            >>> tags = cfn_tags_to_dict(get_cfn_tags)
            >>> print(tags)
            {'aws:cloud9:environment': 'rew34e242342421das032', 'aws:cloud9:owner': 'FJ3IK24JLSDF9233H4'}

    Returns:
        CloudFormation outputs as a dict
    """
    output = {}
    for entry in cfn_tags:
        key = entry['Key']
        value = entry['Value']
        output[key] = value

    return output


def dict_to_cfn_tags(cfn_dict) -> list:
    """Description:
        Converts a dictionary to CloudFormation tags

    Args:
        cfn_dict: Dictionary to be converted

    Example:
        Example usage:

            >>> from onnmisc.aws.cfn import dict_to_cfn_tags
            >>>
            >>> dict_tags = {'Name': 'nginx', 'Team': 'frontend'}
            >>> tags = dict_to_cfn_tags(dict_tags)
            >>> print(tags)
            [{'Key': 'Name', 'Value': 'nginx'}, {'Key': 'Team', 'Value': 'frontend'}]


    Returns:
        List of CloudFormation tags

    """
    output = []

    for key, value in cfn_dict.items():
        entry = {
            'Key': key,
            'Value': value,
        }

        output.append(entry)

    return output
