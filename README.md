# agenda-compartilhada-apisecundaria (SHARP)

Repositorio criado para o desenvolvimento da API de autenticação do projeto SHARP - MVP Full Stack.

## Title: SHARP Authentication API

I------------------------------------------------------------------------------------------I

## Project Description

Authentication API for the SHARP application.

This API is responsible for user authentication and session management.

It communicates with the SHARP Principal API to register users and verify user credentials. After a successful login, the Authentication API creates JWT access and refresh tokens that are stored in HTTP-only cookies.

The API also provides routes for token validation, token refresh and logout.

I------------------------------------------------------------------------------------------I

## Development Tools

Python 3.14
Flask
Flask-OpenAPI3
Flask-CORS
Pydantic
Requests
PyJWT
Docker

I------------------------------------------------------------------------------------------I

## Project Architecture

SHARP is composed of three developed components and one external API:

**Frontend**
- React and TypeScript application.
- Runs on port 5173.
- Sends registration, login, token validation, refresh and logout requests to the Authentication API.
- Communicates with the Principal API to manage application resources.

**Principal API**
- Python and Flask REST API.
- Runs on port 5000.
- Manages users, groups, activities, schedules and participants.
- Communicates with the Authentication API to validate authenticated requests.

**Authentication API**
- Python and Flask REST API.
- Runs on port 5001.
- Responsible for registration, login, JWT validation, token refresh and logout.
- Communicates with the Principal API to register users and verify credentials.
- Generates and validates JWT access and refresh tokens.
- Stores authentication tokens in HTTP-only cookies.

**External API**
- ViaCEP.
- Used by the Principal API to retrieve address information from Brazilian postal codes.

## Project Architecture

The following diagram illustrates the architecture and communication between the components of the Sharp application:

![Sharp Archtecture Diagram](docs/sharp-archtecture.png)

I------------------------------------------------------------------------------------------I

## Local Installation

These instructions can be used to execute the Authentication API locally without Docker.

**Prerequisites**

Python 3.14
pip
Git

The SHARP Principal API must also be running on port 5000 for registration and login to work.

**Using Git Bash**

**1. Clone the repository:**

git clone URL_DO_REPOSITORIO_DA_API_AUTH

**2. Go to the project directory:**

cd agenda-compartilhada-apisecundaria

**3. Create a virtual environment:**

py -m venv venv

**4. Activate the virtual environment:**

source venv/Scripts/activate

**5. Install the dependencies:**

pip install -r requirements.txt

**6. Configure the JWT secret:**

The Authentication API requires the `JWT_SECRET` environment variable to generate and validate JWT tokens.

A secure secret can be generated using Python:

python -c "import secrets; print(secrets.token_hex(32))"

Copy the generated value and configure the environment variable in Git Bash:

export JWT_SECRET="YOUR_GENERATED_SECRET"

The secret must not be committed to the Git repository.

**7. Start the Authentication API:**

py app.py

**The Authentication API will be available at:**

http://localhost:5001

**Swagger documentation will be available at:**

http://localhost:5001/openapi/swagger

**Important:**

When executed locally, the Authentication API uses the following default address to communicate with the Principal API:

http://127.0.0.1:5000

The Principal API must therefore be running on port 5000 for registration and login requests to work.

I------------------------------------------------------------------------------------------I

## Docker Execution

The Authentication API can also be executed inside a Docker container.

**Prerequisites**

Docker Desktop must be installed and running.

The Principal API must also be available for registration and login to work.

**1. Clone the repository:**

git clone URL_DO_REPOSITORIO_DA_API_AUTH

**2. Enter the project directory:**

cd agenda-compartilhada-apisecundaria

**3. Build the Docker image:**

docker build -t sharp-auth .

**4. Create the Docker network used by the SHARP APIs:**

docker network create sharp-network

The Principal API and Authentication API use this network to communicate with each other through their container names.

If the network already exists, it does not need to be created again.

**5. Generate a JWT secret:**

The Authentication API requires a secret key to generate and validate JWT tokens.

A secure secret can be generated using:

python -c "import secrets; print(secrets.token_hex(32))"

Keep the generated value private.

**6. Start the Authentication API container:**

