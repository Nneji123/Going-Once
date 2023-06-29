# Going Once - Django Rest Framework Project

"Going Once" is a Django Rest Framework project that provides an online auction platform, allowing users to buy and sell items in a dynamic and secure environment. This readme file will guide you through the setup, configuration, and features of the project.

## Features

- Docker for easy deployment
- Custom user model for enhanced authentication and user management
- Item, seller, and bidder validation for ensuring data integrity
- Static file hosting with Whitenoise for efficient delivery of static assets
- Image hosting with Cloudinary for seamless image storage and retrieval
- Authentication with dj-rest-auth for secure user authentication and authorization
- Setup and configuration using django-configurations for flexible environment-based configurations
- Automated testing with Django Nose and GitHub Actions for ensuring code quality and reliability

## Screenshots




## Requirements
The requirements are provided in the requirements.txt file contained in this repository.

## Installation and Setup

1. Clone the repository:

```
git clone https://github.com/Nneji123/Going-Once.git
```

2. Navigate to the project directory:

```
cd repo
```

3. Create and activate a virtual environment:

```
python3 -m venv env
source env/bin/activate
```

4. Install the project dependencies:

```
pip install -r requirements.txt
```

5. Set up the environment variables by creating a `.env` file and providing the necessary values:

```
SERVER_MODE="Dev" if set to Prod, Production settings and environment variables will be used.

DEV_SECRET_KEY=

SECRET_KEY=

PROD_SECRET_KEY=

SUPERUSER_EMAIL=
SUPERUSER_PASSWORD=

POSTGRES_URI=

CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

PROD_EMAIL_HOST=
PROD_EMAIL_HOST_USER=
PROD_EMAIL_HOST_PASSWORD=
PROD_EMAIL_PORT=

DEV_EMAIL_HOST = 
DEV_EMAIL_HOST_USER = 
DEV_EMAIL_HOST_PASSWORD = 
DEV_EMAIL_PORT = 

DEBUG=False

PROD_REDIS_URL=

DEV_REDIS_URL=
```

6. Apply database migrations:

```
python manage.py migrate
```

7. Start the development server:

```
python manage.py runserver
```

8. Access the project locally at `http://localhost:8000`.

## Testing

To run the automated tests using Django Nose, execute the following command:

```
python manage.py test
```

GitHub Actions is set up to run tests automatically on every push or pull request.

## Deployment

This project is Docker-ready for easy deployment. You can build and deploy the project using Docker by following these steps:

1. Install Docker on your deployment server.

2. Build the Docker image:

```
docker build -t going-once .
```

3. Run the Docker container:

```
docker run -d -p 8000:8000 going-once
```

Make sure to adjust the port mapping if necessary.

## API Documentation

The API documentation is automatically generated using drf-spectacular. You can access it at `schema/docs/` when running the project locally.
