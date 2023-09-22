from aws_cdk import aws_sns as sns
import aws_cdk as cdk
from aws_cdk.assertions import Template

from cdk.stacks.cdk_organization import OrganizationStack


def test_synthesizes_properly():
    app = cdk.App()

    # Create the TestOrganizationStack with sample params
    deployment_env = "prod"
    main_resources_name = "test-organization"
    state_machine_stack = OrganizationStack(
        app,
        main_resources_name,
        deployment_env,
    )

    # Prepare the stack for assertions.
    template = Template.from_stack(state_machine_stack)

    template.has_output(
        "DeploymentEnvironment",
        {
            "Description": "Deployment environment",
            "Value": deployment_env,
        },
    )
