import torchvision.transforms as T
import torch
import albumentations as A
from albumentations.core.transforms_interface import ImageOnlyTransform  
from albumentations.pytorch import ToTensorV2
import numpy as np


def get_train_transform(resize_crop_size = 640,
                    mean = [0.485, 0.456, 0.406],
                    std = [0.229, 0.224, 0.225],
                  ):

    augmentation = A.Compose(
        [
            # A.RandomResizedCrop(height=resize_crop_size, width=resize_crop_size),
            A.RandomBrightnessContrast(),
            A.HorizontalFlip(),
            A.VerticalFlip(),
            A.GaussianBlur(),
            A.Normalize(mean=mean, std=std),
            ToTensorV2(),
        ]
    )

    def transform(sample):
        image = np.transpose(sample["image"], (1, 2, 0))
        point = sample["point"]

        image = augmentation(image=image)["image"]
        point = coordinate_jitter(point)

        return dict(image=image, point=point)

    return transform


def get_s2_train_transform(resize_crop_size = 640):
    augmentation = T.Compose([
        # T.RandomCrop(resize_crop_size),
        T.RandomHorizontalFlip(),
        T.RandomVerticalFlip(),
        T.GaussianBlur(3),
    ])

    def transform(sample):
        image = sample["image"] / 255.0
        point = sample["point"]
        image = torch.tensor(image)
        image = augmentation(image)
        point = coordinate_jitter(point)
        return dict(image=image, point=point)

    return transform

def get_pretrained_s2_train_transform(resize_crop_size = 256):
    augmentation = T.Compose([
        T.RandomCrop(resize_crop_size),
        T.RandomHorizontalFlip(),
        T.RandomVerticalFlip(),
        T.GaussianBlur(3),
    ])

    def transform(sample):
        image = sample["image"] / 255.0
        point = sample["point"]

        # B10 = np.zeros((1, *image.shape[1:]), dtype=image.dtype)
        # image = np.concatenate([image[:10], B10, image[10:]], axis=0)
        image = torch.tensor(image)

        image = augmentation(image)

        point = coordinate_jitter(point)

        return dict(image=image, point=point)

    return transform

def coordinate_jitter(
        point,
        radius=0.01 # approximately 1 km
    ):
    return point + torch.rand(point.shape) * radius