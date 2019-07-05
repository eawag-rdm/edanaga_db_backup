imagename := edanagabackup
containername := $(imagename)


install:
	@[ -d v3 ] || ( \
	  virtualenv -p python3 v3; \
	  . ./v3/bin/activate; \
	  pip install pytest requests)

test:
	docker run --rm --entrypoint="" edanagabackup pytest -v

build_image: Dockerfile
	docker build -t $(imagename) .

help:
	@echo "Run the image as command:"
	@echo "docker run --rm -v $(containername):/srv/app/data $(imagename)"
	@echo "Execute at appropriate intervals with Cron."
	@echo "The data will be stored in the named (after the variable \"containername\") volume on the host."

clean:
	@C_EXISTS=$$(docker container inspect $(containername) >/dev/null 2>&1; echo $$?); \
	if [ "$$C_EXISTS" = "0" ]; then \
	  docker rm $(containername); \
	fi
	@I_EXISTS=$$(docker image inspect $(imagename) >/dev/null 2>&1; echo $$?); \
	if [ "$$I_EXISTS" = "0" ]; then \
	  docker rmi $(imagename); \
	fi


.PHONY: install test help build_image clean
