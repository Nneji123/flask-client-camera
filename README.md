
# Real-time Image Processing using Flask and OpenCV

## About

**This is a real-time image processing application built using Flask and OpenCV. The application receives a video stream from the client and processes it using OpenCV. The processed video is then sent back to the client for display.**


## Repository Structure
```bash
├── Dockerfile
├── README.md
├── app.py
├── docker-compose.yml
├── requirements.txt
└── templates
    ├── index.html
    └── static
        └── logo.ico
```


## Tools Used

The application was built using the following tools:

- Flask: A micro web framework written in Python.
- Socket.IO: A library that enables real-time, bidirectional communication between web clients and servers.
- OpenCV: A computer vision library with Python bindings.
- Docker: A tool designed to make it easier to create, deploy, and run applications by using containers.
  


## How to run the application (using virtual environment)

1. Clone the repository: 
   `git clone https://github.com/Nneji123/flask-client-camera.git`
2. Create a virtual environment: `python3 -m venv env`
3. Activate the virtual environment: `source env/bin/activate` or `source env/Scripts/activate` if you use windows os.
4. Install the required packages: `pip install -r requirements.txt`
5. Start the application: `python app.py`

## How to run the application (using gitpod)

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Nneji123/flask-client-camera)


## How to run the application (using Docker and Docker Compose)

1. Clone the repository: `git clone https://github.com/your_username/real-time-image-processing.git`
2. Install Docker and Docker Compose on your machine
3. Build the Docker image: `docker build -t image-processing .`
4. Start the Docker container: `docker run -p 5000:5000 -it image-processing`
    
Alternatively, you can use Docker Compose to start the application: `docker-compose up -d --build`

## How to deploy the application

Click the button below to deploy the application to `render.com`
  
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## License
[MIT](./README.md)




