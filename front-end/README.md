# Front end
We want a front end to easily start/stop the server, keep track of who started the server and is on it, automatically shut it down if it is not in use, and manage the server processes without having to SSH in.

## Features
* start/stop the server
    * keep track of who performed those actions
    * keep track of how long the server has been on
* track the server's current external IP address (don't want to have to pay for a static one)
* keep track of who is on the server, how long they've been on
* automatically shut the server down if no one has been on it in a while
    * send admin a notification when this happens?
* users need to be authenticated before being allowed to manipulate the server

## Infrastructure
Although we probably don't need the interface to be running constantly, we do need it to perform occasional checks and have many different HTTP endpoints.
Because of this, using cloud functions probably isn't the best idea because we'd need to maintain lots of separate functions, and
Cloud run is a little better in this regard because it can run a full application with multiple endpoints, but it cannot run constantly to be able to run processes in the background; it can only take action when there is an HTTP request.
It also is completely stateless; there is no way to save data between requests (though you could read/write from/to storage buckets or a database).
App engine is another possibility; it is very similar to cloud run, and although it has access to a `/tmp` directory, anything saved there is not persisted between instances.
So if we want to keep records of how the server has been managed, we need to have access to a database.
GCP has several database products, but the only two that fall under the free tier are Bigquery and Firestore.
Bigquery is an column-store database for OLAP loads, which will be very slow for the row-by-row writing we will be using it for mostly.
Firestore is a no-SQL database, which is apparently pretty fast, but I don't really know too much about it.

To be fair, the simplest possible thing we could do at the moment is to simply deploy a flask app on a free-tier machine running 24/7 and use SQLite as a database.