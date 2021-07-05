Feature: CloudFormation
  Scenario Outline: Test Stack Resources
    Given CloudFormation Stack <stack_name>
    When region is <aws_region>
    Then verify stack resource <resource_id> is of type <resource_type>
    Examples:
      | stack_name | aws_region | resource_id           | resource_type             |
      | bastion    | eu-west-2  | EC2Instance           | AWS::EC2::Instance        |
