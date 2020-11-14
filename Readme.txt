CSE Machine setup
    Steps:
        1. Unzip and save the project. Navigate into the unzipped directory via the command line. (i.e. You should be in the same dirctory as manage.py and this readme file)
        2. Install pipenv with the command 
            - $ pip3 install pipenv
        3. Install project dependancies with 
            - $ python3 -m pipenv install
        4. Activate the projects virual environment with 'python3 -m pipenv shell'
        5. Setup database with the following 2 commands:
            - $ python3 manage.py makemigrations
            - $ python3 manage.py migrate
        6. Run the server with the command
            - $ python3 manage.py runserver

            You should get the following output:

                Performing system checks...

                System check identified no issues (0 silenced).
                November 14, 2020 - 14:08:53
                Django version 3.1.3, using settings 'hermes.settings'
                Starting development server at http://127.0.0.1:8000/
                Quit the server with CONTROL-C.

        Note: If you get the error message 'Django Server Error: port is already in use', you can change the port by passing in a new port via the command line. E.g.
            - $ python3 manage.py runserver 8080

        7. Copy the http address into the url above to use the web application. I.e. http://127.0.0.1:8000/


Deployed Version
    To access the version of the application deployed on the internet, use the url invest-simu.herokuapp.com

Notable Files Locations
    Database Models:
        simulator/models.py
    Site Urls:
        simulator/urls.py
    Page Views
        simulator/views.py
    Backend Logic
        modules/*
        api/*
    Frontend Html Templates
        simulator/templates/*
    Frontend CSS Templates
        static/css/*
    Test Files
        tests/*

Run tests with the following command:
    $ python3 manage.py test tests.<name_of_testfile> 
    e.g.
    $ python3 manage.py test tests.test_search