from numpy import max as nmax
from numpy import *
from scipy.fftpack import fft,ifft
from scipy.io import wavfile
import matplotlib.pyplot as plt
import warnings
import json
import os
from dwnld import downloadAudio
from play import record, replay
import time

warnings.simplefilter("ignore")


def shazam(filename,samplespersec = 30):
    rate,x = wavfile.read(filename)
    n = x.shape[0]
    if len(x.shape) == 2:
        x = x.sum(axis=1)/2
    
    sections = []
    sec = float(samplespersec)
    dt = int(rate/sec)

    f = []
    width = 10*dt
    han = hanning(width)
    for j in range(0,len(x)-width,dt):
        
        i = x[j:j+width]
        
        frr = abs(fft(i*han))

        mid = len(frr)/2
        
        v = linspace(0,mid,16)
        v = v.astype(int)

        f.append([
            argmax((frr[v[0]:v[1]]))+v[0],
            argmax((frr[v[1]:v[3]]))+v[1],
            argmax((frr[v[3]:v[6]]))+v[3],
            argmax((frr[v[6]:v[10]]))+v[6],
            argmax((frr[v[10]:v[15]]))+v[10]
            ])

    return array(f)

def hasher(sound, n, ac=3):
    anchor = float(sound[n][2])
    hsh =   round(sound[n+1][1]/anchor,ac)*10**(ac*3+2)+\
            round(sound[n+1][3]/anchor,ac)*10**(ac*2+1)+\
            round(sound[n+1][2]/anchor,ac)*10**ac
    return hsh

def compiler(sound):
    data = []
    for i in range(1,len(sound)-30):
        h = hasher(sound, i)
        data.append(int(h))
    return array(data[:])

def matcher(clip_data, full_data):
    master = []
    m = len(clip_data)
    dm = m
    
    n = len(full_data)
    l = n-(n%m)
    dl = int(m/10)
    
    for j in range(0, n-m, dl):
        count = 0
 
        bl = 0
        full_test = full_data[j:j+m]
        for i in range(0,m,dm):
            bl = in1d(clip_data[i:i+dm],full_test[i:i+dm])
            count += len(bl[bl==True])
        master.append(count)

    return max(master)/float(m), m, n
    
def evaluate(filenames, full_filename):

    full_data = hashRecall(full_filename,'clips')
    print "Done."
    print "Comparing to " + full_filename + "..."
    print ""

    results = ["null",0.]
    for filename in filenames:
        clip_data = hashRecall(filename,'full')
        count, m, n = matcher(full_data, clip_data)
        count = int((count*1000))/10.

        print "Results:\t" + filename
        print "Percent Match:\t" + str(count)+'%'
        print ""
        if count > results[1]:
            results = [filename,count]
    print "Tested File: " + full_filename
    print "Best Match:  " + results[0]
    print ":::::::::::::::::::::::::::::::::::::"
    print ""

def hashRecall(filename, drc):
    if os.path.isfile('hash\\' + filename+'_hash.txt'):
        print "Retrieving " + filename
        f = open('hash\\' + filename+'_hash.txt')
        data = json.load(f)
        f.close()
        return array(data)
    else:
        print "Hashing " + filename
        f = open('hash\\' + filename+'_hash.txt', 'w')
        full = shazam(drc+'\\'+filename)
        full_data = compiler(full).tolist()
        json.dump(full_data, f)
        f.close()
        return array(full_data)
        

def liveTest(url, name):
    print name
    downloadAudio(url, name)
    while True:
        raw_input('Press Enter when ready to record.')
        print "Recording in..."
        time.sleep(1)
        print "3"
        time.sleep(1)
        print "2"
        time.sleep(1)
        print "1"
        time.sleep(1)
        print "Recording..."
        record(name)
        if raw_input("Play?[Y/y]: ") in ['Y','y']:
            replay(name)
        if raw_input("Again?[Y/y]:") not in ['Y','y']:
            break

# Testing
    
name = 'Cannonball'
url  = 'https://www.youtube.com/watch?v=fxvkI9MTQw4'

test_names = ['Falling_For_You',
              'Hang_Me_Up_To_Dry',
              'Here_Comes_Your_Man',
              'Hey',
              'I_Get_Around',
              'Three_of_a_Perfect_Pair']
clip_names = []
full_names = []

for content in os.listdir("clips"):
        clip_names.append(content)

for content in os.listdir("full"):
        full_names.append(content)

evaluate(full_names,name+'_Clip.wav')


for name in test_names:
    evaluate(full_names,name+'_Clip.wav')
    raw_input("Next?")

