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
    RemovalPolicy,
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
    Class to create the infrastructure for AWS Organizations.
    """

    def __init__(
        self, scope: Construct, construct_id: str, deployment_environment: str, **kwargs
    ) -> None:
        """
        :param scope (Construct): Parent of this stack, usually an ``App`` or a ``Stage``, but could be any construct.
        :param construct_id (str): The construct ID of this stack.
        :param main_resources_name (str): The main solution name being deployed.
        :param deployment_environment (str): Value that represents the deployment environment. For example: "dev" or "prod".
        """
        super().__init__(scope, construct_id, **kwargs)

        self.construct_id = construct_id
        self.deployment_environment = deployment_environment

        # AWS Organization creation, services configuration and SCPs
        self.create_root_organization()
        self.configure_organization_services()
        self.configure_service_control_policies()

        # Create "sandbox" OU with inner OUs and accounts inside
        self.create_ou_sandbox()
        self.create_accounts_inside_ou_sandbox()

        # Create "infrastructure" OU with inner OUs and accounts inside
        self.create_ou_infrastructure()
        self.create_accounts_inside_ou_infrastructure()

        # Create "workloads" OU with inner OUs and accounts inside
        self.create_ou_workloads()
        self.create_ou_finance()
        self.create_accounts_inside_ou_finance()
        self.create_ou_marketing()
        self.create_accounts_inside_ou_marketing()

        # Create "policy_staging_tests" OU with inner OUs and accounts inside
        self.create_ou_policy_staging_tests()
        self.create_accounts_inside_ou_policy_staging_tests()

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
            "RootOrganization",
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
            "PolicyDenyLeave",
            content=json.dumps(scp_prevent_leaving_org),
            policy_name="PreventLeavingOrganization",
            policy_type=PolicyType.SERVICE_CONTROL_POLICY,
            description="SCP to prevent accounts from leaving the organization",
        )
        self.organization.attach_policy(self.policy_deny_leave_org)

        # SCP for only allow access to specific regions in AWS (deny others)
        self.policy_allow_specific_regions = Policy(
            self,
            "PolicyAllowSpecificRegions",
            content=json.dumps(scp_allow_specific_regions),
            policy_name="AllowSpecificRegions",
            policy_type=PolicyType.SERVICE_CONTROL_POLICY,
            description="SCP to only allow access to specific AWS Regions",
        )
        self.organization.attach_policy(self.policy_allow_specific_regions)

    def create_ou_sandbox(self):
        """
        Method that creates inner Organizational Units (OUs) inside the AWS
        Organization for "Sandbox".
        """
        self.top_level_ou_sandbox = OrganizationalUnit(
            self,
            "SandboxOU",
            parent=self.organization.root,
            organizational_unit_name="sandbox",
        )

    def create_accounts_inside_ou_sandbox(self):
        """
        Method that creates AWS Accounts inside the Organizational Units (OUs)
        for "Sandbox".
        """
        self.account_sandbox_1 = Account(
            self,
            "SandboxAccount1",
            account_name="san99tiago-sandbox-1",
            email="san99tiagodemo+san99tiago-sandbox-1@gmail.com",
            parent=self.top_level_ou_sandbox,
            role_name="OrganizationAccountAccessRole",
        )

        # # DELETED TO AVOID LIMIT QUOTA OF 10 ACCOUNTS IN DEMO
        # self.account_sandbox_2 = Account(
        #     self,
        #     "SandboxAccount2",
        #     account_name="san99tiago-sandbox-2",
        #     email="san99tiagodemo+san99tiago-sandbox-2@gmail.com",
        #     parent=self.top_level_ou_sandbox,
        #     role_name="OrganizationAccountAccessRole",
        # )

    def create_ou_infrastructure(self):
        """
        Method that creates inner Organizational Units (OUs) inside the AWS
        Organization for "Infrastructure".
        """
        self.top_level_ou_infrastructure = OrganizationalUnit(
            self,
            "OUInfrastructure",
            parent=self.organization.root,
            organizational_unit_name="infrastructure",
        )
        self.ou_infrastructure_non_prod = OrganizationalUnit(
            self,
            "OUInfrastructureNonProd",
            parent=self.top_level_ou_infrastructure,
            organizational_unit_name="non-prod",
        )
        self.ou_infrastructure_prod = OrganizationalUnit(
            self,
            "OUInfrastructureProd",
            parent=self.top_level_ou_infrastructure,
            organizational_unit_name="prod",
        )

    def create_accounts_inside_ou_infrastructure(self):
        """
        Method that creates AWS Accounts inside the Organizational Units (OUs)
        for "Infrastructure".
        """
        self.account_shared_services_non_prod = Account(
            self,
            "AccountSharedServicesNonProd",
            account_name="shared-services-non-prod",
            email="san99tiagodemo+shared-services-non-prod@gmail.com",
            parent=self.ou_infrastructure_non_prod,
            role_name="OrganizationAccountAccessRole",
        )
        self.account_shared_services_prod = Account(
            self,
            "AccountSharedServicesProd",
            account_name="shared-services-prod",
            email="san99tiagodemo+shared-services-prod@gmail.com",
            parent=self.ou_infrastructure_prod,
            role_name="OrganizationAccountAccessRole",
        )

    def create_ou_workloads(self):
        """
        Method that creates inner Organizational Units (OUs) inside the AWS
        Organization for "Workloads".
        """
        self.top_level_ou_workloads = OrganizationalUnit(
            self,
            "OUWorkloads",
            parent=self.organization.root,
            organizational_unit_name="workloads",
        )

    def create_ou_finance(self):
        """
        Method that creates inner Organizational Units (OUs) inside the AWS
        Organization for "Finance".
        """
        self.ou_finance = OrganizationalUnit(
            self,
            "OUFinance",
            parent=self.top_level_ou_workloads,
            organizational_unit_name="finance",
        )
        self.ou_finance_non_prod = OrganizationalUnit(
            self,
            "OUFinanceNonProd",
            parent=self.ou_finance,
            organizational_unit_name="non-prod",
        )
        self.ou_finance_prod = OrganizationalUnit(
            self,
            "OUFinanceProd",
            parent=self.ou_finance,
            organizational_unit_name="prod",
        )

    def create_accounts_inside_ou_finance(self):
        """
        Method that creates AWS Accounts inside the Organizational Units (OUs)
        for "Finance".
        """
        self.account_finance_dev = Account(
            self,
            "AccountFinanceDev",
            account_name="finance-dev",
            email="san99tiagodemo+finance-dev@gmail.com",
            parent=self.ou_finance_non_prod,
            role_name="OrganizationAccountAccessRole",
        )
        self.account_finance_qa = Account(
            self,
            "AccountFinanceQA",
            account_name="finance-qa",
            email="san99tiagodemo+finance-qa@gmail.com",
            parent=self.ou_finance_non_prod,
            role_name="OrganizationAccountAccessRole",
        )
        self.account_finance_prod = Account(
            self,
            "AccountFinanceProd",
            account_name="finance-prod",
            email="san99tiagodemo+finance-prod@gmail.com",
            parent=self.ou_finance_prod,
            role_name="OrganizationAccountAccessRole",
        )

    def create_ou_marketing(self):
        """
        Method that creates inner Organizational Units (OUs) inside the AWS
        Organization for "Marketing".
        """
        self.ou_marketing = OrganizationalUnit(
            self,
            "OUMarketing",
            parent=self.top_level_ou_workloads,
            organizational_unit_name="marketing",
        )
        self.ou_marketing_non_prod = OrganizationalUnit(
            self,
            "OUMarketingNonProd",
            parent=self.ou_marketing,
            organizational_unit_name="non-prod",
        )
        self.ou_marketing_prod = OrganizationalUnit(
            self,
            "OUMarketingProd",
            parent=self.ou_marketing,
            organizational_unit_name="prod",
        )

    def create_accounts_inside_ou_marketing(self):
        """
        Method that creates AWS Accounts inside the Organizational Units (OUs)
        for "Marketing".
        """
        self.account_marketing_dev = Account(
            self,
            "AccountMarketingDev",
            account_name="marketing-dev",
            email="san99tiagodemo+marketing-dev@gmail.com",
            parent=self.ou_marketing_non_prod,
            role_name="OrganizationAccountAccessRole",
            removal_policy=RemovalPolicy.RETAIN,
            import_on_duplicate=True,
        )

        self.account_marketing_prod = Account(
            self,
            "AccountMarketingProd",
            account_name="marketing-prod",
            email="san99tiagodemo+marketing-prod@gmail.com",
            parent=self.ou_marketing_prod,
            role_name="OrganizationAccountAccessRole",
        )

    def create_ou_policy_staging_tests(self):
        """
        Method that creates inner Organizational Units (OUs) inside the AWS
        Organization for "PolicyStagingTests".
        """
        self.top_level_ou_policy_staging_tests = OrganizationalUnit(
            self,
            "OUPolicyStagingTests",
            parent=self.organization.root,
            organizational_unit_name="policy-staging-tests",
        )

    def create_accounts_inside_ou_policy_staging_tests(self):
        """
        Method that creates AWS Accounts inside the Organizational Units (OUs)
        for "PolicyStagingTests".
        """
        self.account_policy_staging_tests = Account(
            self,
            "AccountPolicyStagingTests",
            account_name="policy-staging-tests",
            email="san99tiagodemo+policy-staging-tests@gmail.com",
            parent=self.top_level_ou_policy_staging_tests,
            role_name="OrganizationAccountAccessRole",
        )

    def add_cdk_accounts_dependencies(self):
        """
        IMPORTANT METHOD to add CDK dependencies for the AWS Accounts that are
        being created (to avoid 2 accounts creation simultaneously, which is
        not supported by AWS). This is because of AWS Organizations limitation.
        """
        # ! IMPORTANT: We MUST add these dependencies, as AWS Organizations only support
        # ... one account creation "IN_PROGRESS". We add CDK dependency to solve issue
        # ... and wait for the previous one to finish, to continue with the next...
        self.account_shared_services_non_prod.node.add_dependency(
            self.account_sandbox_1
        )
        self.account_shared_services_prod.node.add_dependency(
            self.account_shared_services_non_prod
        )
        self.account_finance_dev.node.add_dependency(self.account_shared_services_prod)
        self.account_finance_qa.node.add_dependency(self.account_finance_dev)
        self.account_finance_prod.node.add_dependency(self.account_finance_qa)
        self.account_marketing_dev.node.add_dependency(self.account_finance_prod)
        self.account_marketing_prod.node.add_dependency(self.account_marketing_dev)
        self.account_policy_staging_tests.node.add_dependency(
            self.account_marketing_prod
        )

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
            description="ID of AWS Organization",
        )

        CfnOutput(
            self,
            "RootId",
            value=self.organization.root.identifier(),
            description="ID of AWS Organization Root OU",
        )

        CfnOutput(
            self,
            "ManagementAccountId",
            value=self.organization.management_account_id,
            description="ID of Management Account",
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
            description="ID of SandboxAccount1 Account",
        )

        CfnOutput(
            self,
            "AccountSharedServicesNonProdId",
            value=self.account_shared_services_non_prod.account_id,
            description="ID of AccountSharedServicesNonProd Account",
        )

        CfnOutput(
            self,
            "AccountSharedServicesProdId",
            value=self.account_shared_services_prod.account_id,
            description="ID of AccountSharedServicesProd Account",
        )

        CfnOutput(
            self,
            "AccountFinanceDevId",
            value=self.account_finance_dev.account_id,
            description="ID of AccountFinanceDev Account",
        )

        CfnOutput(
            self,
            "AccountFinanceQAId",
            value=self.account_finance_qa.account_id,
            description="ID of AccountFinanceQA Account",
        )

        CfnOutput(
            self,
            "AccountFinanceProdId",
            value=self.account_finance_prod.account_id,
            description="ID of AccountFinanceProd Account",
        )

        CfnOutput(
            self,
            "AccountMarketingDevId",
            value=self.account_marketing_dev.account_id,
            description="ID of AccountMarketingDev Account",
        )

        CfnOutput(
            self,
            "AccountMarketingProdId",
            value=self.account_marketing_prod.account_id,
            description="ID of AccountMarketingProd Account",
        )

        CfnOutput(
            self,
            "AccountPolicyStagingTestsId",
            value=self.account_policy_staging_tests.account_id,
            description="ID of AccountPolicyStagingTests Account",
        )
