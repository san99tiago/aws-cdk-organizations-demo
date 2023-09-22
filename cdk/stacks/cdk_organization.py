################################################################################
# SAN99TIAGODEMO AWS ORGANIZATION (INFRASTRUCTURE AS CODE CDK SOLUTION)
# NOTE 1: I am using a CDK-based approach that is not maintained by AWS (yet):
# --> https://github.com/pepperize/cdk-organizations
# NOTE 2: As multiple accounts are being created, there are some "CDK" node
# ... dependencies. See example at the end on the source repo (link above)
################################################################################

# Built-in imports
import os
import json

# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
)
from constructs import Construct
from pepperize_cdk_organizations import (
    Account,
    FeatureSet,
    Organization,
    OrganizationalUnit,
    Policy,
    PolicyType,
)


class OrganizationStack(Stack):
    """
    Class to create the infrastructure of the AWS Organizations.
    """

    def __init__(
        self, scope: Construct, construct_id: str, deployment_environment: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.construct_id = construct_id
        self.deployment_environment = deployment_environment

        # Organization creation, services configuration and SCPs
        self.create_root_organization()
        self.configure_organization_services()
        self.configure_service_control_policies()

        # Create "sandbox" OU with inner OUs and accounts inside
        self.create_ou_sandbox()
        self.create_accounts_inside_ou_sandbox()

        # !IMPORTANT: this is mandatory for adding CDK dependencies for each account
        self.add_cdk_accounts_dependencies()  # DO NOT REMOVE!

        # Create CloudFormation outputs
        self.generate_cloudformation_outputs()

    def create_root_organization(self):
        """
        Method that creates the AWS Organization (root).
        """
        self.organization = Organization(
            self,
            id="RootOrganization",
            feature_set=FeatureSet.ALL,
        )

    def configure_organization_services(self):
        """
        Method that configures the AWS Organization with the desired enabled
        services and policies (enable the desired ones).
        """
        # Note 1: for more details on services, see full list at:
        # --> https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_services_list.html
        # Note 2: for more details on policies, see full list at:
        # --> https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies.html

        # Enable service for AWS IAM Identity Center (AWS Single Sign-On Dashboard)
        self.organization.enable_aws_service_access("sso.amazonaws.com")

        # Enable service for Resource Access Manager (RAM)
        self.organization.enable_aws_service_access("ram.amazonaws.com")

        # Enable Service Control Policies (SCPs)
        self.organization.enable_policy_type(PolicyType.SERVICE_CONTROL_POLICY)

    def configure_service_control_policies(self):
        """
        Method that configures the AWS Organization with the desired Service
        Control Policies (SCPs) at organization level.
        """

        # Get OS path to SCPs files and load them (for easier read/write of SCPs)
        path_scp_prevent_leaving_org = os.path.join(
            os.path.dirname(__file__),
            "scp_prevent_leaving_org.json",
        )
        with open(path_scp_prevent_leaving_org, "r") as file:
            scp_prevent_leaving_org = json.load(file)

        path_scp_allow_specific_regions = os.path.join(
            os.path.dirname(__file__),
            "scp_allow_specific_regions.json",
        )
        with open(path_scp_allow_specific_regions, "r") as file:
            scp_allow_specific_regions = json.load(file)

        # SCP for preventing accounts of leaving organization
        self.policy_deny_leave_org = Policy(
            self,
            id="PolicyDenyLeave",
            content=json.dumps(scp_prevent_leaving_org),
            policy_name="PreventLeavingOrganization",
            policy_type=PolicyType.SERVICE_CONTROL_POLICY,
            description="SCP to prevent accounts from leaving the organization",
        )
        self.organization.attach_policy(self.policy_deny_leave_org)

        # SCP for only allow access to specific regions in AWS (deny others)
        self.policy_allow_specific_regions = Policy(
            self,
            id="PolicyAllowSpecificRegions",
            content=json.dumps(scp_allow_specific_regions),
            policy_name="AllowSpecificRegions",
            policy_type=PolicyType.SERVICE_CONTROL_POLICY,
            description="SCP to only allow access to specific AWS Regions",
        )
        self.organization.attach_policy(self.policy_allow_specific_regions)

    def create_ou_sandbox(self):
        """
        Method that creates inner Organizational Units (OUs) inside organization.
        """
        self.top_level_ou_sandbox = OrganizationalUnit(
            self,
            id="SandboxOU",
            parent=self.organization.root,
            organizational_unit_name="sandbox",
        )

    def create_accounts_inside_ou_sandbox(self):
        """
        Method that creates AWS Accounts inside the required Organizational
        Units (OUs).
        """
        self.account_sandbox_1 = Account(
            self,
            id="SandboxAccount1",
            account_name="san99tiago-sandbox-1",
            email="san99tiagodemo+san99tiago-sandbox-1@gmail.com",
            parent=self.top_level_ou_sandbox,
            role_name="OrganizationAccountAccessRole",
        )
        self.account_sandbox_2 = Account(
            self,
            id="SandboxAccount2",
            account_name="san99tiago-sandbox-2",
            email="san99tiagodemo+san99tiago-sandbox-2@gmail.com",
            parent=self.top_level_ou_sandbox,
            role_name="OrganizationAccountAccessRole",
        )

    def add_cdk_accounts_dependencies(self):
        """
        ULTRA IMPORTANT METHOD to add CDK dependencies for the AWS Accounts that
        are being created (to avoid 2 accounts creation simultaneously, which is
        not supported by AWS). This is because of AWS Organizations limitation.
        """
        # ! IMPORTANT: We MUST add these dependencies, as AWS Organizations only support
        # ... one account creation "IN_PROGRESS". We add CDK dependency to solve issue
        # ... and wait for the previous one to finish, to continue with the next...
        self.account_sandbox_2.node.add_dependency(self.account_sandbox_1)

    def generate_cloudformation_outputs(self):
        """
        Method to add the relevant CloudFormation outputs.
        """

        CfnOutput(
            self,
            "DeploymentEnvironment",
            value=self.deployment_environment,
            description="Deployment environment",
        )

        CfnOutput(
            self,
            "OrganizationId",
            value=self.organization.organization_id,
            description="ID of the Organization",
        )

        CfnOutput(
            self,
            "RootId",
            value=self.organization.root.identifier(),
            description="ID of the Root OU",
        )

        CfnOutput(
            self,
            "ManagementAccountId",
            value=self.organization.management_account_id,
            description="ID of the Management Account",
        )

        CfnOutput(
            self,
            "ManagementAccountEmail",
            value=self.organization.management_account_email,
            description="Email of the Management Account",
        )

        CfnOutput(
            self,
            "AccountSandbox1Id",
            value=self.account_sandbox_1.account_id,
            description="ID of the SandboxAccount1",
        )

        CfnOutput(
            self,
            "AccountSandbox2Id",
            value=self.account_sandbox_2.account_id,
            description="ID of the SandboxAccount2",
        )
