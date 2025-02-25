DC = docker compose
APP = deploy/compose/compose-app.yaml
APP_DEV = deploy/compose/compose-app.yaml
POSTGRES = deploy/compose/postgres.yaml
APP_SERVICE = app-api
ENV = --env-file .env

.PHONY: app-dev
app-dev:
	${DC} -f ${APP_DEV} -f ${POSTGRES} ${ENV} up --build -d

.PHONY: app-dev-logs
app-dev-logs:
	${DC} -f ${APP_DEV} -f ${POSTGRES} ${ENV} logs -f

.PHONY: storages
storages:
	${DC} -f ${POSTGRES} ${ENV} up -d --build

.PHONY: down-dev
down-dev:
	${DC} -f ${APP_DEV} -f ${POSTGRES} ${ENV} down

.PHONY: down
down:
	${DC} -f ${APP} -f ${APP_DEV} ${ENV} down

.PHONY: shell
shell:
	${DC} -f ${APP} exec -it ${APP_SERVICE} bash