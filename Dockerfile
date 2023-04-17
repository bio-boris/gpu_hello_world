FROM kbase/sdkpython:3.8.0
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

RUN apt-get update -y && apt-get upgrade -y && apt-get update -y
RUN apt-get install wget linux-headers-$(uname -r) -y
RUN distribution=$(. /etc/os-release;echo $ID$VERSION_ID | sed -e 's/\.//g') && dpkg -i cuda-keyring_1.0-1_all.deb
RUN apt-get update -y && apt-get -y install cuda-drivers


RUN apt-get update -y &&\
apt-get upgrade -y &&\
apt-get update -y &&\
apt-get install wget &&\
apt-get install linux-headers-$(uname -r) &&\ 
distribution=$(. /etc/os-release;echo $ID$VERSION_ID | sed -e 's/\.//g') &&\
dpkg -i cuda-keyring_1.0-1_all.deb &&\
apt-get update &&\ 
apt-get -y install cuda-drivers 
 
# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]