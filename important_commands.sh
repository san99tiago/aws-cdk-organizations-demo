#!/bin/bash

################################################################################
# PART 1: Configure NodeJs, Python and CDK libraries
################################################################################

# Install NodeJs and Python
# -->  https://nodejs.org/en/download/
# -->  https://www.python.org/downloads/

# Verify that NodeJs/npm is installed correctly
node --version
npm --version

# Verify that Python/pip is installed correctly
python --version || python3 --version
pip --version || pip3 --version

# Install AWS-CDK (on NodeJs)
sudo npm install -g aws-cdk

# Verify correct install of AWS-CDK
npm list --global | grep aws-cdk


################################################################################
# PART 2: Initial Project Setup (Only run these at the beginning)
################################################################################

# Configure AWS credentials (follow steps)
aws configure
# --> Alternative 1: Environment variables added to terminal session
# --> Alternative 2: AWS Cloud9 with the right permissions
# --> Alternative 3: AWS SSO login

# Bootstrap CDK (provision initial resources to work with CDK.. S3, roles, etc)
#! Change "ACCOUNT-NUMBER" and "REGION" to your needed values
cdk bootstrap aws://ACCOUNT-NUMBER/REGION

# Install poetry (for managing Python dependencies)
pip install poetry

# Install poetry dependencies for the virtual environment
poetry install


################################################################################
# PART 3: Main CDK and Python commands (most used)
################################################################################

# Activate Python virtual environment with Poetry tool
poetry shell

# Run unit tests
poe test-unit

# Deploy commands (NOTE: prefered method is with the CI/CD Pipeline)
export DEPLOYMENT_ENVIRONMENT=dev
cdk synth
cdk deploy  # I recommend to use GitHub Actions Pipeline instead
