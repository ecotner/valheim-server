# valheim-server
Project for managing a valheim server in the cloud in a resource-efficient way.
Will be composed of two pieces:
1. Docker container which launches a valheim server
2. Front-end from which the server can be controlled. Will need to spin it up and shut it down so that resources aren't being wasted when no on is playing.

## Server
The server is launched by running a docker container. Run
```bash
docker pull lloesche/valheim-server
```
to download the image.

You can find the [repo for this image here](https://github.com/lloesche/valheim-server-docker).
In the [`server`](./server) subdirectory, I have a `docker-compose.yaml` file that starts/stops the container.
Run
```
docker compose up -d
```
in that directory to launch the server.

If you are running this for the first time, make a copy of `example.env` named `.env` and change the environment variables you want to customize.
I would recommend `SERVER_NAME`, `WORLD_NAME` and `SERVER_PASS` at the bare minimum.

You can check on the status logs by running
```
docker logs -f <container name>
```
(press `ctrl+c` to detach from the logs, but don't worry, this won't kill the server).
You can gracefully shut the container down with
```
docker compose down
```
