import requests
import time
import unittest
import testMethods as external
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestPaymentCheckout(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
 
    def test_successful_payment(self):
        # Payment request api call
        url = "http://localhost:8088/v1/payments"
        # payload={}

        tokenPayload = external.JwtPayload(
            issuer = "FAB_BENEFITS_V1",
            amount = 1200,
            currency = "INR",
            email = "shubham.sisodia@thriwe.com",
            contactNumber = "9012100577",
            referenceId = "45dd",
            description = "Amazon 250 voucher booking",
            preAuth = True,
            frontendReturnUrl = "https://thriwe.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            cards = [
                {
                    "first" :"424242",
                    "last" :"4242"
                }
            ],
            binNumbers = [
                "424242","434343"
            ],
            pgCode = "PG01"
            )
        
        headers = {
            'Authorization': 'Bearer ' + external.generateTokenAndSetHeader(tokenPayload)
        }

        response = requests.request("POST", url, headers=headers, data={})
        data = response.json()
        if response.status_code == 200:
            nextAction = data.get('nextAction')
            redirectUrl = nextAction.get('redirectUrl')

            # Navigate to the Checkout payment page
            self.browser.get(redirectUrl)
            time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)

            #Check if there is any error in make payment call
            err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            if err_msg_field.text != "":
                external.logMessage(err_msg_field.text)
            else:
                #success case
                time.sleep(3)
                # Get the title of the webpage
                print("Payment Status page : " + self.browser.title)
                time.sleep(2)
                print("Redirected to frontend url : " + self.browser.title)



        else:
            external.logMessage(data)
 
    def tearDown(self):
        self.browser.close()

if __name__ == '__main__':
    unittest.main()

