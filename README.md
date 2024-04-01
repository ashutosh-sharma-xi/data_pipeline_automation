# This Repository is a Hackathon project organised by Growth School
`Data Pipeline Automation for Stock Price Analysis`

### Data Pipeline Automation
This repository contains code for automating data pipelines using AWS CDK and Lambda functions.

#### Directory Structure

- **.github/workflows**: Contains GitHub Actions workflow for data pipeline.
- **lambda_functions/data_transformer**: Directory for Lambda function code.
  - **data_transformer_lambda.py**: Main Lambda function for data transformation.
  - **Dockerfile**: Dockerfile for packaging Lambda function.
  - **requirements.txt**: Python dependencies for Lambda function.
  - **utils.py**: Utility functions for data transformation.
- **src**: Contains source code for the data pipeline.
- **tests**: Directory for unit tests.
- **README.md**: Detailed documentation for the project.
- **cdk.json, ecr_lifecycle_policy.json, source.bat**: Configuration and setup files.

#### Usage

1. **Lambda Function**: The `data_transformer_lambda.py` file contains the main Lambda function code for transforming data. Dockerfile and requirements.txt are used for packaging the function.
   
2. **CDK Stack**: The `data_pipeline_automation_stack.py` file defines the AWS CDK stack for deploying the data pipeline infrastructure.

3. **GitHub Actions**: Workflow in `.github/workflows/data_pipeline.yml` automates deployment of the data pipeline on GitHub push events.

#### Deployment

To deploy the data pipeline:

1. Add required credentials in Github secrets.
2. Run github workflow it will deploy the data pipeline all in one stack.
3. Monitor the deployment status in the AWS Management Console.

#### AWS CDK Deployment Workflow
This GitHub Actions workflow automates the deployment process of an AWS CDK (Cloud Development Kit) application. It performs the following tasks:

#### Testing

Unit tests for the data pipeline stack are located in the `tests/unit` directory. Run tests using your preferred testing framework.

#### Contributing

Contributions to this project are welcome. Please open an issue or pull request for any suggestions, improvements, or bug fixes.

