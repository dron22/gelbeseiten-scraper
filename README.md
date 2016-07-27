
# gelbeseiten.de scraper


## Quickstart


### Deploy AWS Lambda

* Install kappa

        $ pip install kappa

* Configure <profile> and <region> in kappa.yml

        $ cp kappa.yml.sample kappa.yml
        $ vim kappa.yml

* Deploy to AWS Lambda

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


## API Endpoints


* GET /companies

        $ curl -XGET {{url}}/companies?q=Rocket%20Internet&postcode=10111    
        
        [
            {
                "id": "1056434575",
                "companyName": "Rocket Internet GmbH Internetservice"
            }
        ]

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

