-- table for storing encrypted user data
CREATE TABLE user_data (
	user_id VARCHAR ( 100 ) PRIMARY KEY,
	login_key VARCHAR ( 100 ) UNIQUE NOT NULL,
	password_key VARCHAR ( 100 ) UNIQUE NOT NULL,
    password_salt VARCHAR ( 100 ) UNIQUE NOT NULL,
    created_on TIMESTAMP NOT NULL
);

GRANT ALL PRIVILEGES ON TABLE user_data TO myuser;
