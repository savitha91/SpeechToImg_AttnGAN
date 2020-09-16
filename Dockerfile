FROM conda/miniconda3-centos7
RUN yum install epel-release -y && yum clean all && yum update -y
# link : sudo apt-get install pulseaudio  alsa-utils dbus-x11 libasound2-dev
#pulseaudio depenedency - mac : cmake, json-c, autoconf, automake, libtool, libogg, flac, libvorbis, opus, libsndfile, libsoxr and speexdsp
# /usr/local/Cellar/ :  folder where the above modules are installed

WORKDIR /app
EXPOSE 8501
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --ignore-installed
COPY . .
CMD ["python","AppFlask.py"]
