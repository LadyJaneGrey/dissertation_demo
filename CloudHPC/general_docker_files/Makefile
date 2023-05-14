
.PHONY: clean

clean:
	-docker stop $(shell docker ps -a -q)
	-docker rm -f $(shell docker ps -a -q)
	-docker rmi -f $(shell docker images -a -q)
	-docker volume prune -f

remove-buildx:
	for builder in $(shell docker buildx ls | awk 'NR>1 {print $$1}'); do \
		docker buildx rm $$builder; \
	done

run_image: 
	make remove-buildx
	make clean
	docker build . -t random && docker run -it random bash

# make remove_builders: 
	
# docker buildx build --push --platform linux/amd64,linux/arm64 -t ronnydonny/project-benchmarks-y3:hpl-testhpcg-ssh .


# * docker buildx create --name hpl-builder
# * docker buildx use hpl-builder
# * docker buildx build --platform linux/amd64,linux/arm64 -t gcr.io/mine/image:latest --push .