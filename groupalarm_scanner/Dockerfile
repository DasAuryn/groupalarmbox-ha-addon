ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache python3 py3-pip avahi avahi-tools
RUN pip install zeroconf requests --break-system-packages

COPY run.py /run.py
COPY run.sh /run.sh
RUN chmod 755 /run.sh

CMD ["/run.sh"]
