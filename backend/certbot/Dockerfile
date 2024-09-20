FROM certbot/certbot:latest

ENTRYPOINT ["/bin/sh", "-c", "trap exit TERM; while true; do certbot renew; sleep 12h; done;"]