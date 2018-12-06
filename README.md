# organizer-backend

This is the backend service powering my [organizer](https://github.com/jchio001/organizer) app. It does CRUD things 
related to scheduling future events & tracking past events. It uses python3, flask, and PSQL and it's currently 
deployed on Heroku.

## Getting Started

First, clone the clone from Github:
```bash
https://github.com/jchio001/organizer-backend.git
```

Before beginning development, please ensure that the following tools are installed on your laptop:
- Python 3 (NOTE: Python 2.7 is the default on Mac! [This guide](
https://docs.python-guide.org/starting/install3/osx/) gives a pretty good rundown on installing Python 3 with Brew. 
Be aware that there's 2 versions of Python on your laptop and to specify Python 3, use python3/pip3 instead! Currently, 
this app is using <b>Python 3.7</b>)
- virtualenv (This should be done after installing Python3! Virtualenvs allows us to isolate python dependencies for a 
project, meaning that we have multiple projects cleanly running multiple different versions of a library. [Here's a 
good guide on installing and setting up a virtualenv.](
https://packaging.python.org/guides/installing-using-pip-and-virtualenv/))  

Once the Python environment has been set up correctly and that there's a virtualenv up and running, download all the 
requirements contained in `requirements.txt` with:
```bash
pip3 install -r requirements.txt
```

This should download all the libraries needed for the project and contain them within your virtualenv.

For security reasons, a lot of critical constant values are hidden in environment variables. These values 
(as of currently) are:
- PSQL Database URI (`FOOD_ORGANIZER_DB_URI`)
- API Key for Google (`FOOD_ORGANIZER_GOOGLE_API_KEY`)
- Client id for Google (`FOOD_ORGANIZER_GOOGLE_SERVER_CLIENT_ID`)
- JWT secret (`FOOD_ORGANIZER_JWT_SECRET`)

If these values are not set as environment variables (whether you're running locally or on Heroku), the code will 
<b>crash</b>. Make sure that these environment variables are set when you're running your code!

## Running the application

### Deploying locally 

To deploy the application locally, run:
```bash
gunicorn -w 2 -b 0.0.0.0:<put_port_number_here> routes:app
```

If you are suddenly getting errors related to missing certain library requirements, please check to see if you have a 
virtualenv running in your project directory. If not, please run it and try again.

### Deploying to Heroku

Alternatively, if you want a better sense of how the app runs in its actual "production" environment, you can spin up 
your own Heroku server instance & deploy your code there. If you're not familiar with Heroku, you can begin by 
downloading and setting up the tools listed in the `Introduction` and `Set Up` tabs of 
[this guide](https://devcenter.heroku.com/articles/getting-started-with-python). Cloning the demo application is not 
needed, as you should be cloning the actual `organizer-backend` instead. 

Once you have heroku's command line interface (CLI) set up, you can create an application by running:
```bash
heroku create
```

Or if you want an actual name for Heroku application:
```bash
heroku apps:create <whatever name you want here>
```

You may have to provision an instance of PSQL (unsure if creating a Heroku app from command line creates an instance by 
default). If so, you can do so through the `Resources` tab for your Heroku app on Heroku's website. 

If you're feeling really lazy, here's a button for you to press that does most things for you:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jchio001/organizer-backend)

## Contributing

- Pull requests should be submitted through your own fork of the codebase
- If your pull request installs new requirements, please run `pip3 freeze > requirements.txt` before submitting a PR
- Pull requests <i>must</i> have a test plan before they can be successfully merged in. Doesn't matter if it's unit 
tests or testing locally/on a Heroku instance: just make sure your code is tested in some reasonable way.

## License

[License as of now (I probably need to change this as some point.)](https://www.youtube.com/watch?v=CXerF6crDRs)