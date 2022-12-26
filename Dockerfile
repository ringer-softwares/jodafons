#FROM ubuntu:22.10
FROM tensorflow/tensorflow:2.11.0-gpu
USER root



LABEL maintainer "Joao Victor Pinto <jodafons@cern.ch>"

ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV TERM screen
ENV TZ=America/New_York
ENV DEBIAN_FRONTEND=noninteractive
#ENV CPU_N=$(grep -c ^processor /proc/cpuinfo)
ENV CPU_N=40

# update all packages
RUN apt-get update -y --fix-missing

# others
RUN apt-get install -y wget git dpkg-dev \
g++ gcc binutils libx11-dev libxpm-dev \
libxft-dev libxext-dev libglew1.5-dev \
python-dev libboost-all-dev librange-v3-dev \
libboost-python-dev libxerces-c-dev curl

# root dependencies
RUN apt-get install -y dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev \
libxft-dev libxext-dev python3 libssl-dev gfortran libpcre3-dev \
xlibmesa-glu-dev libglew-dev libftgl-dev \
libmysqlclient-dev libfftw3-dev libcfitsio-dev \
graphviz-dev libavahi-compat-libdnssd-dev \
libldap2-dev libxml2-dev libkrb5-dev \
libgsl0-dev qtwebengine5-dev



# Installing cmake3
WORKDIR /usr
RUN wget --progress=dot:giga https://cmake.org/files/v3.19/cmake-3.19.7-Linux-x86_64.sh -P /usr/
RUN chmod 755 cmake-3.19.7-Linux-x86_64.sh
RUN ./cmake-3.19.7-Linux-x86_64.sh --skip-license




WORKDIR /apt
# install ROOT
RUN git clone https://github.com/root-project/root.git
RUN cd root && git checkout v6-26-10
RUN cd root && mkdir buildthis && cd buildthis && cmake  -Dpython_version=3 -Dxrootd=OFF -Dbuiltin_xrootd=OFF .. && make -j$CPU_N
ENV ROOTSYS "/apt/root/buildthis/"
ENV PATH "$ROOTSYS/bin:$PATH"
ENV LD_LIBRARY_PATH "$ROOTSYS/lib:$LD_LIBRARY_PATH"
ENV PYTHONPATH "/apt/root/buildthis/lib:$PYTHONPATH"

RUN pip install --upgrade pip
RUN pip install virtualenv
