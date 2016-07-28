

import argparse
import boto3
import uuid


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--region',
                    metavar='{REGION}', required=True)
parser.add_argument('-a', '--api_name',
                    metavar='{API_NAME}',  default='gelbeseiten')
parser.add_argument('-l', '--lambda_name',
                    metavar='{LAMBDA_NAME}',  default='gelbeseiten')
parser.add_argument('-c', '--cache_disable', action='store_true')

args = parser.parse_args()

AWS_REGION = args.region
LAMBDA_NAME = args.lambda_name
API_NAME = args.api_name
CACHE_DISABLE = args.cache_disable
API_DESC = 'gelbeseiten.de scraper API'


###############################################################################
# Init
###############################################################################

aws_gateway = boto3.client('apigateway', AWS_REGION)
aws_lambda = boto3.client('lambda', AWS_REGION)

aws_account = boto3.client('sts').get_caller_identity().get('Account')

lambda_version = aws_lambda.meta.service_model.api_version
lambda_uri_data = {
    'aws-region': AWS_REGION,
    'aws-acct-id': aws_account,
    'lambda-function-name': LAMBDA_NAME,
    'api-version': lambda_version,
}
lambda_uri = 'arn:aws:apigateway:{aws-region}:lambda:path/{api-version}/functions/arn:aws:lambda:{aws-region}:{aws-acct-id}:function:{lambda-function-name}/invocations'.format(**lambda_uri_data)


###############################################################################
# Create API
###############################################################################

api = aws_gateway.create_rest_api(
    name=API_NAME,
    description=API_DESC
)
home_resource = aws_gateway.get_resources(restApiId=api['id'])['items'][0]


###############################################################################
# Create endpoint: GET /companies
###############################################################################

companies_resource = aws_gateway.create_resource(
    restApiId=api['id'],
    parentId=home_resource['id'],
    pathPart='companies'
)


aws_gateway.put_method(
    restApiId=api['id'],
    resourceId=companies_resource['id'],
    httpMethod='GET',
    authorizationType='NONE',
    requestParameters={
        'method.request.querystring.q': True,
        'method.request.querystring.postcode': True,
    }
)


aws_gateway.put_method_response(
    restApiId=api['id'],
    resourceId=companies_resource['id'],
    httpMethod='GET',
    statusCode='200'
)


tpl = """
#set($inputRoot = $input.path('$'))
{
    "method": "companies",
    "q": "$input.params('q')",
    "postcode": "$input.params('postcode')"
}
"""

aws_gateway.put_integration(
    restApiId=api['id'],
    resourceId=companies_resource['id'],
    httpMethod='GET',
    type='AWS',
    integrationHttpMethod='POST',
    uri=lambda_uri,
    requestParameters={
        'integration.request.querystring.q': 'method.request.querystring.q',
        'integration.request.querystring.postcode': 'method.request.querystring.postcode',
    },
    requestTemplates={
        'application/json': tpl
    },
    cacheKeyParameters=[
        'method.request.querystring.q',
        'method.request.querystring.postcode']
)

aws_gateway.put_integration_response(
    restApiId=api['id'],
    resourceId=companies_resource['id'],
    httpMethod='GET',
    statusCode='200',
    selectionPattern='.*'
)

uri_data = {
    'aws-region': AWS_REGION,
    'aws-acct-id': aws_account,
    'lambda-function-name': LAMBDA_NAME,
    'api-version': lambda_version,
    'aws-api-id': api['id'],
}
source_arn = "arn:aws:execute-api:{aws-region}:{aws-acct-id}:{aws-api-id}/*/GET/companies".format(**uri_data)


aws_lambda.add_permission(
    FunctionName=LAMBDA_NAME,
    StatementId=uuid.uuid4().hex,
    Action="lambda:InvokeFunction",
    Principal="apigateway.amazonaws.com",
    SourceArn=source_arn
)


###############################################################################
# Create endpoint: GET /companies/{company_id}
###############################################################################

company_resource = aws_gateway.create_resource(
    restApiId=api['id'],
    parentId=companies_resource['id'],
    pathPart='{company_id}'
)

aws_gateway.put_method(
    restApiId=api['id'],
    resourceId=company_resource['id'],
    httpMethod='GET',
    authorizationType='NONE'
)


aws_gateway.put_method_response(
    restApiId=api['id'],
    resourceId=company_resource['id'],
    httpMethod='GET',
    statusCode='200'
)


tpl = """
#set($inputRoot = $input.path('$'))
{
    "method": "company",
    "company_id": "$input.params('company_id')"
}
"""

aws_gateway.put_integration(
    restApiId=api['id'],
    resourceId=company_resource['id'],
    httpMethod='GET',
    type='AWS',
    integrationHttpMethod='POST',
    uri=lambda_uri,
    requestTemplates={
        'application/json': tpl
    }
)

aws_gateway.put_integration_response(
    restApiId=api['id'],
    resourceId=company_resource['id'],
    httpMethod='GET',
    statusCode='200',
    selectionPattern='.*'
)

uri_data = {
    'aws-region': AWS_REGION,
    'aws-acct-id': aws_account,
    'lambda-function-name': LAMBDA_NAME,
    'api-version': lambda_version,
    'aws-api-id': api['id'],
}
source_arn = "arn:aws:execute-api:{aws-region}:{aws-acct-id}:{aws-api-id}/*/GET/companies/*".format(**uri_data)


aws_lambda.add_permission(
    FunctionName=LAMBDA_NAME,
    StatementId=uuid.uuid4().hex,
    Action="lambda:InvokeFunction",
    Principal="apigateway.amazonaws.com",
    SourceArn=source_arn
)


###############################################################################
# Deploy
###############################################################################

if CACHE_DISABLE:

    aws_gateway.create_deployment(
        restApiId=api['id'],
        stageName='dev'
    )

else:

    aws_gateway.create_deployment(
        restApiId=api['id'],
        stageName='dev',
        cacheClusterEnabled=True,
        cacheClusterSize='0.5'
    )

    aws_gateway.update_stage(
        restApiId=api['id'],
        stageName='dev',
        patchOperations=[
            {
                'op': 'replace',
                'path': '/*/*/caching/enabled',
                'value': 'True'
            },
            {
                'op': 'replace',
                'path': '/*/*/caching/ttlInSeconds',
                'value': '3600'
            },
            {
                'op': 'replace',
                'path': '/*/*/caching/requireAuthorizationForCacheControl',
                'value': 'False'
            }
        ]
    )
    print('Cache creation in progress (This will take some time)')

print('API Creation successful.')
url = 'https://{0}.execute-api.eu-central-1.amazonaws.com/dev/companies'
url = url.format(api['id'])
print('Example calls:\n')
print('  $ curl -XGET "{0}?q=pizza&postcode=10111"'.format(url))
print('  $ curl -XGET "{0}/1056800802"\n'.format(url))
