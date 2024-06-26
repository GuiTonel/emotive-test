# Emotive Test -  Mars Rover Gif Generator

## The Idea
The project main goal is to generate a gif from the images provided by the specified Mars Rover from Nasa API.

## Getting Started
Dependencies:
* Docker - See [Get Docker](https://docs.docker.com/get-docker/)
* Docker Compose - Installed with Docker Desktop, See [Install Docker Compose](https://docs.docker.com/compose/install/)

With the dependencies installed, running the project is as simple as running:
```bash
docker compose up
```

This will pull the required Docker images and spin up a container running your service on http://localhost:8000/swagger.

On that page you can see two routes:
 - [POST] /videos
 - [GET] /videos/\<video-id\>

### Generating a video
The first route `[POST] /videos` is responsible to ask for a video to be generated. On this, route you can provide the following body:
```
{
  "requested_rover": "CUR",
  "requested_camera": "FHAZ",
  "requested_date": "2016-06-4"
}
```
- Requested Rover: Is the Mars Rover that the video should be generated from. It can be one of the three option `[CUR, OPP, SPI]` - Representing the rovers Curiosity, Opportunity and Spirity, respectively. If not provided, it will be `CUR`;
- Request Camera: Is the Rover Camera. It can be `[FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM, PANCAM, MINITES]` - Representing each provided camera by Nasa API (You can see more informations in [NASA Documentation](https://api.nasa.gov/index.html#browseAPI)). If not provided, it will be `FHAZ`;
- Requested Date: Is the earth date that the photos will be taken. It can be any date in the format `YYYY-MM-DD`. If not provided it will be the current day.

None of these parameters are required, any empty one will be changed by a default value.

The response of this request will be something like this:
```
{
  "video_id": "8f739167-7280-4113-8617-8143c8935a70"
}
```

### Requesting a video
After the first request, the video will be generated asynchronously. In that way, with the `video_id` provided earlier, you can check the status of your video on the second Route `[GET] /videos/\<video-id\>`.

The request will return you something like this:
```
{
  "file": "",
  "status": "Not Ready"
}
```

Which means, File is the url of the video, if the video is not ready yet, it will be empty as presented, otherwise, it will be a URL, as follows. 

The status, is the status of the video, if not ready it will be `Not Ready` as presented, if done it will be `Done` as follows.
```
{
  "file": "http://127.0.0.1:8000/media/videos/70fb5dd3352b03966bcbee66bb94b5d0.gif",
  "status": "Done"
}
```
### The video
You can access the provided URL to see your generated gif. If the provided informations results in no photos from the NASA API, the gif will be a default one. If not, it will be a soft gif with all the photos collected, from the first page, of that rover and that camera on that day.

![Alt Text](./c8d51b28469865f0202a7f45b8413d6e.gif)

### Shut Down
To end the service, press `Ctrl+C`

## Final Considerations
The project is being commited with the `.env` already included to make things easier. The only real sensitive information is the `NASA_API_KEY`, which can be freely generated by anyone.

There are some details about the development that might be interesting to discuss in the interview, such as celery integration and the error handler.

Furthermore, the project was a lot of fun to develop and the whole test was very interesting. Hope you like :)
