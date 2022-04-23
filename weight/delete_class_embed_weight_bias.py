import torch
import os

source = 'detr-r101-2c7b67e5.pth'
target = 'detr-r101-no-class-embed.pth'

if not os.path.exists(source):
    os.system(f'wget https://dl.fbaipublicfiles.com/detr/{source}')

checkpoint = torch.load(source)
del checkpoint['model']['class_embed.weight']
del checkpoint['model']['class_embed.bias']
torch.save(checkpoint, target)
print('Done.')