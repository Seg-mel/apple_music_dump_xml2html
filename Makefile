# Param default values

i := "input.xml"
o := "output.html"


convert:
	@python am_xml2html -i $(i) -o $(o)

convert-docker:
	@docker compose -f docker/docker-compose.yml run --rm -e INPUT=$(i) -e OUTPUT=$(o) am_xml2html


# --- For development ---

ruff:  # Run `ruff` code formatter
	@docker compose -f docker/docker-compose.yml run --rm amx2h_ruff
# Here `--rm` option automatically removes container after the command finishes

rm-images:  # Stop project + remove containers, images
	@docker compose -f docker/docker-compose.yml down --rmi all
	@docker compose -f docker/docker-compose.yml --profile donotstart down --rmi all
# Here `--rmi all` removes images
# Have to select images with `profiles: donotstart` setting separately (they're not picked up by default)

rm-all: rm-images  # Stop project + remove build cache, containers, images, volumes
	@docker compose -f docker/docker-compose.yml down --volumes
	@docker builder prune --force --filter "label=com.docker.compose.project=am_xml2html"
# Here `--volumes` removes volumes
# Here `--filter` removes all build cache related to this project
# Here `--force` do not prompt for confirmation

