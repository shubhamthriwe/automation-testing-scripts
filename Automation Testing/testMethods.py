import time
import jwt
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class JwtPayload:
    def __init__(self, issuer,amount,currency,email,contactNumber,referenceId,description,preAuth,frontendReturnUrl,backendReturnUrl,cards,binNumbers,pgCode):
        self.issuer = issuer
        self.amount = amount
        self.currency = currency
        self.email = email
        self.contactNumber = contactNumber
        self.referenceId = referenceId
        self.description = description
        self.preAuth = preAuth
        self.frontendReturnUrl = frontendReturnUrl
        self.backendReturnUrl = backendReturnUrl
        self.cards = cards
        self.binNumbers = binNumbers
        self.pgCode = pgCode

class Jwtcards:
    def __init__(self, issuer,userId,cards,name,number,binId,cardId):
        self.issuer = issuer
        self.userId = userId
        self.cards = cards
        self.name = name
        self.number = number
        self.binId = binId
        self.cardId = cardId


def submitCardDetails(browser,cardNumber, expiryMonth, expiryYear, cvv, cardholderName):

    actions = ActionChains(browser)
    actions.send_keys('command+option+i')
    actions.perform()

    # Enter Card Number
    cardNumber_field = browser.find_element(By.NAME,"cardNumber")
    cardNumber_field.send_keys(cardNumber)
    # time.sleep(500/1000) 

    # Enter Expiry Month
    expiryMonth_field = browser.find_element(By.NAME,"expiryMonth")
    expiryMonth_field.send_keys(expiryMonth)
    # time.sleep(500/1000)

    # Enter Expiry Year
    expiryYear_field = browser.find_element(By.NAME,"expiryYear")
    expiryYear_field.send_keys(expiryYear)
    # time.sleep(500/1000)

    # Enter Cvv Number
    cvvNumber_field = browser.find_element(By.NAME,"cvv")
    cvvNumber_field.send_keys(cvv)
    #time.sleep(500/1000)

    # Enter Card Holder Name
    cardHolderName_field = browser.find_element(By.NAME,"customerName")
    cardHolderName_field.send_keys(cardholderName)
    #time.sleep(500/1000)

    #Submit
    submitButton = browser.find_element(By.ID,"submitButton")
    submitButton.send_keys(Keys.RETURN)
 
def logMessage(testCase,type,msg):
    print("\n===============================================>\n")
    print("Test Case %d : %s -> %s" % (testCase,type,msg))
    print("\n===============================================>\n")

def generateTokenAndSetHeader(JwtPayload):
    # the payload containing the claims
    payload = {
        "iss": JwtPayload.issuer,
        "amount": JwtPayload.amount,
        "currency": JwtPayload.currency,
        "email": JwtPayload.email,
        "contactNumber": JwtPayload.contactNumber,
        "referenceId": JwtPayload.referenceId,
        "description": JwtPayload.description,
        "preAuth": JwtPayload.preAuth,
        "frontendReturnUrl": JwtPayload.frontendReturnUrl,
        "backendReturnUrl": JwtPayload.backendReturnUrl,
        "cards": JwtPayload.cards,
        "binNumbers": JwtPayload.binNumbers,
        "pgCode": JwtPayload.pgCode
    }


    # the secret key used to sign the JWT
    secret_key = "jwt_2JdMPbiyaVj77x2lWGao5GFOxFv"

    # encode the payload with the secret key
    encoded_jwt = jwt.encode(payload, secret_key, algorithm='HS256')
    return encoded_jwt

def generateTokenAndSetHeaderforbinsandcards(Jwtcards):
    # the payload containing the claims
    payload = {
        "iss": Jwtcards.issuer,
        "userId": Jwtcards.userId,
        "card": Jwtcards.cards,
        "name": Jwtcards.name,
        "number": Jwtcards.number,
        "binId": Jwtcards.binId,
        "cardId": Jwtcards.cardId
    }

    # the secret key used to sign the JWT
    secret_key = "jwt_2JdMPbiyaVj77x2lWGao5GFOxFv"

    # encode the payload with the secret key
    encoded_jwt = jwt.encode(payload, secret_key, algorithm='HS256')
    return encoded_jwt



def check_browser_redirection(currentUrl,self,test_case):
    self.browser.maximize_window()
    wait = WebDriverWait(self.browser, 5)
    try:
        # print("Here current url is",self.browser.current_url)
        element = wait.until(EC.url_changes(currentUrl))
        
    except TimeoutException:
        logMessage(test_case,"Error","The URL did not redirected to payment status page.")
    else:
        #test for frontend url
        wait = WebDriverWait(self.browser, 5)
        try:
            element = wait.until(EC.url_changes(self.browser.current_url))
        except TimeoutException:
            logMessage(test_case,"Error","Page did not redirected to frontend url page."+" Payment Status : " + self.browser.title)
        else:
            logMessage(test_case,"Success","Successfully redirected to frontend url: " + self.browser.current_url)

def handle_page_redirection(self,test_case):
    # print("current_url: " + self.browser.current_url)
    if self.browser.current_url.startswith("https://hooks.stripe.com/"):
        time.sleep(4)
        #This is Stripe 3-D Secure Payment
        self.browser.switch_to.default_content()
        self.browser.switch_to.frame(0)

        newFrame = self.browser.find_element(By.ID,"challengeFrame")
        self.browser.switch_to.frame(newFrame)
        submitButton = self.browser.find_element(By.ID,"test-source-authorize-3ds")
        currentUrl = self.browser.current_url
        submitButton.send_keys(Keys.RETURN)
        check_browser_redirection(currentUrl,self,test_case)
                        
    elif self.browser.current_url.startswith("https://api.razorpay.com/v1/gateway"):
        #This is Razorpay Domestic Payment
        submitButton = self.browser.find_element(By.CLASS_NAME,"success")
        currentUrl = self.browser.current_url
        submitButton.send_keys(Keys.RETURN)
        check_browser_redirection(currentUrl,self,test_case)
        
    elif self.browser.current_url.startswith("https://api.razorpay.com/v1/payments"):
        #This is Razorpay International Payment
        self.browser.set_window_size(500, 1000)

        submitButton = self.browser.find_element(By.ID,"submit-action")
        currentUrl = self.browser.current_url
        submitButton.send_keys(Keys.RETURN)

        wait = WebDriverWait(self.browser, 5)
        try:
            element = wait.until(EC.url_changes(currentUrl))
        except TimeoutException:
            logMessage(test_case,"Error","The URL did not redirected to razorpay success popup page.")
        else:
            submitButton = self.browser.find_element(By.CLASS_NAME,"success")
            submitButton.send_keys(Keys.RETURN)
            check_browser_redirection(currentUrl,self,test_case)
        

    else:
        #This is a normal Payment
        #test for frontend url
        wait = WebDriverWait(self.browser, 5)
        try:
            element = wait.until(EC.url_changes(self.browser.current_url))
        except TimeoutException:
            logMessage(test_case,"Error","Page did not redirected to frontend url page."+" Payment Status : " + self.browser.title)
        else:
            logMessage(test_case,"Success","Successfully redirected to frontend url: " + self.browser.current_url)