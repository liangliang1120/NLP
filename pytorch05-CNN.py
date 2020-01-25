# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 17:27:40 2020

@author: us
"""

import torch 
from torch.utils import data # 获取迭代数据
from torch.autograd import Variable # 获取变量
import torchvision
from torchvision.datasets import mnist # 获取数据集
import matplotlib.pyplot as plt


'''
2.1 获取数据集，并对数据集进行预处理

（1）对原有数据转成Tensor类型

（2）用平均值和标准偏差归一化张量图像
'''
# 数据集的预处理
data_tf = torchvision.transforms.Compose(
    [
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize([0.5],[0.5])
    ]
)



data_path = r'./MNIST_DATA_PyTorch'

# 本地没有数据集，先下载
# train_data = mnist.MNIST(data_path,train=True,transform=data_tf,download=True)

# 获取数据集
train_data = mnist.MNIST(data_path,train=True,transform=data_tf,download=False)
test_data = mnist.MNIST(data_path,train=False,transform=data_tf,download=False)


# 2.2 获取迭代数据
train_loader = data.DataLoader(train_data,batch_size=128,shuffle=True)
test_loader = data.DataLoader(test_data,batch_size=100,shuffle=True)


# 3. 定义网络结构
# 定义网络结构
class CNNnet(torch.nn.Module):
    def __init__(self):
        super(CNNnet,self).__init__()
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=1,
                            out_channels=16,
                            kernel_size=3,
                            stride=2,
                            padding=1),
            torch.nn.BatchNorm2d(16),
            torch.nn.ReLU()
        )
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv2d(16,32,3,2,1),
            torch.nn.BatchNorm2d(32),
            torch.nn.ReLU()
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(32,64,3,2,1),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU()
        )
        self.conv4 = torch.nn.Sequential(
            torch.nn.Conv2d(64,64,2,2,0),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU()
        )
        self.mlp1 = torch.nn.Linear(2*2*64,100)
        self.mlp2 = torch.nn.Linear(100,10)
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.mlp1(x.view(x.size(0),-1))
        x = self.mlp2(x)
        return x
model = CNNnet()
print(model)

'''
4. 定义损失和优化器

（1）使用交叉熵损失

（2）使用Adam优化器
'''
loss_func = torch.nn.CrossEntropyLoss()
opt = torch.optim.Adam(model.parameters(),lr=0.001)

# 5. 训练网络
loss_count = []
for epoch in range(2):
    for i,(x,y) in enumerate(train_loader):
        batch_x = Variable(x) # torch.Size([128, 1, 28, 28])
        batch_y = Variable(y) # torch.Size([128])
        # 获取最后输出
        out = model(batch_x) # torch.Size([128,10])
        # 获取损失
        loss = loss_func(out,batch_y)
        # 使用优化器优化损失
        opt.zero_grad()  # 清空上一步残余更新参数值
        loss.backward() # 误差反向传播，计算参数更新值
        opt.step() # 将参数更新值施加到net的parmeters上
        if i%20 == 0:
            loss_count.append(loss)
            print('{}:\t'.format(i), loss.item())
            # torch.save(model,r'C:\Users\liev\Desktop\myproject\yin_test\log_CNN')
        if i % 100 == 0:
            for a,b in test_loader:
                test_x = Variable(a)
                test_y = Variable(b)
                out = model(test_x)
                # print('test_out:\t',torch.max(out,1)[1])
                # print('test_y:\t',test_y)
                accuracy = torch.max(out,1)[1].numpy() == test_y.numpy()
                print('accuracy:\t',accuracy.mean())
                break
plt.figure('PyTorch_CNN_Loss')
plt.plot(loss_count,label='Loss')
plt.legend()
plt.show()






'''
0:       2.2166190147399902
accuracy:        0.31
20:      0.6877725720405579
40:      0.2734276056289673
60:      0.35138726234436035
80:      0.1277933120727539
100:     0.11527200043201447
accuracy:        0.93
120:     0.2288316786289215
140:     0.12041088193655014
160:     0.13211597502231598
180:     0.10686729103326797
200:     0.033652205020189285
accuracy:        0.98
220:     0.11361207813024521
240:     0.11988528817892075
260:     0.04487280175089836
280:     0.11504130810499191
300:     0.04793582856655121
accuracy:        0.98
320:     0.04414645954966545
340:     0.09040714055299759
360:     0.06945277750492096
380:     0.028021585196256638
400:     0.1156919002532959
accuracy:        0.99
420:     0.1104198694229126
440:     0.10534176975488663
460:     0.10244958847761154
0:       0.04450759291648865
accuracy:        1.0
20:      0.06610526144504547
40:      0.06480401009321213
60:      0.03039785660803318
80:      0.1288413405418396
100:     0.03308161348104477
accuracy:        0.99
120:     0.02228604629635811
140:     0.026129387319087982
160:     0.03116900846362114
180:     0.026287615299224854
200:     0.09807232767343521
accuracy:        1.0
220:     0.04609508439898491
240:     0.06488360464572906
260:     0.04470324516296387
280:     0.09226852655410767
300:     0.04389720410108566
accuracy:        0.97
320:     0.05493634566664696
340:     0.08741962164640427
360:     0.021164508536458015
380:     0.011999910697340965
400:     0.09000810980796814
accuracy:        1.0
420:     0.040731098502874374
440:     0.08093228936195374
460:     0.024273447692394257


原文链接：https://blog.csdn.net/qq_34714751/article/details/85610966
'''



















