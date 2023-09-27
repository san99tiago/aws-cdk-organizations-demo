[![GitHub LICENSE](https://img.shields.io/github/license/san99tiago/aws-cdk-organizations-demo?style=plastic)](https://github.com/san99tiago/aws-cdk-organizations-demo/blob/main/LICENSE)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/san99tiago/aws-cdk-organizations-demo/deploy.yml?branch=main&label=deploy&style=plastic)](https://github.com/san99tiago/aws-cdk-organizations-demo/actions/workflows/deploy.yml)
[![GitHub Release (Latest SemVer)](https://img.shields.io/github/v/release/san99tiago/aws-cdk-organizations-demo?sort=semver&style=plastic)](https://github.com/san99tiago/aws-cdk-organizations-demo/releases)

# [<img src="assets/aws_dynamic.gif" width=10% align="center" alt="cool aws image"  title="aws-cdk-organizations-demo">](https://github.com/san99tiago/aws-cdk-organizations-demo) AWS-CDK-ORGANIZATIONS-DEMO [<img src="assets/aws_dynamic.gif" width=10% align="center" alt="cool aws image"  title="aws-cdk-organizations-demo">](https://github.com/san99tiago/aws-cdk-organizations-demo)

Advanced DEMO of [AWS Organizations](https://aws.amazon.com/organizations/) for sharing the best practices of managing multiple production-grade AWS Accounts with Infrastructure as Code on [CDK-Python](https://docs.aws.amazon.com/cdk/v2/guide/home.html).

## Architecture 🏦

This diagram illustrates the generated AWS Organizations structure with multiple OUs and Account.

<img src="assets/aws-cdk-organizations-demo.png" width=90%> <br>

```bash
# Hierarchy of the OUs and Accounts
OURoot/
├── 🏠ManagementAccount(🚩)
├── 📝OUInfrastructure/
│   ├── 📝OUInfrastructureNonProd/
│   │   └── 🏠AccountSharedServicesNonProd
│   └── 📝OUInfrastructureProd/
│       └── 🏠AccountSharedServicesProd
├── 📝OUWorkloads/
│   ├── 📝OUFinance/
│   │   ├── 📝OUFinanceNonProd/
│   │   │   ├── 🏠AccountFinanceDev
│   │   │   └── 🏠AccountFinanceQA
│   │   └── 📝OUFinanceProd/
│   │       └── 🏠AccountFinanceProd
│   └── 📝OUMarketing/
│       ├── 📝OUMarketingNonProd/
│       │   ├── 🏠AccountMarketingDev
│       └── 📝OUMarketingProd/
│           └── 🏠AccountMarketingProd
└── 📝OUPolicyStagingTests/
    └── 🏠AccountPolicyStagingTests
```

## CI/CD and Deployment 🚀

The deployment process is intended to run with GitHub Actions Workflows and implementing the Cloud Development Tool (CDK) tool for managing the IaC and State.

<img src="assets/aws-cdk-organizations-demo-cicd.png" width=90%> <br>

- On `feature/****` branches commits, the CDK project gets **synthesized** and it shows the **state diff** between the current AWS resources and the expected ones.

- When merged to `main` branch, it will get deployed to the AWS Account automatically.

To understand the AWS Credentials usage for GitHub Actions auth, please refer to the [`prerequisites/README.md`](.github/prerequisites/README.md).

## Manual Steps (Only Once) 👋

As of now, IAM Identity Center (successor to AWS Single Sign-On) has to be "manually" enabled once, so that the SSO Configurations and Permission Sets can be created via IaC. In order to do so, we have to go to the SSO Console and click on `Enable IAM Identity Center`:

<img src="assets/aws-cdk-organizations-demo-sso-enable.png" width=90%> <br>

Then, we have to configure our SSO URL as follows:

<img src="assets/aws-cdk-organizations-demo-sso-url.png" width=50%> <br>

## Special thanks 🎁

- Huge shout-out to [pepperize/cdk-organizations](https://github.com/pepperize/cdk-organizations) for the Custom AWS-CDK Constructs that are provided for managing this project.

## Author 🎹

### Santiago Garcia Arango

<table border="1">
    <tr>
        <td>
            <p align="center">Curious DevOps Engineer passionate about advanced cloud-based solutions and deployments in AWS. I am convinced that today's greatest challenges must be solved by people that love what they do.</p>
        </td>
        <td>
            <p align="center"><img src="assets/SantiagoGarciaArangoCDK.png" width=80%></p>
        </td>
    </tr>
</table>

## LICENSE

Copyright 2023 Santiago Garcia Arango.
