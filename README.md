# authentication-service

Set up postgres instance - https://gist.github.com/phortuin/2fe698b6c741fd84357cec84219c6667


Authentication server:

1. Create user (POST). Receive user login and password from getway, encypt it with hash (store secret as const), 
and save the encrypted data in DB (create internal user ID). With encrypted data, user role is also stored.
2. Authenticate user (GET). Get user login and password, encrypt it, make request to DB - if the user exists,
create JWT and return it:
    - JWT token with a payload containing the user technical identifier (user id from DB?) and an expiration timestamp
    ![alt text](helper_images/bearer_token.png)
    - take a secret key and use it to sign the Header plus Payload and send it back
    - Do I create header?
3. Verify user
