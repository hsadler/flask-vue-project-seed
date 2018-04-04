
cd .. && \
docker-compose -f docker-compose.dev.yml up --build --force-recreate \
--remove-orphans --abort-on-container-exit
