# DjangoBookCatalog

## Requirements

- Docker
- Docker Compose

## Installation and Setup

1. **Clone the repository**

    ```sh
    git clone https://github.com/nurbol0tt/book_catalog.git
    cd book_catalog
    ```

2. **Make the start script executable**

    ```sh
    chmod +x ./start.sh
    ```

3. **Run the project**

   To run the project, use the following command:

    ```sh
    ./start.sh start
    ```

   This command will build the Docker image and run the container in the
   background.

4. **Create an admin user**

   To create an admin user, use the following command:

    ```sh
    ./start.sh create-admin
    ```

5. **Stop the project**

    To stop the project and remove the container, use the following command:

    ```sh
    ./start.sh stop
    ```
