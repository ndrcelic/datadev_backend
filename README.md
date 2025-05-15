This is a README file of project.

This project, both backend and frontend, are dockerized.

Steps to start a backend are bellow:

    ******* BACKEND *******
    1. Open in terminal a root path of application (../datadev_backend)
    2. Type in terminal this: **docker compose up -d --build**
    3. Run a migrations: **docker compose exec web flask --app run db upgrade**
    4. Start a tests: **docker compose exec web python -m unittest discover image_app**

    ******* FRONTEND *******
    1. Open in terminal a root path of application (../datadev_frontend)
    2. Type in terminal this: **docker compose up -d --build**
    3. A page will be opend in the browser (http://localhos:3000)


Flask framework is used for backend part of application.
    Database - PostgreSQL
    REST     - Flask-RESTful
    ORM      - SQLAlchemy

React JS is used as frontend framework.
    Bootstrap is used for UI.


How to test APP:

    1. Import the picture(s). After that you can see list of pictures on the right side of window.

    2. On the left side, you can see the canvas. Once, when you choose a picture, this picture will be on the canvas.

    3. Above the canvas are 2 buttons (Draw Box and Draw Polygon).

    4. Depending on your selection, you can either draw a box by dragging the mouse or create a polygon by adding points.
        Once you have added enough points, clicking the "Finished and View polygon", the edges will be drawn.

    5. Also, there are Undo and Redo option (for box, drawn polygon and points).

    6. The image cannot be changed while drawing. It can only be modified after saving the shapes ("Save shapes" button) or
       clearing everything ("Clear All" button).

    7. By clicking the "Get All Annotations" button, you will load all previous annotations for the image.
       The shapes will be displayed on the image (canvas), and the coordinate values appear in JSON format bellow the canvas.

    8. By clicking the "Export" button, you will download a JSON file containing two dataset:
       one in COCO format and the other in standard JSON format.