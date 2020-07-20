#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2019-2020 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr
# Juan Manuel CORIA - https://juanmc2005.github.io

from typing import Union, Dict
from argparse import Namespace
import math
import torch
from pytorch_metric_learning.losses import ArcFaceLoss
from .base import BaseSpeakerEmbedding


class SpeakerEmbeddingArcFaceLoss(BaseSpeakerEmbedding):
    def setup_loss(self):

        if "margin" not in self.hparams:
            self.hparams.margin = 0.2

        num_classes = len(self.hparams.classes)
        if "scale" not in self.hparams:
            # Use scaling initialization trick from AdaCos
            # Reference: https://arxiv.org/abs/1905.00292
            self.hparams.scale = math.sqrt(2) * math.log(num_classes - 1)

        self.arcface_loss = ArcFaceLoss(
            margin=self.hparams.margin,
            scale=self.hparams.scale,
            num_classes=num_classes,
            embedding_size=self.model.dimension,
        )

    def get_loss(self):
        return self.arcface_loss
