# Connected Garden API

## About

This project is a light and basic REST API which aim to manage sensors.
This API is developed with flask, a micro Python web framework with the help of the FlaskRestfull extension.
For now the API only has two resources, sensor and sensor_type. The reason for this is that my main concern is to fit to REAL REST philosophy, without going to extrem ones like HATEOAS. I also want to use this project to try python FlaskRest Sphinx documentation module to offer a usefull and easy-to-use API documentation. Furthermore I want to do real TDD this time :) All developers know the problem, we always want to do it but the time goes and direct coding seems more and more to be the right and shortest path to delivery.

This time I have no deadlines (except the ones I put myself) so I'm gonna take my time and do the things right, sexy and slowly instead of quick and dirty :)!

Since the first time I started the project I have already refactored all the routing and resources access once and I am reworking it again (see branch CG-S-01). I spend most of my working time brainstorming and discusing with friends and buddies (particularly [Kaze GH](https://github.com/m-brunet)) about RESTFULL definition and philosophy.

## Project structure

The app folder contains all the project sources. See the app [readme](https://github.com/Starlight42/connected-garden/blob/master/app/README.md) file for more information.
The requirements.txt file contains all the Python dependences that are necessary to run the project.
In a virtualenv just run :

```python
pip install -r requirements.txt
```