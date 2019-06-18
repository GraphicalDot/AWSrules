FORMAT: 1A
HOST: https://url/Production/

# Datapod Remote registration Apis

The documentation of the APIS used for users remote registration.

## Users [/users/signup]
### Signup [POST]
API to register new users.</br>
• 400 is returned if the user does not have access to the requested account</br>
• 401 If the username already exists</br>

+ Request 200 (application/json)
        {
          "email": "houzier@gmail.com",
          "password": "Golfurl##45",
          "name": "Saurav Verma",
          "username": "graphical"
        }
        
+ Response 200 

        {
        "error": false,
        "success": true,
        "msg": "Please confirm your signup, check Email for validation code"
          }

+ Response 400 (application/json)
        {
        "msg": "An error occurred (UserLambdaValidationException) when calling the SignUp operation: PreSignUp failed with error This email already exists.",
        "error": true,
        "success": false
        }
        
+ Response 401 (application/json)

        {
        "msg": "An error occurred (UsernameExistsException) when calling the SignUp operation: User already exists",
        "error": true,
        "success": false
        }
    
+ Response 
    
    + Body 
        {
            "msg": "An error occurred (InvalidPasswordException) when calling the SignUp operation: Password did not conform with policy: Password must have symbol characters",
            "error": true,
            "success": false
        }

## User Confirm Signup [users/confirm-signup]
### Confirm Signup [POST]
API to register new users.</br>
• 400 is returned if the user does not have access to the requested account</br>
• 401 If the username already exists</br>

+ Request 200 (application/json)
         {
              "username": "graphical",
              "code": "007603"
        }
      
        
+ Response 200 
        
    + Body 
        {
          "error": true,
          "success": false,
          "message": "The user has been confirmed, Please sign in",
          "data": {
            "username": "graphical",
            "code": "511193",
            "mnemonic": "car summer woman oyster west special spray verify upgrade eyebrow clutch science",
            "public": "5038cd30fa91334181999a6fce408884bba9219cfbe917f41237dbd954cb7047",
            "private": "03622df83771d1a1afa53dfc54fa091d1aa08cb0c0c7644278badce87886abec6d",
            "name": "Saurav Verma",
            "email": "houzier@gmail.com"
          }
        }


+ Response 400 (application/json)
       
        {
            "error": true,
            "success": false,
            "message": "User is already confirmed",
            "data": null
        }
        
+ Response 401 (application/json)

        {
            "error": true,
            "success": false,
            "message": "Invalid Verification code",
            "data": null
        }


+ Response 401 (appliction/json)

       {
            "error": true,
            "success": false,
            "message": "Username doesnt exists",
            "data": null
        }


## [users/login]
### Login [POST]

The api to login for the users <br/> 
<b>Case 1</b>:  When the user hasnt enabled MFA, the user will directly get his id_token, access_token and refresh_token <br/>
<b>Case 2</b>: When the user has enabled MFA, in this case, he will get only session_token and a second api post_login must <br/>
be called with MFA device code and this session token.

+ Request  (application/json)

    + Body 
        {
          "password": "Golfurl##45",
          "username": "graphical"
        }

+ Response (application/json)

    When the MFA has been setup, Now this session token must be used to post_login_mfa api.

    + Body
        {
            "error": false,
            "success": true,
            "data": {
                "challenge_name": "SOFTWARE_TOKEN_MFA",
                "session_token": "aDsyC",
                "challenge_parameters": {
                    "USER_ID_FOR_SRP": "graphical"
                }
            }
        }


+ Response  (application/json)
    
    When the MFA has not been setup, User has to setup MFA to login.
    + Body
        
        {
            "error": false,
            "success": true,
            "data": {
                "challenge_name": "MFA_SETUP",
                "session_token": "EI23ArWHOg",
                "challenge_parameters": {
                    "MFAS_CAN_SETUP": "[\"SOFTWARE_TOKEN_MFA\"]",
                    "USER_ID_FOR_SRP": "graphical"
                }
            }
        }


+ Response (application/json)

    When the user has signed up but has not confirmed with the validation code received on its registered email.
    + Body
        {
            "message": "User is not confirmed",
            "error": true,
            "success": false,
            "data": null
        }

+ Response 400

    When the user is unregistered with us.
    + Body
        {
            "message": "An error occurred (UserNotFoundException) when calling the AdminInitiateAuth operation: User does not exist.",
            "error": true,
            "success": false,
            "data": null
        }

+ Response 400

    When the user has enetered either the wrong username or wrong password.
    + Body
        
        {
            "message": "The username or password is incorrect",
            "error": true,
            "success": false,
            "data": null
        }

##[users/mfa-settings]
###  MFA  [POST]
TO enable or disable MFA, if MFA is disabled the login api will give you 
all the required credentials like IdToken, AccessToken, RefreshToken.

If MFA is enabled, Then users/post-login-mfa must be called to get the 
required credentials.


Process to change MFA TOTP: 
If the user has lost his/her MFA device without disabling the MFA first, 
he needs to contact adminstrator to disable his/her MFA.

