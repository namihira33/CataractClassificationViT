import torch
from torch.utils.data import Dataset
from torchvision import transforms
import torch.nn as nn
import config
from PIL import Image
import os
import numpy as np
from utils import *
import timm
from timm.data.constants import IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD

#水平断面画像のデータセット
class OCThorizontalDatasetBase(Dataset):
    def __init__(self, root, image_list_file,transform=None,n_per_unit=1,d_type=5):
        image_names,labels,item_indexes = [],[],[]
        item_index = 0
        self.image_list_file = image_list_file

        with open(image_list_file, "r") as f:
            for line in f:
                items = line.split(',')
                if isint(items[1]):

                    if d_type == 4:
                        gender = items[d_type][0]
                        label = 0 if gender == 'M' else 1

                    elif d_type == 3:
                        age = items[d_type]
                        label = 0 if (int(age)<60) else 1

                    else :
                        if isint(items[d_type]):                        
                            label = self.get_label(int(items[d_type][0]))
                    
                    for i in range(n_per_unit):
                        image_name = items[1] + '_' + items[2] + '_' + '{:0=3}'.format(int(i)) + '.jpg'
                        image_name = os.path.join(root,image_name)
                        image_names.append(image_name)
                        labels.append(label)
                        item_indexes.append(item_index)
                        item_index += 1

        self.image_names = np.array(image_names)
        self.labels = np.array(labels)
        self.item_indexes = np.array(item_indexes)
        self.transform = transform


    def __getitem__(self, index):
        image_name = self.image_names[index]
        image = Image.open(image_name).convert('L')
        label = torch.eye(config.n_class)[self.labels[index]]
        #label = [self.labels[index]]
        #label = normal_distribution(self.labels[index])
        item_index = self.item_indexes[index]
        if self.transform is not None:
            image = self.transform(image)

        return (image,torch.Tensor(label),item_index) if self.image_list_file==config.train_info_list else (image,torch.Tensor(label),image_name)

    def __len__(self):
        return len(self.image_names)
        #return 1000

    def pick_label(self, index):
        label = torch.eye(config.n_class)[self.labels[index]]
        return torch.Tensor(label)

    def get_label(self, label_base):
        pass

        
class OCThorizontalDataset(OCThorizontalDatasetBase):
    def get_label(self, label_base):
        if label_base == 1:
            return 0
        elif label_base == 2:
            return 1
        elif label_base == 3:
            return 1
        else:
            #return 2
            return 1

#回転断面画像のデータセット
'''
class OCTspinDatasetBase(Dataset):
    def __init__(self, root, image_list_file,transform=None,n_per_unit=16,d_type=6):
        image_names,labels,item_indexes = [],[],[]
        item_index = 0
        self.image_list_file = image_list_file
        self.images = torch.empty(0)

        with open(image_list_file, "r") as f:
            for line in f:
                items = line.split(',')
                if isint(items[1]):

                    if d_type == 4:
                        gender = items[d_type][0]
                        label = 0 if gender == 'M' else 1

                    elif d_type == 3:
                        age = items[d_type]
                        label = 0 if (int(age)<60) else 1

                    else :
                        if isint(items[d_type]):                        
                            label = self.get_label(int(items[d_type][0]))
                    
                    spin_images = torch.empty(0)

                    #ここで回転画像の追加
                    for i in range(n_per_unit):
                        image_name = items[1] + '_' + items[2] + '_' + '{:0=3}'.format(int(i)) + '.jpg'
                        image_name = os.path.join(root,image_name)
                        image_names.append(image_name)
                        item_indexes.append(item_index)
                        item_index += 1
                        labels.append(label)

        self.image_names = np.array(image_names)
        self.labels = np.array(labels)
        self.item_indexes = np.array(item_indexes)
        self.transform = transform
        print(len(self.image_names))

    def __getitem__(self, index):
        image_name = self.image_names[index]
        image = Image.open(image_name).convert('RGB')
        label = torch.eye(config.n_class)[self.labels[index]]
        item_index = self.item_indexes[index]
        if self.transform is not None:
            image = self.transform(image)

        return (image,torch.Tensor(label),item_index) if self.image_list_file==config.train_info_list else (image,torch.Tensor(label),image_name)

    def __len__(self):
        return len(self.image_names)

    def get_label(self, label_base):
        pass
'''

'''
class OCTspinDatasetBase(Dataset):
    def __init__(self, root, image_list_file,transform=None,n_per_unit=16,d_type=6):
        # まずはファイルを開いてID一覧を出力
        with open(image_list_file,"r") as f:
            lines = f.readlines()
        lines = [line.rstrip("\n") for line in lines] #右の改行文字の削除
        item_matrix = [line.split(',') for line in lines]

        self.transform = transform

        #画像の名前、ラベル、インデックスを記録する
        self.image_names = [os.path.join(root,item[1] + '_' + item[2] + '_' + '{:0=3}'.format(int(i)) + '.jpg')  for item in item_matrix for i in range(n_per_unit) if isint(item[1]) if isint(item[d_type])]
        self.images = [Image.open(os.path.join(root,item[1] + '_' + item[2] + '_' + '{:0=3}'.format(int(i)) + '.jpg')).convert('RGB') for item in item_matrix for i in range(n_per_unit) if isint(item[1]) if isint(item[d_type])]
        self.images = [self.transform(image) for image in self.images]
        self.labels = [self.get_label(int(item[d_type][0])) for item in item_matrix for i in range(n_per_unit) if isint(item[1]) if isint(item[d_type])]
        

        self.item_indexes = np.array(range(len(item_matrix)*n_per_unit))
        self.transform = transform
        self.image_list_file = image_list_file


    def __getitem__(self, index):
        image_name = self.image_names[index]
        #image = Image.open(image_name).convert('L')
        image = self.images[index]
        label = torch.eye(config.n_class)[self.labels[index]]
        item_index = self.item_indexes[index]
        #if self.transform is not None:
        #    image = self.transform(image)

        return (image,torch.Tensor(label),item_index) if self.image_list_file==config.train_info_list else (image,torch.Tensor(label),image_name)

    def __len__(self):
        return len(self.image_names)

    def pick_label(self, index):
        label = torch.eye(config.n_class)[self.labels[index]]
        return torch.Tensor(label)

'''


