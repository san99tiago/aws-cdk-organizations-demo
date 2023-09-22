# :bank: AWS-CDK-ORGANIZATIONS-DEMO :bank:

![Badge Workflow](https://github.com/san99tiago/aws-cdk-organizations-demo/actions/workflows/deploy.yml/badge.svg)

DEMO for the best practices of AWS Organizations with Infrastructure as Code on CDK-Python.

## TODO:

Add a detailed README with diagrams, explanations and examples of usage.

## CI/CD and Deployment 🚀

The deployment process is intended to run with GitHub Actions Workflows.

- On `feature/****` branches commits, the CDK project gets **synthesized** and it shows the **state diff** between the current AWS resources and the expected ones.

- When merged to `main` branch, it will get deployed to the AWS Account automatically.

To understand the AWS Credentials usage, please refer to the [`prerequisites/README.md`](.github/prerequisites/README.md).

## Special thanks :gift:

- Thanks to all contributors of the great OpenSource projects that I am using. <br>

## Author :musical_keyboard:

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