+ Request  (application/json)
    + Body 
        
        { "enabled": true,
        "access_token": "dasa"        }
        }
        
+ Response 200
    + Body 
    
        {
            "error": true,
            "success": false,
            "message": null,
            "data": null
        }


+ Response 400
    + Body
    
        {
            "error": true,
            "success": false,
            "message": "Invalid Verification code",
            "data": null
        }


+ Response 400
    + Body
        
        {
            "error": true,
            "success": false,
            "message": "Username doesnt exists",
            "data": null
        }





##[users/associate-mfa]
### Associate mfa setup [POST]

The login is only enabled for MFA, SO after the user signup and confirm_signup, the user 
needs to associate a MFA with his/her login. The user logins and will receive a session_token 
which must be used here.

+ Request  (application/json)
    
    + Body 
        {
          "session": "2eoKfhw",
        }

+ Request  (application/json)
    
    + Body 
        {
          "access_token": "2lecR6dM2QSeoKfhw",
        }

+ Response (application/json)
    
    This secret_code in response must be used to generate a time base QR code , Tools like 
    python-totp , time base OTP or google authenticator can be used 
    
    + Body
        {
            "message": "success",
            "error": false,
            "success": true,
            "data": {
                "secret_code": "KGR2HE3WDWXKUXYE225DFASSTHNVQTMSGFIA",
                "session_token": "anhxDd0LDult1dYsMk0eQg0wQ"
            }
        }


+ Response (application/json)
    When the user is trying to reuse the session token or the MFA has already been setup, or the session has expired genuinely
    + Body

        
        {
            "message": "Session has expired",
            "error": true,
            "success": false,
            "data": null
        }


## [users/verify-mfa]
### verify mfa setup [POST]

After the user has associated MFA and TOTP has been enabled with secret, this api must be used to verify the present totp.

+ Request  (application/json)
    code is TOTP from tool.
    session must be the session token from /users/associate-mfa api given in response.
    
    + Body 
        {
            "session": "vm0uOlsjAIt1zskzf2EyEA8eiLVkvA",
             "username": "graphical",
             "code": "790972"
            }

+ Request  (application/json)
    code is TOTP from tool.
    access_token must be the access_token token from /users/login api given in response.
    
    + Body 
        {
            "access_token": "vv7lsjAIt1zskzf2EyEA8eiLVkvA",
             "username": "graphical",
             "code": "790972"
            }


+ Response (application/json)
    
    + Body
        
        {
            "message": "success",
            "error": false,
            "success": true,
            "data": {
                "session_token": "_Ba9FaQ_8LkL3G4lwnY9Few3bDrqSMZg_JdS2Lw"
            }
        }


+ Response (application/json)
    When the user is trying to reuse the session token after a failed attempt.
    + Body

        
        {
            "message": "Session has expired",
            "error": true,
            "success": false,
            "data": null
        }

+ Response (application/json)
    When the user is trying to reuse the session token or the MFA has already been setup
    + Body

        {
            "message": "A session can be used only once",
            "error": true,
            "success": false,
            "data": null
        }




## Post login MFA [users/post-login-mfa]
### POST login [POST]

Since MFA is enabled, This api needs to be called after the login API, if the MFA has been setup, 
the login will return a session token, this session token must be passed in the body alongwith the TOTP 
from google authenticator.

+ Request  (application/json)
    code is TOTP from tool.
    session must be the session token from /users/associate-mfa api given in response.
    
    + Body 
        {
            "session": "vv7IOr5FeiLVkvA",
             "username": "graphical",
             "code": "790972"
            }


+ Response 
    + Body
        {
            "message": "Wrong code entered",
            "error": true,
            "success": false,
            "data": null
        }
        
+ Response 
    
    + Body 
    
        {
            "message": "success",
            "error": false,
            "success": true,
            "data": {
                "id_token": "eyJraW2w",
                "refresh_token": "eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2R0NNIiwiYoiUlNBLU9BRVAifQ.Pi52O_fDhrKctY8AwxI7c8NwjqrvT-whF8oxIkqrO0uiXuHyj-gQQuCqWAmibVwMHFc0HFMgeoqYMpxLhvlCXhpuUE0QAp8h2tgMRwG7weDzuthy9thZJiXocu3OeAlAPXA_ci-HFxasMqxo_4yLlisIVKI3RKfHmKvy0Uo6qzofPYVIRSb0mg6D-tPoohqJ3Ly96LKEsxxLqwOTV-RLd6QPfe9wTSXMjGNaTeiCZQ-mzolVSoenv_Z2H_QSV9m2s7yRHzaXxQ00Rigo6xZnRBEsfS3Q49Z563cowhTCvlaMVqXIsDGq7qlxn5PmZI1yTxFBMhc_W8awfzUIw.HNrmDQdtdwspam0QeZdM9Q",
                "access_token": "eyJraWQiOiJaTVFXS05DdEZIQUo4WGQ1ZzdnSDF3M3BtcWFiWnFaV0JMOFZIUlVzPSIsImFsZyI6IlJTMjU2In0.QJWtm0EbLoxcarAvI5Mpo7rTlOR2FiznnaVGt4JK6DQQAcml_Eb3-clkTJwZbxqQhFmUMNEAaR3d5QE9lxMeoSq2jG7QCtrv9HPTWO6y7W4EtjcqA_C5SxDmdm9TfbbKfIFdyjhXzgZJlmVexbJE-8LDcq2YKgfENws7SA5pubwei0SOK7WqRVShs2GrfN1llxQlqiBiek0mDE94w8_2jbMVEY2qfxM_I8IeEzqGmrZcjhrRLVuOa2sk6Qa9g",
                "expires_in": 3600,
                "token_type": "Bearer"
            }
        }


