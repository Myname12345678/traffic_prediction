# coding=utf8

""" Setup an laboratory which contains train/validation/test datasets
&& sample each of them.
"""
import os
import os.path
import logging
import glob
import numpy as np
import shutil


class Lab(object):
    """ """
    def __init__(self, root_path, suffix, sample_ratio, create_when_not_exist=True):
        self._root_path = root_path
        if not os.path.exists(self._root_path) and create_when_not_exist:
            os.makedirs(self._root_path)
        
        self._suffix = suffix
        self._sample_ratio = sample_ratio
        
        logging.info('the lab is built at: ' + self._root_path)
       
    
    def _make_lab_dirs(self):
        dirs = [
            '{}/train'.format(self._root_path), 
            '{}/validation'.format(self._root_path), 
            '{}/test'.format(self._root_path), 
            '{}/sample/train'.format(self._root_path), 
            '{}/sample/validation'.format(self._root_path), 
            '{}/sample/test'.format(self._root_path)
        ]
        
        # recreate all these dirs
        for d in dirs:
            logging.info('recreate ' + d)
            if os.path.exists(d):
                shutil.rmtree(d)
                
            os.makedirs(d)
    
    
    def _sample(self):
        g = glob.glob('{}/train/*.{}'.format(self._root_path, self._suffix))
        shuffled = np.random.permutation(g)
        sample_size = int(len(shuffled) * self._sample_ratio)
        logging.info('taking {} as train sample'.format(sample_size))
        for i in range(0, sample_size):
            # logging.info('move {}=>{}/sample/train'.format(shuffled[i], self._root_path))
            shutil.move(shuffled[i], '{}/sample/train'.format(self._root_path))
            
        g = glob.glob('{}/validation/*.{}'.format(self._root_path, self._suffix))
        shuffled = np.random.permutation(g)
        sample_size = int(len(shuffled) * self._sample_ratio)
        logging.info('taking {} as validation sample'.format(sample_size))
        for i in range(0, sample_size):
            # logging.info('move {}=>{}/sample/validation'.format(shuffled[i], self._root_path))
            shutil.move(shuffled[i], '{}/sample/validation'.format(self._root_path))
            
        g = glob.glob('{}/test/*.{}'.format(self._root_path, self._suffix))
        shuffled = np.random.permutation(g)
        sample_size = int(len(shuffled) * self._sample_ratio)
        logging.info('taking {} as test sample'.format(sample_size))
        for i in range(0, sample_size):
            # logging.info('move {}=>{}/sample/test'.format(shuffled[i], self._root_path))
            shutil.move(shuffled[i], '{}/sample/test'.format(self._root_path))
        

    def setup_from_single_dataset(self, from_path, train_set_ratio, valid_set_ratio):
        """ separate the given dataset into train/validation/test sets
        && sample each of them """
        self._make_lab_dirs()
        
        g = glob.glob('{}/{}/*.{}'.format(self._root_path, from_path, self._suffix))
        total_size = len(g)
        train_set_size = int(total_size * train_set_ratio)
        valid_set_size = int(total_size * valid_set_ratio)
        test_set_size = total_size - train_set_size - valid_set_size
        
        logging.info('copying {} as train set, {} as valid set, {} as test set'.format(
            train_set_size, valid_set_size, test_set_size))
        
        shuffled = np.random.permutation(g)
        for i in range(0, total_size):
            filename = shuffled[i].split('/')[-1]
            if i < train_set_size:
                # logging.info('copy {}=>{}'.format(shuffled[i], '{}/train/{}'.format(self._root_path, filename)))
                shutil.copyfile(shuffled[i], '{}/train/{}'.format(self._root_path, filename))
            elif i < train_set_size + valid_set_size:
                # logging.info('copy {}=>{}'.format(shuffled[i], '{}/validation/{}'.format(self._root_path, filename)))
                shutil.copyfile(shuffled[i], '{}/validation/{}'.format(self._root_path, filename))
            else:
                # logging.info('copy {}=>{}'.format(shuffled[i], '{}/test/{}'.format(self._root_path, filename)))
                shutil.copyfile(shuffled[i], '{}/test/{}'.format(self._root_path, filename))
    
        self._sample()
        
        
    def setup_from_train_test_set(self, from_path, train_set_ratio, valid_set_ratio):
        """ separate the given train dataset into train/validation sets, take the given test set, 
        && sample each of them """
        self._make_lab_dirs()
        
        g = glob.glob('{}/{}/train/*.{}'.format(self._root_path, from_path, self._suffix))
        total_size = len(g)
        train_set_size = int(total_size * train_set_ratio)
        valid_set_size = total_size - train_set_size
        g_test = glob.glob('{}/{}/test/*.{}'.format(self._root_path, from_path, self._suffix))
        test_set_size = len(g_test)
        
        logging.info('copying {} as train set, {} as valid set, {} as test set'.format(
            train_set_size, valid_set_size, test_set_size))
        
        shuffled = np.random.permutation(g)
        for i in range(0, total_size):
            filename = shuffled[i].split('/')[-1]
            if i < train_set_size:
                # logging.info('copy {}=>{}'.format(shuffled[i], '{}/train/{}'.format(self._root_path, filename)))
                shutil.copyfile(shuffled[i], '{}/train/{}'.format(self._root_path, filename))
            else:
                # logging.info('copy {}=>{}'.format(shuffled[i], '{}/validation/{}'.format(self._root_path, filename)))
                shutil.copyfile(shuffled[i], '{}/validation/{}'.format(self._root_path, filename))
        
        shuffled = np.random.permutation(g_test)
        for i in range(0, test_set_size):
            filename = shuffled[i].split('/')[-1]
            shutil.copyfile(shuffled[i], '{}/test/{}'.format(self._root_path, filename))
                
        self._sample()
        
        