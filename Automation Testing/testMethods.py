import time
import jwt
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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

def submitCardDetails(browser,cardNumber, expiryMonth, expiryYear, cvv, cardholderName):

    actions = ActionChains(browser)
    actions.send_keys('command+option+i')
    actions.perform()

    # Enter Card Number
    cardNumber_field = browser.find_element(By.NAME,"cardNumber")
    cardNumber_field.send_keys(cardNumber)
    time.sleep(500/1000) 

    # Enter Expiry Month
    expiryMonth_field = browser.find_element(By.NAME,"expiryMonth")
    expiryMonth_field.send_keys(expiryMonth)
    time.sleep(500/1000)

    # Enter Expiry Year
    expiryYear_field = browser.find_element(By.NAME,"expiryYear")
    expiryYear_field.send_keys(expiryYear)
    time.sleep(500/1000)

    # Enter Cvv Number
    cvvNumber_field = browser.find_element(By.NAME,"cvv")
    cvvNumber_field.send_keys(cvv)
    time.sleep(500/1000)

    # Enter Card Holder Name
    cardHolderName_field = browser.find_element(By.NAME,"customerName")
    cardHolderName_field.send_keys(cardholderName)
    time.sleep(500/1000)

    #Submit
    submitButton = browser.find_element(By.ID,"submitButton")
    submitButton.send_keys(Keys.RETURN)
 
def logMessage(msg):
    print("\n===============================================>\n")
    print("Error Test Case 1 : Make payment error -> %s" % msg)
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

    # convert the encoded JWT to a string
    # jwt_string = encoded_jwt.decode('utf-8')

    # print the JWT string
    # print(jwt_string)
    return encoded_jwt
