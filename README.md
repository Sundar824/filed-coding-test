# Filed Coding Test

I have done this test with three different type of payment gateways

1. Cheap Payment Gateway:
   
         Stripe payment gateway
   
2. Expensive Payment Gateway:
        
        cashfree payment gateway
   
3. Premium Payment Gateway:
        
        Razor payment gateway
   
I have added my secret keys for this test.
All process is only to going to create sessions(orders) only.
All the APIs are using payment gateway "API integration". Not the SDK.

Parameters for sample API calls

    {
       "CreditCardNumber": "6069980100503646",
       "CardHolder": "Mano",
       "ExpirationDate": "10/2021",
       "SecurityCode":"324",
       "Amount": "50"
    }

pleas pull the code and run the PaymentProcess.py file 
with below command.

    python PaymentProcess.py

The link https://localhost:500 will redirect you to sample page for 
payment process.

Thanks!!..
