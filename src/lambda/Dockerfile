# Lambda base image for Docker from AWS
FROM public.ecr.aws/lambda/python:3.11

# Copying code
COPY ./ ${LAMBDA_TASK_ROOT} 

# Installing requirements
RUN python3 -m pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

CMD ["data_transformer_lambda.lambda_handler"]