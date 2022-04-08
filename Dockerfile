FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime
ADD ./ /trainer
WORKDIR /trainer
RUN conda install -c conda-forge xgboost
RUN pip install -r requirements.txt 

CMD ["run.sh"]