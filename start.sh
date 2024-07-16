#!/bin/zsh

CONTAINER_NAME="app"


run() {
  python src/manage.py collectstatic --no-input && python src/manage.py migrate && gunicorn -b 0.0.0.0:8000 src.core.wsgi --reload
}

create-admin() {
  echo "Creating a super user"
  docker exec -it app bash -c "python src/manage.py createsuperuser"
}

generate-env() {
  echo "Generating .env from template"
  cp .config/.env.template .config/.env
}

start() {
  echo "Build and run the application"
  generate-env
  docker-compose up --build
}

stop() {
    echo "Stopping and removing Docker container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
}

usage() {
    echo -e "Usage: ./start.sh <command>\n"
    echo -e "Commands:"
    echo -e "\t create-admin:\tCreating an admin"
    echo -e "\t start:\t\tProject launch"
    echo -e "\t stop:\t\tStopping the project"
}

case "$1" in
    run)
        run;;
    create-admin)
        create-admin;;
    generate-env)
        generate-env;;
    start)
        start;;
    stop)
        stop;;
    *)
        usage
        exit 1
        ;;
esac