FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime
ADD ./ /trainer
WORKDIR /trainer
#RUN apt-get -y update && apt-get -y install nvidia-cuda-toolkit
#RUN conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch-lts -c nvidia
RUN conda install -c conda-forge xgboost
RUN pip install -r requirements.txt 
CMD ["run.sh"]