Using Git Bash on Windows:

docker run -d --name sharp-auth \
  --network sharp-network \
  -p 5001:5001 \
  -e MAIN_API_URL=http://sharp-principal:5000 \
  -e JWT_SECRET=YOUR_GENERATED_SECRET \
  sharp-auth

Replace `YOUR_GENERATED_SECRET` with the secret generated in the previous step.

**The parameters used in this command are:**

--name sharp-auth  
Defines the name of the container.

--network sharp-network  
Connects the container to the SHARP Docker network.

-p 5001:5001  
Makes the Authentication API available through port 5001.

-e MAIN_API_URL=http://sharp-principal:5000  
Defines the address used by the Authentication API to communicate with the Principal API.

-e JWT_SECRET=YOUR_GENERATED_SECRET  
Defines the secret key used to generate and validate JWT tokens.

sharp-auth  
Defines the Docker image used to create the container.

**The Authentication API will be available at:**

http://localhost:5001

**Swagger documentation will be available at:**

http://localhost:5001/openapi/swagger

**Important:**

The Principal API container must be connected to the same `sharp-network` network and must use the container name `sharp-principal`.

The instructions for executing the Principal API are available in its own repository.

I------------------------------------------------------------------------------------------I

## Docker Commands

**To view running containers:**

docker ps

**To view all containers:**

docker ps -a

**To view Docker images:**

docker images

**To stop the Authentication API:**

docker stop sharp-auth

**To start the existing Authentication API container again:**

docker start sharp-auth

**To stop and remove the Authentication API container:**

docker stop sharp-auth

docker rm sharp-auth

Removing the Authentication API container invalidates the container configuration, but does not affect the data stored by the Principal API.

When recreating the Authentication API container, configure the `JWT_SECRET` environment variable again.

I------------------------------------------------------------------------------------------I

## Authentication

The Authentication API uses JSON Web Tokens (JWT) to manage authenticated sessions.

After a successful login, two tokens are generated:

**Access Token**

- Used to authenticate requests.
- Valid for 30 minutes.
- Stored in an HTTP-only cookie.
- Sent to the Authentication API when a session needs to be validated.

**Refresh Token**

- Used to generate a new access token when the current access token expires.
- Valid for 7 days.
- Stored in an HTTP-only cookie.
- Used by the `/auth/refresh` route.

The use of HTTP-only cookies prevents the frontend JavaScript code from directly accessing the authentication tokens.

I------------------------------------------------------------------------------------------I

## API Functions

**Register**

POST /auth/register | Register a new user through the Principal API

The Authentication API sends the user information to the Principal API, where the user is stored in the SQLite database.

**Login**

POST /auth/login | Authenticate a user

The Authentication API sends the provided email and password to the Principal API for credential verification.

If the credentials are valid, access and refresh JWT tokens are generated and stored in HTTP-only cookies.

**Validate**

POST /auth/validate | Validate the current access token

Checks if the access token exists, is valid, has not expired and is an access token.

**Refresh**

POST /auth/refresh | Generate a new access token

Validates the refresh token and generates a new access token for the authenticated user.

**Logout**

POST /auth/logout | End the authenticated session

Removes the access and refresh token cookies from the browser.

I------------------------------------------------------------------------------------------I

## Communication with the Principal API

The Authentication API does not store users or application data.

User information is stored by the Principal API in its SQLite database.

During registration:

Authentication API -> Principal API -> SQLite

During login:

Authentication API -> Principal API -> Credential Verification

During authenticated requests to protected resources:

Frontend -> Principal API -> Authentication API -> Token Validation

This separation allows authentication responsibilities to remain in the Authentication API while application data and resources remain managed by the Principal API.

I------------------------------------------------------------------------------------------I

## Environment Variables

**JWT_SECRET**

Secret key used to sign and validate JWT access and refresh tokens.

This variable is required. The Authentication API will not start if it is not configured.

Example:

JWT_SECRET=YOUR_GENERATED_SECRET

The real secret must not be committed to the Git repository.

**MAIN_API_URL**

Defines the address of the SHARP Principal API.

When running locally, the default value is:

http://127.0.0.1:5000

When running with Docker on `sharp-network`:

http://sharp-principal:5000