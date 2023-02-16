import requests
import time
import json
import unittest
import testMethods as external
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class TestPaymentCheckout(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
 
    # Only cards givn in the request
    def test_case_1(self):
        test_case = 1
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
            preAuth=None,
            description = "Amazon 250 voucher booking",
            frontendReturnUrl = "https://thriwe.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            cards = [
                {
                    "first" :"424242",
                    "last" :"4242"
                }
            ],
            binNumbers=None,
            pgCode=None
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)
            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
            
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))

    # only bins given
    def test_case_2(self):
        test_case = 2
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
            preAuth=None,
            frontendReturnUrl = "https://thriwe.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            binNumbers =["424242"],
            cards=None,
            pgCode=None
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)

            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        external.handle_page_redirection(self,test_case)
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))
    
    # only PGcode given
    def test_case_3(self):
        test_case = 3
        # Payment request api call
        url = "http://localhost:8088/v1/payments"
        # payload={}

        tokenPayload = external.JwtPayload(
            issuer = "FAB_BENEFITS_V1",
            amount = 1200,
            currency = "INR",
            email = "shubham.sisodia@thriwe.com",
            contactNumber = "9012100577",
            preAuth=None,
            referenceId = "45dd",
            description = "Amazon 250 voucher booking",
            frontendReturnUrl = "https://thriwe.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            pgCode = "PG01",
            binNumbers=None,
            cards=None
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)

            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))
   
    #pre-auth true
    def test_case_4(self):
        test_case = 4
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
            cards=None,
            binNumbers=None,
            pgCode=None
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)

            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))
    
    # Cards and bin both in request
    def test_case_5(self):

        test_case = 5
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
            binNumbers =["526731"],
            cards = [
                {
                    "first" :"424242",
                    "last" :"4242"
                }
            ],
            pgCode=None
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)

            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))

    # Pre-auth False
    def test_case_6(self):
        test_case = 6
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
            preAuth=False,
            frontendReturnUrl = "https://thriwe.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            cards=None,
            binNumbers=None,
            pgCode=None
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)
            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
            
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))

    # wrong project code
    def test_case_7(self):
        
        test_case = 7
        # Payment request api call
        url = "http://localhost:8088/v1/payments"
        # payload={}

        tokenPayload = external.JwtPayload(
            issuer = "FAB_BENEFITS_V2",
            amount = 1200,
            currency = "INR",
            email = "shubham.sisodia@thriwe.com",
            contactNumber = "9012100577",
            referenceId = "45dd",
            description = "Amazon 250 voucher booking",
            preAuth=None,
            frontendReturnUrl = "https://thriwe1.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            binNumbers =["526731"],
            cards = [
                {
                    "first" :"424242",
                    "last" :"4242"
                }
            ],
            pgCode=None
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)
            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
            
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))

    # Wrong cardnumber in request token
    def test_case_8(self):
        #wrong frontend URL
        test_case = 8
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
            preAuth=None,
            pgCode=None,
            frontendReturnUrl = "https://thriwe1.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            binNumbers =["526731"],
            cards = [
                {
                    "first" :"424241",
                    "last" :"4242"
                }
            ],
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)
            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
            
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))
    
    # Without Contact number
    def test_case_9(self):
        test_case = 9
        # Payment request api call
        url = "http://localhost:8088/v1/payments"
        # payload={}

        tokenPayload = external.JwtPayload(
            issuer = "FAB_BENEFITS_V1",
            amount = 1200,
            currency = "INR",
            email = "shubham.sisodia@thriwe.com",
            contactNumber = None,
            referenceId = "45dd",
            description = "Amazon 250 voucher booking",
            pgCode=None,
            preAuth=None,
            frontendReturnUrl = "https://thriwe1.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            binNumbers =["526731"],
            cards = [
                {
                    "first" :"424242",
                    "last" :"4242"
                }
            ],
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)
            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
            
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))
    
    # Without Email
    def test_case_10(self):
        test_case = 10
        # Payment request api call
        url = "http://localhost:8088/v1/payments"
        # payload={}

        tokenPayload = external.JwtPayload(
            issuer = "FAB_BENEFITS_V1",
            amount = 1200,
            currency = "INR",
            email = None,
            contactNumber = 9958229588,
            referenceId = "45dd",
            description = "Amazon 250 voucher booking",
            pgCode=None,
            preAuth=None,
            frontendReturnUrl = "https://thriwe1.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            binNumbers =["526731"],
            cards = [
                {
                    "first" :"424242",
                    "last" :"4242"
                }
            ],
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)
            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
            
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))
    
    # Wrong currency
    def test_case_11(self):
        test_case = 10
        # Payment request api call
        url = "http://localhost:8088/v1/payments"
        # payload={}

        tokenPayload = external.JwtPayload(
            issuer = "FAB_BENEFITS_V1",
            amount = 1200,
            currency = "SDR",
            email = "shubham.sisodia@thriwe.com",
            contactNumber = "9958229588",
            referenceId = "45dd",
            description = "Amazon 250 voucher booking",
            pgCode=None,
            preAuth=None,
            frontendReturnUrl = "https://thriwe1.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            binNumbers =["526731"],
            cards = [
                {
                    "first" :"424242",
                    "last" :"4242"
                }
            ],
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"4242424242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)
            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
            
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))
    
    # Wrong card input in checkout
    
    def test_case_12(self):
        test_case = 11
        # Payment request api call
        url = "http://localhost:8088/v1/payments"
        # payload={}

        tokenPayload = external.JwtPayload(
            issuer = "FAB_BENEFITS_V1",
            amount = 1200,
            currency = "INR",
            email = "shubham.sisodia@thriwe.com",
            contactNumber = "9958229588",
            referenceId = "45dd",
            preAuth=None,
            description = "Amazon 250 voucher booking",
            frontendReturnUrl = "https://thriwe1.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            binNumbers =["526731"],
            cards = [
                {
                    "first" :"424242",
                    "last" :"4242"
                }
            ],
            pgCode="PG02"
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"424224212424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)
            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
            
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))
    
    # No Card/PGcode/Binnumbers
    def test_case_13(self):
        test_case = 12
        # Payment request api call
        url = "http://localhost:8088/v1/payments"
        # payload={}

        tokenPayload = external.JwtPayload(
            issuer = "FAB_BENEFITS_V1",
            amount = 1200,
            currency = "INR",
            email = "shubham.sisodia@thriwe.com",
            contactNumber = "9958229588",
            referenceId = "45dd",
            preAuth=None,
            description = "Amazon 250 voucher booking",
            frontendReturnUrl = "https://thriwe1.com/index.html",
            backendReturnUrl = "https://eogtmtsbqyib8xf.m.pipedream.net",
            binNumbers =None,
            cards = None,
            pgCode=None
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
            # time.sleep(1) #Slow down the process

            #Submit payment details
            external.submitCardDetails(self.browser,"424224242424242","08","2026","345","Shubham Sisodia")
            
            # Delay the screen
            time.sleep(2)
            #Check if there is any error in make payment call
            try:
                err_msg_field = self.browser.find_element(By.CLASS_NAME,"notify-message")
            except:
                external.handle_page_redirection(self,test_case)   
            else:
                if err_msg_field.text != "":
                    external.logMessage(test_case,"Error",err_msg_field.text)
                else:
                    # Wait for 5 seconds until the URL changes
                    wait = WebDriverWait(self.browser, 5)
                    try:
                        element = wait.until(EC.url_changes(redirectUrl))
                    except TimeoutException:
                        external.logMessage(test_case,"Error","The URL did not redirected to payment status page.")
                    else:
                        # print("Here 1")
                        external.handle_page_redirection(self,test_case)
            
        else:
            external.logMessage(test_case,"Error"," Make payment error : " + json.dumps(data))
    
    def tearDown(self):
        self.browser.close()

if __name__ == '__main__':
    # Run all test cases at once
    unittest.main()

    # Run a particular test case separately
    # test_suite = unittest.TestSuite()
    # test_suite.addTest(TestPaymentCheckout('test_case_2'))
    # unittest.TextTestRunner().run(test_suite)