## AWS temporary credentials for users [users/awstempcredentials]
### aws temp credentials [POST]
Temporary credentials for the users required for backup, it will have the permission
only on a folder in s3 Bucket.

+ Request  (application/json)
   Id_token is what you will get from post_login api.
   
   
    + Body 
        {
            "id_token": "vv7IOr5FaaPy0_Th2aPOfdoZ5Ouiz9upDoVETOZE8nqgzPlIO2tOVzsUSMHDDCHu2_zAYX1ljct_KDwJmYqN4ntLQlCv_XUUxt_hiUbLpEbf4CBkCJwEiDiNRT_eLilcX9lw-MH0SAQHiUqB4pyWbB0Ug4pRayoAzav97xdZsApxxWULdhh_EoGQv0ep8SbDS2hf-DR2MTOpf6F3PfwrkxZebJD-CDMK15QTzbcBLOnoD9_Pto9KIypg8fb0eKdCXEAmblm0uOlsjAIt1zskzf2EyEA8eiLVkvA",
            }


+ Response 
    When the token is not a valid openid connect token
    + Body
            {
                "error": true,
                "success": false,
                "message": "An error occurred (NotAuthorizedException) when calling the GetId operation: Invalid login token. Not a valid OpenId Connect identity token.",
                "data": null
            }
        
+ Response 
    When user gives a valid id_token
    
    + Body 
            {
            "data": {
                "identity_id": "ap-south-1:379790a8-db75-49c4-8d5c-470c285267670",
                "access_key": "ASIA267T",
                "secret_key": "cumytZIyR/yQ3KfUQ4u3dhK",
                "session_token": "AgoGb3JpZ2luEFEaCmFwLXNvdXTEig7Bxn+siDGi2t1IVrDpk0zyjsOUacrqt7iOih/liEqYoetgg1gU1f/MS3VK4Ro0UDGYHzmykDxK11l68M/z4nzs9vw58QMyRLdGbDgjG3242odYZxEMIXMmugF"
            },
            "error": false,
            "success": true,
            "message": null
        }



## Forgot password [users/forgot-password]
###  forgot password [POST]
If a user forgot his/her password.

+ Request  (application/json)
    + Body 
        {
            "username": "graphical",
            }


+ Response 
    + Body

        {
            "error": false,
            "success": true,
            "message": "Please check your Registered email id for validation code",
            "data": null
        }


## confirm Forgot password [users/confirm-password]
###  confirm forgot password [POST]
+ Request  (application/json)
    + Body 
        {
          "username": "graphical",
          "code": "254764",
          "newpassword": "Gdoom1234@#"
        }

+ Response 200
    + Body 
    
        {
            "error": false,
            "success": true,
            "message": "Password has been changed successfully",
            "data": null
        }


+ Response 400
    + Body
    
        {
            "error": true,
            "success": false,
            "message": "Invalid Verification code",
            "data": null
        }


+ Response 400
    + Body
        
        {
            "error": true,
            "success": false,
            "message": "Username doesnt exists",
            "data": null
        }
        


#Mnemonics

##Mnemonics [/mnemonics]


## [mnemonics/check-mnemonic]

### check-mnemonic[POST]
If the sanctity of user mnemonic is to be checked, 
    Since we are not storing users mnemonic (only sha3_512 and sha3_256 hashes of the mnemonic), 
    we want to check if the user has entered the right mnemonic or not , 
    this API must be called with sha3_256 hash of the mnemonic.
+ Request  (application/json)
    + Header 
        Authorization: id_token
    + Body 
       
       {
          "username": "graphicaldot",
          "mnemonic_sha_256": "2295050486a54d4627cf30f4dc9f6d43d8612c07dd6ea12b08120f8357808fa6"
        }
        
+ Response 200
    + Body 
        {
            "error": false,
            "success": true,
            "message": "Mnemonic hash matched",
            "data": null
        }

+ Response 400
    + Body 
        {
            "error": true,
            "success": false,
            "message": "sha3_256 hash of mnemonic didnt match",
            "data": null
        }

+ Response 400
    + Body
        {
            "error": true,
            "success": false,
            "message": "User isn't present"
        }
