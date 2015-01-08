runinfra:
	cd dock2dns
	@fig up -d
	cd ../thruk
	@fig up -d
	cd ../mongo
	@fig up -d
	
startinfra:
	cd dock2dns
	@fig start
	cd ../thruk
	@fig start
	cd ../mongo
	@fig start

stopinfra:
	cd dock2dns
	@fig stop
	cd ../thruk
	@fig stop
	cd ../mongo
	@fig stop

cleaninfra:
	cd dock2dns
	@fig rm --force
	cd ../thruk
	@fig rm --force
	cd ../mongo
	@fig rm --force

restartinfra: stopinfra startinfra

.PHONY: runinfra startinfra stopinfra cleaninfra
