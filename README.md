
# gelbeseiten.de Scraper

A scraper API to gelbeseiten.de using [AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html) and [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html). Deployment with [kappa](https://github.com/garnaat/kappa). Done as a code exercise as part of a job application.


## Quickstart


### Deploy AWS Lambda

* Install kappa

        $ pip install kappa

* Configure `<profile>` and `<region>` in kappa.yml

        $ cp kappa.yml.sample kappa.yml
        $ vim kappa.yml

* Deploy to AWS Lambda (assumes awscli is [configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html))

        $ kappa deploy


### Create API Gateway api


##### GET /companies


* Add request parameters "q" & "postcode"

        Method Request > URL Query String Parameters > "q" + "postcode"


* Configure integration to Lambda function "gelbeseiten"

        Integration Request > Lambda Function > "gelbeseiten"


* Configure body mapping

        Integration Request > Body Mapping Templates > Content-Type > application/json

        #set($inputRoot = $input.path('$'))
        {
            "method": "companies",
            "q": "$input.params('q')",
            "postcode": "$input.params('postcode')"
        }


##### GET /companies/{company_id}


* Configure integration to Lambda function "gelbeseiten"

        Integration Request > Lambda Function > gelbeseiten


* Configure body mapping

        Integration Request > Body Mapping Templates > Content-Type > application/json

        #set($inputRoot = $input.path('$'))
        {
            "method": "company",
            "company_id": "$input.params('company_id')"
        }


##### Deploy API

        APIs > gelbeseiten > Resources > Actions > Deploy API


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


## Why AWS Lambda & AWS API Gateway

* With serverless architecure you just pay for what you use
* Serverless architecture scales
* Caching included


## Possible improvements

* **Authentication:** Use a second AWS Lambda function as authentication service
* **Company data:** Crawl data from companies own website.
* **DB:** Persist data in DB instead of caching.
* **Deployment:** Automate API Gateway api creation.
* **Documentation:** Export API Gateway api description in swagger format.
* **Proxy:** Use proxy service to use changing IPs (Crawlera etc.)
* **Tests:** Add automated testing e.g. travis-ci
* **Third party Services:** Use 3rd party api services to extend company info, e.g. solvency/credit history


## Limitations

* **AWS Lambda:** If this service is expanded, AWS Lambda could be a drawback. While it is a perfect usecase for small, independent, modular solutions, it can be complicated and hard to debug for a bigger architecture.
* **Blocking:** A high number of requests might cause blocking by gelbeseiten.de. Varying user agents of popular browsers are used, but the originating IP is not concealed.
* **Pagination:** on gelbeseiten.de search is not yet handled

