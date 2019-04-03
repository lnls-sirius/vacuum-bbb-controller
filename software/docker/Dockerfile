FROM debian:9
LABEL maintainer="Rafael Ito <rafael.ito@lnls.br>"A
USER root

#=================================================
# install prerequisites
#=================================================
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    git \
    libreadline-gplv2-dev \
    python3 \
    python \
    python-pip \
    python3-pip \
    pyqt5-dev-tools \
    python3-pyqt5 \
    python3-pyqt5.qtsvg \
    python3-pyqt5.qtwebkit \
    qttools5-dev-tools 

RUN pip install pyepics

#=================================================
# install EPICS base
#=================================================
WORKDIR /opt
RUN mkdir epics-R3.15.6
WORKDIR epics-R3.15.6
RUN wget https://epics.anl.gov/download/base/base-3.15.6.tar.gz
RUN tar -xvzf base-3.15.6.tar.gz
RUN rm base-3.15.6.tar.gz
RUN mv base-3.15.6 base
WORKDIR base
RUN make
# set EPICS environment variables:
ENV EPICS_CA_ADDR_LIST="10.128.255.255"
ENV EPICS_CA_AUTO_ADDR_LIST=NO
ENV EPICS_CA_MAX_ARRAY_BYTES=51200
ENV EPICS_BASE=/opt/epics-R3.15.6/base
ENV EPICS_HOST_ARCH=linux-x86_64
ENV PATH="$PATH:/opt/epics-R3.15.6/base/bin/linux-x86_64"

#=================================================
# installing PyDM 1.6.5
#=================================================
WORKDIR /opt
RUN wget https://github.com/slaclab/pydm/archive/v1.6.5.tar.gz
RUN tar -xvzf v1.6.5.tar.gz
RUN rm v1.6.5.tar.gz
WORKDIR pydm-1.6.5
RUN sed -i -e '31s/extras/#extras/' -e '32i\ \ \ \ pass' setup.py
RUN pip3 install .[all]
RUN sed -i -e '$a\PYQTDESIGNERPATH=/opt/pydm-1.6.5' /etc/environment

#=================================================
# cloning VBC project
#=================================================
WORKDIR /opt
RUN git clone https://github.com/lnls-sirius/vacuum-bbb-controller
WORKDIR /opt/vacuum-bbb-controller/software/pydm/pydm_1.2/python

CMD ./start.sh
