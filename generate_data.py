import os
import glob
import PIL
import h5py
import PIL.Image as Image
import numpy as np
import scipy.io as sio
import tensorflow as tf

def data_augmentation(label, mode=0):

    if mode == 0:
        # original
        return label
    elif mode == 1:
        # flip up and down
        return np.flipud(label)
    elif mode == 2:
        # rotate counterwise 90 degree
        return np.rot90(label)
    elif mode == 3:
        # rotate 90 degree and flip up and down
        return np.flipud(np.rot90(label))
    elif mode == 4:
        # rotate 180 degree
        return np.rot90(label, k=2)
    elif mode == 5:
        # rotate 180 degree and flip
        return np.flipud(np.rot90(label, k=2))
    elif mode == 6:
        # rotate 270 degree
        return np.rot90(label, k=3)
    elif mode == 7:
        # rotate 270 degree and flip
        return np.flipud(np.rot90(label, k=3))

def Im2Patch(img, win, stride=1):  # Based on code written by Shuhang Gu (cssgu@comp.polyu.edu.hk)
    k = 0
    endw = img.shape[0]
    endh = img.shape[1]
    if endw < win or endh < win:
        return None, None
    patch = img[0:endw - win + 0 + 1:stride, 0:endh - win + 0 + 1:stride]
    TotalPatNum = patch.shape[0] * patch.shape[1]
    # TotalPatNum = (img.shape[0]-win+1)*(img.shape[1]-win+1)
    Y = np.zeros([win * win, TotalPatNum])
    for i in range(win):
        for j in range(win):
            patch = img[i:endw - win + i + 1:stride, j:endh - win + j + 1:stride]
            Y[k,:] = np.array(patch[:]).reshape(TotalPatNum)
            k = k + 1

    return Y.reshape([win, win, 1, TotalPatNum])

data_path = 'Train400'
out_dir = 'data/'
batchSize = 128
patchsize = 40
# filename = 'imdb_'+str(patchsize)+'_'+str(batchSize)+'_V1.mat'
tfrecords_filename = 'imdb_'+str(patchsize)+'_'+str(batchSize)+'_V1.tfrecords'
stride = 10
count = 0
ext = '*.png'
scales = [1, 0.9, 0.8, 0.7]
data_dir = os.path.join(os.getcwd(), data_path)
data = glob.glob(os.path.join(data_dir, ext))
print(len(data))
for i in range(len(data)):
    # print(i)
    img = Image.open(data[i]).convert('L')
    for sc in range(len(scales)):
        newsize = (int(img.size[0] * scales[sc]), int(img.size[1] * scales[sc]))
        img = img.resize(newsize, resample=PIL.Image.BICUBIC)
        label_ = np.array(img, dtype='uint8')
        h = label_.shape[0]
        w = label_.shape[1]
        for x in range(0, h-patchsize+2, stride):
            for y in range(0, w-patchsize+2, stride):
                count = count + 1
print(count)
TotalNum = batchSize*(count//batchSize if count//batchSize==0 else count//batchSize + 1)
print(TotalNum)
sub_label_sequence = np.zeros([patchsize,patchsize,1,TotalNum], dtype=np.uint8)
# sub_label_sequence = []
count = 0
for i in range(len(data)):
    print(i)
    img = Image.open(data[i]).convert('L')
    for sc in range(len(scales)):
        newsize = (int(img.size[0] * scales[sc]), int(img.size[1] * scales[sc]))
        img = img.resize(newsize, resample=PIL.Image.BICUBIC)
        label_ = np.array(img, dtype='uint8')
        # image_aug = data_augmentation(label_, 0).astype(np.float32)
        # label_ = image_aug / 255.0
        # label_patches = Im2Patch(label_, patchsize, stride=stride)
        h = label_.shape[0]
        w = label_.shape[1]
        for x in range(0, h-patchsize+2, stride):
            for y in range(0, w-patchsize+1, stride):
                p = label_[x:x+patchsize, y:y+patchsize]
                size_p = p.shape
                sub_label_sequence[0:size_p[0], 0:size_p[1], :, count:count + 1] = np.reshape(p,
                                           [size_p[0], size_p[1], 1, 1])
                # sub_label_sequence.append(np.reshape(p, [size_p[0], size_p[1], 1]).astype(np.float32))
                count = count + 1

        # if i == 0:
        #     sub_label_sequence = label_patches
        # else:
        #     sub_label_sequence = np.append(sub_label_sequence, label_patches, axis=3)
print(sub_label_sequence.shape)
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
writer = tf.python_io.TFRecordWriter(out_dir + tfrecords_filename)
# inputs = tf.train.Example(features=tf.train.Features(
#         feature={'inputs': tf.train.Feature(float_list=tf.train.FloatList(value=sub_label_sequence))}))
# writer.write(inputs.SerializeToString())

# for img in sub_label_sequence:
for ind in range(sub_label_sequence.shape[3]):
    img_raw = np.reshape(sub_label_sequence[:, :, :, ind], [patchsize, patchsize, 1]).tostring()
    inputs = tf.train.Example(features=tf.train.Features(
        feature={'inputs': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))}))
    writer.write(inputs.SerializeToString())
    # for i in range(patchsize):
    #     for j in range(patchsize):
    #         inputs = tf.train.Example(features=tf.train.Features(
    #             feature={'inputs': tf.train.Feature(float_list=tf.train.FloatList(value=[img_raw[i,j,0]]))}))
    #         writer.write(inputs.SerializeToString())
    # inputs = tf.train.Example(features=tf.train.Features(
    #     feature={'inputs': tf.train.Feature(float_list=tf.train.FloatList(value=[img_raw[:]]))}))
    # writer.write(inputs.SerializeToString())

writer.close()
# sio.savemat(out_dir + filename, {'inputs':sub_label_sequence})

