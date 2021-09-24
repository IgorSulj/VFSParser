FROM ubuntu:20.04
WORKDIR ./app

# Copy project files
COPY vfs_parser.py ./
COPY telegram.py ./
COPY requirements.txt ./
COPY credentials.py ./

# Installing all requirements
RUN apt update
RUN apt install firefox -y
RUN apt install firefox-geckodriver -y
RUN apt install python3.9 -y
RUN apt install python3-pip -y
RUN python3.9 -m pip install -r requirements.txt

# Starting the app
CMD ["python3.9", "telegram.py"]

