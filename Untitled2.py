#!/usr/bin/env python
# coding: utf-8

# ### Kütüphanelerin import edilmesi

# In[1]:


import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
import scipy.io as scio
from scipy.io import loadmat
import torchvision
import os
import argparse
import progress_bar
import numpy as np
import random
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
import pdb
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import torchvision.transforms as tfs
import torchvision.datasets as datasets


# ### Kaiming Normal İnitialization Fonksiyonu

# In[2]:


# m değerine göre normal dağılıma sahip ağırlık değerleri ve nonlinearity değerleri oluşturur.



device = 'cuda' if torch.cuda.is_available() else 'cpu'
best_acc = 0  # best test accuracy
start_epoch = 1  # start from epoch 0 or last checkpoint epoch


import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler

import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
from PIL import Image
from tempfile import TemporaryDirectory

plt.ion()   # interactive mode


# In[10]:


from torchvision import datasets, transforms
from torch.utils.data import DataLoader





import multiprocessing

def worker_function():

    liste = ["flowers_train", "flowers_test"]
    data_transforms = {
        liste[0]: transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
        ]),
        liste[1]: transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
        ]),
    }

    data_dir = "C:\\users\\vuralbayrakli\\lwf"  # veri kümesinin ana dizini

    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in [liste[0], liste[1]]}
    dataloaders = {x: DataLoader(image_datasets[x], batch_size=4, shuffle=True, num_workers=4) for x in [liste[0], liste[1]]}
    dataset_sizes = {x: len(image_datasets[x]) for x in [liste[0], liste[1]]}
    class_names = image_datasets[liste[0]].classes




    def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
        since = time.time()

        # Create a temporary directory to save training checkpoints
        with TemporaryDirectory() as tempdir:
            best_model_params_path = os.path.join(tempdir, 'best_model_params.pt')

            torch.save(model.state_dict(), best_model_params_path)
            best_acc = 0.0

            for epoch in range(num_epochs):
                print(f'Epoch {epoch}/{num_epochs - 1}')
                print('-' * 10)

                # Each epoch has a training and validation phase
                for phase in liste:
                    if phase == liste[0]:
                        model.train()  # Set model to training mode
                    else:
                        model.eval()   # Set model to evaluate mode

                    running_loss = 0.0
                    running_corrects = 0

                    # Iterate over data.
                    for inputs, labels in dataloaders[phase]:
                        inputs = inputs.to(device)
                        labels = labels.to(device)

                        # zero the parameter gradients
                        optimizer.zero_grad()

                        # forward
                        # track history if only in train
                        with torch.set_grad_enabled(phase == liste[0]):
                            outputs = model(inputs)
                            _, preds = torch.max(outputs, 1)
                            loss = criterion(outputs, labels)

                            # backward + optimize only if in training phase
                            if phase == liste[0]:
                                loss.backward()
                                optimizer.step()

                        # statistics
                        running_loss += loss.item() * inputs.size(0)
                        running_corrects += torch.sum(preds == labels.data)
                    if phase == liste[0]:
                        scheduler.step()

                    epoch_loss = running_loss / dataset_sizes[phase]
                    epoch_acc = running_corrects.double() / dataset_sizes[phase]

                    print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

                    # deep copy the model
                    if phase == liste[1] and epoch_acc > best_acc:
                        best_acc = epoch_acc
                        torch.save(model.state_dict(), best_model_params_path)

                print()

            time_elapsed = time.time() - since
            print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
            print(f'Best val Acc: {best_acc:4f}')
            best_model_params_path = os.path.join(data_dir, 'best_model_params.pt')
            torch.save(model.state_dict(), best_model_params_path)
            # load best model weights
            model.load_state_dict(torch.load(best_model_params_path))
        return model


    # In[17]:


    model_ft = models.resnet18(weights='IMAGENET1K_V1')
    num_ftrs = model_ft.fc.in_features
    # Here the size of each output sample is set to 2.
    # Alternatively, it can be generalized to ``nn.Linear(num_ftrs, len(class_names))``.
    model_ft.fc = nn.Linear(num_ftrs, 5)
    

    model_ft = model_ft.to(device)

    criterion = nn.CrossEntropyLoss()

    # Observe that all parameters are being optimized
    optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)

    # Decay LR by a factor of 0.1 every 7 epochs
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)


    model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler,
                           num_epochs=1)
    

if __name__ == '__main__':
    multiprocessing.freeze_support()  # freeze_support() fonksiyonunu çağırın

    # Yeni işlem oluşturma
    process = multiprocessing.Process(target=worker_function)
    process.start()
    process.join()






