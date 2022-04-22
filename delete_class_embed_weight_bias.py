import torch
checkpoint = torch.load('detr-r101-2c7b67e5.pth')
del checkpoint['model']['class_embed.weight']
del checkpoint['model']['class_embed.bias']
torch.save(checkpoint, 'detr-r101-no-class-embed.pth')
