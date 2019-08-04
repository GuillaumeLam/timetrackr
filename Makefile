.PHONY: all clean build #release

all: clean build

clean:
	rm -rf bin

build:
	pipenv run buildozer android debug
	gzip -k bin/timetrackr-*-debug.apk
