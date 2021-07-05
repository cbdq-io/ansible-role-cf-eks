# coding=utf-8
"""CloudFormation Stack feature tests."""
import json
import testinfra

from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)


@scenario('../features/cloudformation.feature', 'Verify Stack Resources')
def test_verify_stack_resources():
    """Verify Stack Resources."""


@given('CloudFormation Stack <stack_name>', target_fixture='cloudformation_stack')
def cloudformation_stack_stack_name(stack_name):
    """CloudFormation Stack <stack_name>."""
    return {
        'stack_name': stack_name
    }


@when('region is <aws_region>')
def region_is_aws_region(aws_region, cloudformation_stack):
    """region is <aws_region>."""
    stack_name = cloudformation_stack['stack_name']
    cloudformation_stack['aws_region'] = aws_region
    host = testinfra.get_host('docker://localstack')
    fmt = 'awslocal cloudformation --region %s describe-stack-resources --stack %s'
    cmd = host.run(fmt % (aws_region, stack_name))
    assert cmd.rc == 0, f'Unable to get stack details for {stack_name} in region {aws_region}.'
    cloudformation_stack['StackResources'] = json.loads(cmd.stdout)['StackResources']


@then('verify stack resource <resource_id> is of type <resource_type>')
def verify_stack_resource_resource_id_is_of_type_resource_type(resource_id, resource_type, cloudformation_stack):
    """verify stack resource <resource_id> is of type <ResourceType>."""
    resource_is_present = False

    for resource in cloudformation_stack['StackResources']:
        if resource['LogicalResourceId'] == resource_id:
            resource_is_present = True
            break

    assert resource_is_present, f'Resource {resource_id} is missing from stack {cloudformation_stack["stack_name"]}'
    fmt = 'Wrong resource type (%s), for resource_id %s.  Expected %s.'
    assert resource['ResourceType'] == resource_type, fmt % (resource['ResourceType'], resource_id, resource_type)
