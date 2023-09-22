################################################################################
# SAN99TIAGODEMO AWS ORGANIZATION (INFRASTRUCTURE AS CODE CDK SOLUTION)
# ! --> PLEASE SEE NOTES ON "stacks/cdk_organization.py" file. (IMPORTANT)
################################################################################

# Built-in imports
import os

# External imports
import aws_cdk as cdk

# Own imports
from helpers.add_tags import add_tags_to_app
from stacks.cdk_organization import OrganizationStack


print("--> Deployment AWS configuration (safety first):")
print("CDK_DEFAULT_ACCOUNT", os.getenv("CDK_DEFAULT_ACCOUNT"))
print("CDK_DEFAULT_REGION", os.getenv("CDK_DEFAULT_REGION"))

app = cdk.App()

# Configurations for the deployment (obtained from env vars and CDK context)
DEPLOYMENT_ENVIRONMENT = os.environ.get("DEPLOYMENT_ENVIRONMENT", "prod")
MAIN_RESOURCES_NAME = app.node.try_get_context("main_resources_name")


org_stack = OrganizationStack(
    app,
    MAIN_RESOURCES_NAME,
    DEPLOYMENT_ENVIRONMENT,
    env={
        "account": os.getenv("CDK_DEFAULT_ACCOUNT"),
        "region": os.getenv("CDK_DEFAULT_REGION"),
    },
    description="Stack for {} infrastructure in {} environment".format(
        MAIN_RESOURCES_NAME, DEPLOYMENT_ENVIRONMENT
    ),
)

add_tags_to_app(
    app,
    MAIN_RESOURCES_NAME,
    DEPLOYMENT_ENVIRONMENT,
)

app.synth()
