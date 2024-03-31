# This Repository is a Hackathon project organised by Growth School
`This is a Data Pipeline Automation`






# AWS CDK Deployment Workflow
This GitHub Actions workflow automates the deployment process of an AWS CDK (Cloud Development Kit) application. It performs the following tasks:

`Checkout:`

Uses the actions/checkout@v2 action to fetch the source code repository.
Configure AWS Credentials:

Configures AWS credentials using the aws-actions/configure-aws-credentials@v1 action.
Requires the AWS access key ID and secret access key stored as GitHub secrets.
Sets the AWS region to us-east-1.
Push Docker Image for Lambda:

Prepares AWS CLI and Docker environment.
Creates or describes an ECR repository.
Sets up a lifecycle policy for the repository.
Builds a Docker image for a Lambda function.
Tags and pushes the Docker image to the ECR repository.
Install npm:

Updates package lists and installs Node.js and npm.
Install AWS CDK:

Installs the AWS CDK globally using npm.
Install Requirements:

Installs Python dependencies specified in requirements.txt.
Synthesize CDK Application:

Generates AWS CloudFormation templates from the CDK application.
Bootstrap CDK:

Prepares the environment for deploying the CDK stack.
Deploy Application:

Deploys the CDK application.
Disables the requirement for manual approval (--require-approval never).
Note: Ensure that all required AWS resources, such as IAM roles and ECR repositories, are properly configured before running this workflow.