class OCTspinDatasetBase(Dataset):
    def __init__(self, root, image_list_file,transform=None,n_per_unit=16,d_type=6):
        # まずはファイルを開いてID一覧を出力
        with open(image_list_file,"r") as f:
            lines = f.readlines()
        lines = [line.rstrip("\n") for line in lines] #右の改行文字の削除
        item_matrix = [line.split(',') for line in lines]

        self.transform = transform
        self.images = torch.empty(0)

        #画像の名前、ラベル、インデックスを記録する
        self.image_names = [os.path.join(root,item[1] + '_' + item[2] + '_' + '{:0=3}'.format(int(0)) + '.jpg') for item in item_matrix if isint(item[1]) and isint(item[d_type]) ]
        labels = []

        #別々に扱う場合
        for item in item_matrix:
            spin_images = torch.empty(0)
            if isint(item[1]) and isint(item[d_type]):
                for i in range(n_per_unit):
                    image_name = item[1] + '_' + item[2] + '_' + '{:0=3}'.format(int(i)) + '.jpg'
                    subset_image = Image.open(os.path.join(root,image_name)).convert('L')
                    if transform is not None:
                        subset_image = self.transform(subset_image)
                    spin_images = torch.cat((spin_images,subset_image),0)
                spin_images = torch.reshape(spin_images,(1,n_per_unit,config.image_size,config.image_size))
                self.images = torch.cat((self.images,spin_images),0)
                label = self.get_label(int(item[d_type][0]))
                print(label)
                labels.append(label)

        self.labels = labels
        self.item_indexes = np.array(range(len(labels)))
        self.image_list_file = image_list_file


    def __getitem__(self, index):
        image_name = self.image_names[index]
        #image = Image.open(image_name).convert('L')
        image = self.images[index]
        label = torch.eye(config.n_class)[self.labels[index]]
        item_index = self.item_indexes[index]
        #if self.transform is not None:
        #    image = self.transform(image)

        return (image,torch.Tensor(label),item_index) if self.image_list_file==config.train_info_list else (image,torch.Tensor(label),image_name)

    def __len__(self):
        return len(self.labels)

    def pick_label(self, index):
        label = torch.eye(config.n_class)[self.labels[index]]
        return torch.Tensor(label)

        

# 症状なし:0 軽度:1 中度:2 重度:3と分類する。
class OCTspinDataset(OCTspinDatasetBase):
    def get_label(self, label_base):
        if label_base == 1:
            return 0
        elif label_base == 2 or label_base == 3:
            return 1
        else:
            #return 2
            return 1

def load_dataset(n_per_unit,d_type,preprocess):
    train_transform = \
        transforms.Compose([transforms.Resize(config.image_size),
                            transforms.CenterCrop(config.image_size),
                            transforms.ToTensor(),
                            transforms.Normalize((0.5, ),(0.5, )),
                            ])
    test_transform = \
        transforms.Compose([transforms.Resize(config.image_size),
                            transforms.CenterCrop(config.image_size),
                            transforms.ToTensor(),
                            transforms.Normalize((0.5, ),(0.5, )),
                            ])
    
    dataset = {}
    if n_per_unit == 1:
        dataset['train'] = \
            OCThorizontalDataset(root=os.path.join(config.data_root,preprocess),
                                    image_list_file=config.train_info_list,
                                    transform=train_transform,n_per_unit = n_per_unit,d_type=d_type)

        dataset['test'] = \
            OCThorizontalDataset(root=config.data_root,
                                    image_list_file=config.test_info_list,
                                    transform=test_transform,n_per_unit = n_per_unit,d_type=d_type)
    elif n_per_unit == 16:
        dataset['train'] = \
            OCTspinDataset(root=config.data_root,
                                    image_list_file=config.train_info_list,
                                    transform=train_transform,n_per_unit = n_per_unit,d_type=d_type)
        dataset['test'] = \
            OCTspinDataset(root=config.data_root,
                                    image_list_file=config.test_info_list,
                                    transform=test_transform,n_per_unit = n_per_unit,d_type=d_type)


    return dataset

    '''
    CV実装のため、データセットのみの実装
    dataloader = {}
    
    dataloader['train'] = \
        torch.utils.data.DataLoader(train_dataset,
                                    batch_size=batch_size,
                                    num_workers=0)
    dataloader['test'] = \
        torch.utils.data.DataLoader(test_dataset,
                                    batch_size=batch_size,
                                    num_workers=0)
    return dataloader
    '''


    '''
    CV実装のため、データセットのみの実装
    dataloader = {}
    
    dataloader['train'] = \
        torch.utils.data.DataLoader(train_dataset,
                                    batch_size=batch_size,
                                    num_workers=0)
    dataloader['test'] = \
        torch.utils.data.DataLoader(test_dataset,
                                    batch_size=batch_size,
                                    num_workers=0)
    return dataloader
    '''

