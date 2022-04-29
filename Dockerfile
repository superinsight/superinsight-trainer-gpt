FROM nvcr.io/nvidia/pytorch:21.08-py3
ADD ./ /app
WORKDIR /app
RUN apt-get -y update
RUN pip install -r requirements.txt 
ENV WANDB_DISABLED=true
CMD ["python","main.py"]