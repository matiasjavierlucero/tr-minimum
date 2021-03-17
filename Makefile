
project=tecno-red
app_name=plant-management
app_version=1.0

build:
	@docker build --tag $(project)/$(app_name):$(app_version) --tag $(project)/$(app_name):latest .

run:
	docker run -d -p 8050:8050 --name $(app_name) $(project)/$(app_name):$(app_version)

logs:
	docker logs -f $(app_name) 

kill:
	@echo 'Killing container...'
	@docker ps -a | grep $(app_name) | awk '{print $$1}' | xargs docker rm -f -v

.PHONY: build run kill logs