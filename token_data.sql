-- table for refresh tokens: not needed at the moment
CREATE TABLE refresh_tokens (
	user_id VARCHAR ( 100 ) UNIQUE NOT NULL,
	token_id VARCHAR ( 100 ) UNIQUE NOT NULL,
    expiration_timestamp TIMESTAMP NOT NULL,
	PRIMARY KEY (user_id, token_id)
);

GRANT ALL PRIVILEGES ON TABLE user_data TO myuser;
