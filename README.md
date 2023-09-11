<h1 align="center">Django DRF Clean Architecture</h1>
<h3 align="center">Just a big starting point for any backend project</h3>
<p align="center">
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://www.djangoproject.com/" target="_blank"> <img src="https://user-images.githubusercontent.com/29748439/177030588-a1916efd-384b-439a-9b30-24dd24dd48b6.png" alt="django" width="60" height="40"/> </a> 
<a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://www.postgresql.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a>
<a href="https://www.nginx.com" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" alt="nginx" width="40" height="40"/> </a>
<a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a>
</p>

[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Guideline

- [Goal](#goal)
- [Repo Features](#repo-features)
- [Before Setup](#before-setup)
- [Development usage](#development-usage)
- [Production usage](#production-usage)
- [License](#license)
- [Reources](#resources)
- [Special Thanks To](#special-thanks-to)
- [Bugs](#bugs)

# Goal

This project main goal is to provide an enreach starting point for mid-level to large scale projects.

# Repo Features

<ul>
  <li>
    <strong>Latest LTS Django4.2</strong>        
    <p>Latest LTS included 4.2.x and needed requirements</p>
  </li>

  <li>
    <strong>Git</strong>        
    <p>python gitignore and README with license</p>
  </li>

  <li>
    <strong>Docker File</strong>        
    <p>Latest Python image dockerfile prod/dev and dockerignore</p>
  </li>
  
  <li>
    <strong>Docker Compose</strong>        
    <p>Docker compose prod/dev and minimum setup for django and db included,with volumes and network</p>
  </li>
  
  <li>
    <strong>Nginx + Gunicorn</strong>        
    <p>included nginx setup with gunicorn as serving service and file configs for production</p>
  </li>
 
  <li>
    <strong>Django env</strong>        
    <p>enviroment sample file and setup</p>
  </li>
 
  <li>
    <strong>Github Actions</strong>
    <p>Pre Configurations for CI/CD in github actions. plus two step jobs for testing and deploying on vps with docker</p>
  </li>

  <li>
    <strong>Black and Flake8</strong>
    <p>Included Pep8 and Flake8 configuration file for test purposes.Reformating the codes and bring the best out of it.</p>
  </li>

  <li>
    <strong>Django Rest Framework</strong>
    <p>Included DRF package and all its dependencies along side of cors headers. plus simplejwt and jwt authentication for identity.</p>
  </li>

  <li>
    <strong>Swagger and Redoc</strong>
    <p>Allowing the urls to include rest api documentations</p>
  </li>

  <li>
    <strong>Locust</strong>
    <p>locust for api load testing</p>
  </li>

  <li>
    <strong>Seq</strong>
    <p> Seq logging for log monitoring</p>
  </li>

  <li>
    <strong>Attrs</strong>
    <p>Attrs for Dto</p>
  </li>

  <li>
    <strong>Poetry</strong>
    <p>Poetry for better dependency management</p>
  </li>

  <li>
    <strong>Tests</strong>
    <p>django-pytest and pytest-cov and factoryboy for test and test coverage</p>
  </li>

  <li>
    <strong>Redis</strong>
    <p>Redis and beat for schedules and cache</p>
  </li>

  <li>
    <strong>Integrated Response & Exceptions
    <p>integrated response and exceptions for REST</p>
  </li>

  <li>
    <strong>Djoser</strong>
    <p>Preconfigured Djoser for authentication</p>
  </li>

  <li>
    <strong>Honeypot</strong>
    <p>Honeypot admin panel to ban anyone tries to brute force into /admin</p>
  </li>

  <li>
    <strong>Preconfigured</strong>        
    <p>Preconfigured settings and etc...</p>
  </li>

  <li>
    <strong>README</strong>
    <p>README.md files in all layers for more information</p>
  </li>
</ul>

# Before Setup

<strong>Note:</strong> I Highly recommend checking [Resources](#resources) section.

<ul>
  <li>
    <strong>Read layers README.md</strong>
    <p>Every layer has it's own README.md for furture explanation</p>
  </li>
  <li>
       <strong>Change env variables in /envs to suite your project needs</strong>
        <p>/envs directory contains environment variables for database and django</p>
  </li>
    <li>
       <strong>Review settings in /src/infrastructure/settings</strong>
  </li>
</ul>

# Development usage

You'll need to have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) installed.
It's available on Windows, macOS and most distros of Linux.

If you're using Windows, it will be expected that you're following along inside
of [WSL or WSL
2](https://nickjanetakis.com/blog/a-linux-dev-environment-on-windows-with-wsl-2-docker-desktop-and-more).

That's because we're going to be running shell commands. You can always modify
these commands for PowerShell if you want.

#### Clone this repo anywhere you want and move into the directory:

```sh
git clone https://github.com/alireza0sfr/Django-DRF-Clean-Architecture-Base.git
```

#### Build everything:

_The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python + requirements dependencies._

```sh
docker-compose -f docker/docker-compose.yml up --build
```

Now that everything is built and running we can treat it like any other Django
app.

#### Note:

If you receive an error about a port being in use? Chances are it's because
something on your machine is already running on the same port as one of the services in docker-compose. then you have to change the docker-compose.yml file according to your needs.

#### Check it out in a browser:

Visit <http://localhost:port> in your favorite browser.

# Stage usage

In this phase of the project you can launch the service either in your pc/laptop to use as local host or you can setup on a vps to access through ip or even the domain which is dedicated to it.

```bash
docker-compose -f docker-compose-stage.yml up --build
```

# Production usage

In this phase of the project you can launch the project only on the vps with the domain name connect to it other than that you have to change the settings accordingly.(you can use the stage config as base for the nginx)
But before that don't forget to check nginx config located at /nginx/default.conf the db.
then all you need to do to build the project is to run the command bellow:

```bash
docker-compose -f docker-compose-prod.yml up --build
```

# Security

With special thanks to [Mr.Ali Bigdeli](https://github.com/AliBigdeli) this repo uses his security configs for more info read [this](https://github.com/AliBigdeli/Ultimate-Django4.2-Template/blob/main/README.md#security).

- Mozilla Observatory
  <img src="https://user-images.githubusercontent.com/29748439/187753171-c600c12d-1979-44e7-ad32-65243e777c77.png" alt="security headers" style="max-width:1280px;width:100%" />

- Security Headers
  <img src="https://user-images.githubusercontent.com/29748439/187752756-8368f1dc-e4c2-4256-ab8a-9c7d2a44da00.png" alt="security headers" style="max-width:1280px;width:100%" />

- SSL Checker
  <img src="https://user-images.githubusercontent.com/29748439/187753336-dd575268-f2be-49b9-9934-21928017d518.png" alt="security headers" style="max-width:200px;width:100%; max-height:400px;text-align:center" />

# License

MIT.

# Resources

<strong>Clean Architecture: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html></strong>

# Special Thanks to
  This repository is heavily inspired by [Django Clean Architecture](https://github.com/sdediego/django-clean-architecture) and [Ultimate Django4.2 Template](https://github.com/AliBigdeli/Ultimate-Django4.2-Template)
  repositories.

- [Ali Bigdeli](https://github.com/AliBigdeli)
- [Sergio de Diego](https://github.com/sdediego)

# Bugs

Feel free to let me know if something needs to be fixed. or even any features seems to be needed in this repo.
