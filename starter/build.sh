docker build \
    -t jcharo/trivia_app_backend \
    --build-arg PASS=$PASS \
    .




# docker run --name backend_trivia_v2 -dp 5000:5000 trivia_app_backend


# docker run -it --rm -v ${PWD}:/app -v /app/node_modules -p 3000:3000 frontend_test
