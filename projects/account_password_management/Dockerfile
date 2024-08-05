FROM xiao75896453/demo-python-requirements

ARG PROJECT_PATH

WORKDIR /app

COPY --from=xiao75896453/demo-python-requirements /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./${PROJECT_PATH} /app/${PROJECT_PATH}
COPY ./lib /app/lib
COPY ./startup_server.sh /app/startup_server.sh

RUN chmod +x startup_server.sh

CMD "/app/startup_server.sh"
