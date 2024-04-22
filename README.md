<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">scalable django backend</h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/kylelobo/The-Documentation-Compendium/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

---

<p align="center"> Assignment for Backend Developer (Python Django) - Technical Evaluation<br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Prerequisites](#Prerequisites)
- [Installing](#Installing)
- [Usage](#usage)
- [Cron Jobs Setup](#Cron_Jobs)
- [Unit Test ](#tests)

## 🧐 About <a name = "about"></a>
Assignment for Backend Developer (Python Django) - Technical Evaluation

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before installing the Django project, ensure you have the following prerequisites installed:

1. **Python**: Django is a Python web framework, so you need Python installed on your system. You can download and install Python from the [official website](https://www.python.org/downloads/).

2. **PIP**: PIP is a package manager for Python that allows you to install and manage Python packages. It usually comes pre-installed with Python versions 3.4 and above. If you don't have PIP installed, you can install it by following the instructions on the [official PIP website](https://pip.pypa.io/en/stable/installation/).

3. **PostgreSQL with PostGIS**: Django uses a database to store its data, and if you are using spatial data, you'll need to install PostgreSQL with PostGIS extension. You can follow the instructions in this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-20-04) to install PostgreSQL, PostGIS [tutorial](https://www.igismap.com/install-postgis-postgresql-ubuntu/) and then install PostGIS by running:


## Installing

Once you have Python and PIP installed, follow these steps to set up your Django development environment:

1. **Create a virtual environment**: It's recommended to use a virtual environment to manage dependencies for your Django project. Navigate to your project directory in the terminal and run:

    ```bash
    python3 -m venv myenv
    ```

    This command will create a virtual environment named `myenv` in your project directory.

2. **Activate the virtual environment**: Activate the virtual environment by running:

    ```bash
    source myenv/bin/activate
    ```

3. **Install requirements**: With the virtual environment activated, install requirements using PIP:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**: Create a `.env` file in your project's root directory and add the following environment variables:

    ```plaintext
    MYPROJECT_ENV = dev
    EMAIL_HOST_USER = 'your_email@example.com'
    EMAIL_HOST_PASSWORD = 'create password from gmail account under settings>secuity>Passkeys and secuity keys'
    DB_NAME = 'your_database_name'
    DB_USER = 'your_database_user'
    DB_PASSWORD = 'your_database_password'
    ```

    Replace the values with your actual email host credentials and database information.

5. **Run migrations**: Before running the development server, apply database migrations by running:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Run the development server**: Navigate into your project directory and start the Django development server by running:

    ```bash
    cd scalable-django-backend
    python manage.py runserver
    ```

7. **Access the development server**: Once the server is running, open a web browser and go to `http://127.0.0.1:8000/` to see your Django project in action.

End with an example of getting some data out of the system or using it for a little demo.

## 🎈 Usage <a name="usage"></a>

To start using the system, follow these steps:

1. **Create Customer Users**:
   - Navigate to the `dummy` directory in your terminal:
     ```bash
     cd dummy
     ```
   - Run the `load_user.py` script to create customer users:
     ```bash
     python load_user.py
     ```
   This script will populate the system with customer users.

2. **Login to the System**:
   - Use one of the following usernames: `user1`, `user2`, `user3`, and soon upto 100 users. (These users are created by the script in step 1.)
   - The password for all users is `common_password`.

3. **Access System Features**:
   - Once logged in, you can access various features of the system based on the user's role and permissions.

4. **Explore and Interact**:
   - Explore the system functionalities, perform actions, and interact with the interface.


for api urls, there swagger api url /swagger  you get more details about API

## Managing Cron Jobs<a name = "Cron_Jobs"></a>

To manage cron jobs within the Django project, you can use Django's `django-crontab` package. Follow the instructions below:

### Adding a Cron Job

To add a new cron job defined in the Django settings, run the following command:

```bash
python manage.py crontab add
```


## 🔧 Running the tests <a name = "tests"></a>

To run the unit tests for this system, use the following command:

```bash
python manage.py test
```

Executing this command will trigger the execution of all unit tests defined within the above project. It ensures that individual components of the system function correctly in isolation.
    # scalable-django-backend
