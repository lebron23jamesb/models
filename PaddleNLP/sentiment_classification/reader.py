#   Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Senta Reader
"""

import os
import types
import csv
import numpy as np
from utils import load_vocab
from utils import data_reader

import paddle
import paddle.fluid as fluid


class SentaProcessor(object):
    """
    Processor class for data convertors for senta
    """

    def __init__(self, data_dir, vocab_path, random_seed=None):
        self.data_dir = data_dir
        self.vocab = load_vocab(vocab_path)
        self.num_examples = {"train": -1, "dev": -1, "infer": -1}
        np.random.seed(random_seed)

    def get_train_examples(self, data_dir, epoch):
        """
        Load training examples
        """
        return data_reader((self.data_dir + "/train.tsv"), self.vocab,
                           self.num_examples, "train", epoch)

    def get_dev_examples(self, data_dir, epoch):
        """
        Load dev examples
        """
        return data_reader((self.data_dir + "/dev.tsv"), self.vocab,
                           self.num_examples, "dev", epoch)

    def get_test_examples(self, data_dir, epoch):
        """
        Load test examples
        """
        return data_reader((self.data_dir + "/test.tsv"), self.vocab,
                           self.num_examples, "infer", epoch)

    def get_labels(self):
        """
        Return Labels
        """
        return ["0", "1"]

    def get_num_examples(self, phase):
        """
        Return num of examples in train, dev, test set
        """
        if phase not in ['train', 'dev', 'infer']:
            raise ValueError(
                "Unknown phase, which should be in ['train', 'dev', 'infer'].")
        return self.num_examples[phase]

    def get_train_progress(self):
        """
        Get train progress
        """
        return self.current_train_example, self.current_train_epoch

    def data_generator(self, batch_size, phase='train', epoch=1, shuffle=True):
        """
        Generate data for train, dev or infer
        """
        if phase == "train":
            return paddle.batch(
                self.get_train_examples(self.data_dir, epoch), batch_size)
        elif phase == "dev":
            return paddle.batch(
                self.get_dev_examples(self.data_dir, epoch), batch_size)
        elif phase == "infer":
            return paddle.batch(
                self.get_test_examples(self.data_dir, epoch), batch_size)
        else:
            raise ValueError(
                "Unknown phase, which should be in ['train', 'dev', 'infer'].")