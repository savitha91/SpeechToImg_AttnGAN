from __future__ import print_function

import sys
import torch
import time
import numpy as np
from PIL import Image
import torch.onnx
from torch.autograd import Variable
from config import cfg
from AttnGan.miscc.utils import build_super_images2
from AttnGan.model import RNN_ENCODER, G_NET

if sys.version_info[0] == 2:
    import cPickle as pickle
else:
    import pickle

#from werkzeug.contrib.cache import SimpleCache
#cache = SimpleCache()

def vectorize_caption(wordtoix, caption, copies=2):
    # create caption vector
    tokens = caption.split(' ')
    cap_v = []
    for t in tokens:
        t = t.strip().encode('ascii', 'ignore').decode('ascii')
        if len(t) > 0 and t in wordtoix:
            cap_v.append(wordtoix[t])

    # expected state for single generation
    captions = np.zeros((copies, len(cap_v)))
    for i in range(copies):
        captions[i,:] = np.array(cap_v)
    cap_lens = np.zeros(copies) + len(cap_v)

    #print(captions.astype(int), cap_lens.astype(int))
    #captions, cap_lens = np.array([cap_v, cap_v]), np.array([len(cap_v), len(cap_v)])
    #print(captions, cap_lens)
    #return captions, cap_lens

    return captions.astype(int), cap_lens.astype(int)

def generate(caption, wordtoix, ixtoword, text_encoder, netG, copies=2):
    # load word vector
    captions, cap_lens  = vectorize_caption(wordtoix, caption, copies)
    n_words = len(wordtoix)

    # only one to generate
    batch_size = captions.shape[0]

    nz = cfg.GAN.Z_DIM
    with torch.no_grad():
        captions = Variable(torch.from_numpy(captions))
        cap_lens = Variable(torch.from_numpy(cap_lens))
        noise = Variable(torch.FloatTensor(batch_size, nz))

    if cfg.CUDA:
        captions = captions.cuda()
        cap_lens = cap_lens.cuda()
        noise = noise.cuda()



    #######################################################
    # (1) Extract text embeddings
    #######################################################
    hidden = text_encoder.init_hidden(batch_size)
    words_embs, sent_emb = text_encoder(captions, cap_lens, hidden)
    mask = (captions == 0)


    #######################################################
    # (2) Generate fake images
    #######################################################
    noise.data.normal_(0, 1)
    fake_imgs, attention_maps, _, _ = netG(noise, sent_emb, words_embs, mask)

    # G attention
    cap_lens_np = cap_lens.cpu().data.numpy()

    # storing to blob storage
    full_path =cfg.OUTPUT_IMG_PATH
    # only look at first one
    #j = 0
    for j in range(batch_size):
        save_name = '%s/%d_s_%d' % (full_path, j, j)
        for k in range(len(fake_imgs)):
            im = fake_imgs[k][j].data.cpu().numpy()
            im = (im + 1.0) * 127.5
            im = im.astype(np.uint8)
            im = np.transpose(im, (1, 2, 0))
            im = Image.fromarray(im)
            fullpath = '%s_g%d.png' % (save_name, k)
            im.save(fullpath)

            if copies == 2:
                for k in range(len(attention_maps)):
                #if False:
                    if len(fake_imgs) > 1:
                        im = fake_imgs[k + 1].detach().cpu()
                    else:
                        im = fake_imgs[0].detach().cpu()

                    attn_maps = attention_maps[k]
                    att_sze = attn_maps.size(2)

                    img_set, sentences = \
                        build_super_images2(im[j].unsqueeze(0),
                                            captions[j].unsqueeze(0),
                                            [cap_lens_np[j]], ixtoword,
                                            [attn_maps[j]], att_sze)

                    if img_set is not None:
                        im = Image.fromarray(img_set)
                        fullpath = '%s_a%d.png' % (save_name, k)
                        im.save(fullpath)
        if copies == 2:
            break


def word_index():
    #ixtoword = cache.get('ixtoword')
    #wordtoix = cache.get('wordtoix')
    if True:
        #print("ix and word not cached")
        # load word to index dictionary
        x = pickle.load(open(cfg.CAPTIONFILE, 'rb'))
        ixtoword = x[2]
        wordtoix = x[3]
        del x
        #cache.set('ixtoword', ixtoword, timeout=60 * 60 * 24)
        #cache.set('wordtoix', wordtoix, timeout=60 * 60 * 24)

    return wordtoix, ixtoword

def models(word_len):
    #print(word_len)
    #text_encoder = cache.get('text_encoder')
    if True:
        #print("text_encoder not cached")
        text_encoder = RNN_ENCODER(word_len, nhidden=cfg.TEXT.EMBEDDING_DIM)
        state_dict = torch.load(cfg.TRAIN.NET_E, map_location=lambda storage, loc: storage)
        text_encoder.load_state_dict(state_dict)
        if cfg.CUDA:
            text_encoder.cuda()
        text_encoder.eval()
        #cache.set('text_encoder', text_encoder, timeout=60 * 60 * 24)

    #netG = cache.get('netG')
    if True:
        #print("netG not cached")
        netG = G_NET()
        # map_location=lambda storage, loc: storage  -> Load all weights trained on GPU to CPU
        state_dict = torch.load(cfg.TRAIN.NET_G, map_location=lambda storage, loc: storage)
        netG.load_state_dict(state_dict)
        if cfg.CUDA:
            netG.cuda()
        netG.eval()
        #cache.set('netG', netG, timeout=60 * 60 * 24)

    return text_encoder, netG

def eval(caption):
    # load word dictionaries
    wordtoix, ixtoword = word_index()
    # lead models
    text_encoder, netG = models(len(wordtoix))
    # load blob service

    t0 = time.time()
    urls = generate(caption, wordtoix, ixtoword, text_encoder, netG)
    t1 = time.time()

    response = {
        'small': urls[0],
        'medium': urls[1],
        'large': urls[2],
        'map1': urls[3],
        'map2': urls[4],
        'caption': caption,
        'elapsed': t1 - t0
    }

    return response

if __name__ == "__main__":
    caption = "the bird has a yellow crown and a black eyering that is round"

    # load configuration
    #cfg_from_file('eval_bird.yml')
    # load word dictionaries
    wordtoix, ixtoword = word_index()
    # lead models
    text_encoder, netG = models(len(wordtoix))
    # load blob service

    t0 = time.time()
    urls = generate(caption, wordtoix, ixtoword, text_encoder, netG)
    t1 = time.time()
    print(t1-t0)
    print(urls)
