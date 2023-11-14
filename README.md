# Systems Integration Development Kit #

## Introduction ##

Welcome to the Systems Integration Development Kit! This toolkit is specially designed to facilitate the setup of your development environment and manage dependencies effortlessly for the 1st assignment (TP1) in the Systems Integration class, part of the Informatics Engineering course at IPVC/ESTG.

## Setting Up Your Development Environment ##

Follow the steps below to establish a conducive working environment:

1. **Install Docker Desktop**
   - Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

2. **Create Docker Images and Containers**
   - Navigate to the project's root folder and execute the following command:
     ```
     docker-compose up --build
     ```

3. **Managing Containers**
   - To terminate all applications (containers), employ the STOP signal (Ctrl+C) in the terminal where `docker-compose up` was initiated.
   - For background execution, append the `-d` flag at the end of the command.
   - To halt operations post-assignment (when running in the background), execute:
     ```
     docker-compose down
     ```
     - **Note:** Executing the above command will reset database data. For data retention, consider stopping the container using `docker-compose stop`.

4. **Starting and Stopping Containers**
   - Stopping all containers:
     ```
     docker-compose stop
     ```
   - Restarting all containers:
     ```
     docker-compose start
     ```

## Available Resources ##

### PostgreSQL Database ###

- Accessible at `is-rpc-server:5432`
  - **username**: is
  - **password**: is
  - **database**: is
- Also accessible via `localhost:5432`
- **Note:** Conflicts might occur if another PG instance occupies port 5432. Modify the mapping port in the docker-compose file under the `service db` section to resolve this issue.

### Python Development Environment ###

- **Version:** Python 3.9.18
- **Dependency Management:** Add pre-installed packages in the `requirements.txt` file. Updating dependencies necessitates Docker image rebuilding.
- **Usage:**
  - Access the Python environment by opening a terminal with the following command:
    ```
    docker-compose run --entrypoint sh <service name>

    #example:
    docker-compose run --entrypoint sh rpc-client
    ```
  - Execute scripts other than `main.py` directly as illustrated below:
    ```
    docker-compose run --entrypoint "python another.py" rpc-client 
    ```
  - Utilize watch mode for scripts (beneficial for the rpc-server), enabling automatic server reload upon source code modification:
    ```
    docker-compose run --entrypoint "nodemon main.py" rpc-server 
    ```

___
#### _Informatics Engineering @ipvc/estg, 2023-2024_ ####