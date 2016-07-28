
# gelbeseiten.de Scraper

![build status](https://travis-ci.org/dron22/gelbeseiten-scraper.svg?branch=master)

A scraper API to gelbeseiten.de using [AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html) and [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html). Lambda deployment with [kappa](https://github.com/garnaat/kappa), API creation with [boto3](https://boto3.readthedocs.io/). Done as a code exercise as part of a job application.


## Quickstart


### Prerequisites


* Install dependencies

        $ pip install -r requirements


* Configure aws credentials

        $ vim ~/.aws/credentials:

        [default]
        aws_access_key_id = YOUR_ACCESS_KEY
        aws_secret_access_key = YOUR_SECRET_KEY


* Configure default region (optional)

        $ vim ~/.aws/config:

        [default]
        region=us-east-1


### Deploy AWS Lambda with kappa

* Configure `<profile>` and `<region>` in kappa.yml

        $ cp kappa.yml.sample kappa.yml
        $ vim kappa.yml


* Deploy to AWS Lambda

        $ kappa deploy


### Create API on AWS Gateway

    $ python ./create_api.py -r 'eu-central-1' [-a <API_NAME>]


### Create API Gateway api


## API Endpoints


* GET /companies

        $ curl -XGET {{url}}/companies?q=Rocket%20Internet&postcode=10111    
        
        {
            "companies": [
                {
                    "id": "1056434575",
                    "companyName": "Rocket Internet GmbH Internetservice"
                }
            ]
        }

* GET /companies/{company_id}

        $ curl -XGET {{url}}/companies/1056434575

        {
            "website": "http://www.rocket-internet.de",
            "locality": "Berlin-Prenzlauer Berg",
            "companyName": "Rocket Internet GmbH Internetservice",
            "phone": "(030) 55 95 54",
            "streetAddress": "Saarbrücker Str. 20/21",
            "postcode": "10405"
        }


## Caching

Provided by [AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html).


## Run tests

    $ kappa test


## Why AWS Lambda & AWS API Gateway?

* With serverless architecure you just pay for what you use
* Serverless architecture scales
* Caching included


## Possible improvements

* **Authentication:** Use a second AWS Lambda function as authentication service
* **Company data:** Crawl data from companies own website
* **DB:** Persist data in DB instead of caching
* **Documentation:** Export API Gateway api description in swagger format
* **Proxy:** Use proxy service to spoof originating IP (Crawlera etc.)
* **Third party Services:** Use 3rd party api services to extend company info, e.g. solvency/credit history


## Limitations

* **AWS Lambda:** If this service is expanded, AWS Lambda could be a drawback. While it is a perfect usecase for small, independent, modular solutions, it can be complicated and hard to debug for a bigger architecture.
* **Blocking:** A high number of requests might cause blocking by gelbeseiten.de. Varying user agents of popular browsers are used, but the originating IP is not concealed.
* **Pagination:** On gelbeseiten.de search is not yet handled
