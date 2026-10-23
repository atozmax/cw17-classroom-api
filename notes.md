image =>
pull from dockerhub
build from local

container =>
docker run


docker build -t classroom-api:0.1.0 .   
converts Dockerfile to image


docker run -p 8000:8000 classroom-api:0.2.0
converts image to container

--rm
-d


(.venv) amir@Amirs-MacBook-Pro classroom-api % docker run -p 8000:8000 classroom-api:0.2.0  
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
IN THE MIDDLE OF THE REQUEST/RESPONSE
IN THE MIDDLE OF THE REQUEST/RESPONSE
INFO:     192.168.65.1:39146 - "GET / HTTP/1.1" 404 Not Found
INFO:     192.168.65.1:53260 - "GET /json/version HTTP/1.1" 404 Not Found
IN THE MIDDLE OF THE REQUEST/RESPONSE
INFO:     192.168.65.1:16845 - "GET /docs HTTP/1.1" 200 OK
IN THE MIDDLE OF THE REQUEST/RESPONSE
INFO:     192.168.65.1:16845 - "GET /openapi.json HTTP/1.1" 200 OK
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [1]
(.venv) amir@Amirs-MacBook-Pro classroom-api % 
(.venv) amir@Amirs-MacBook-Pro classroom-api % 
(.venv) amir@Amirs-MacBook-Pro classroom-api % docker run -p 8000:8000 -d classroom-api:0.2.0 
e0180bb1ba2f2bd72d619875f36362c90e0317698bb8ed5103041ecadd3c51fb