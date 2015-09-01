import sys
import re
import perceplearn
import os

def createtempfile(input, output):
    feature = {}
    for line in input:
        list = line.split()
        i = 0
        for item in list:
            cls = item.split('/')[-1]
            current = ''.join(item.split('/')[0:-2])
            wshape = re.sub(r'[A-Z]', 'A', current)
            wshape = re.sub(r'[a-z]', 'a', wshape)
            wshape = re.sub(r'[0-9]', '9', wshape)
            wshape = re.sub(r'[^A-Za-z0-9]', '-', wshape)
            wshape = re.sub(r'A+', 'A', wshape)
            wshape = re.sub(r'a+', 'a', wshape)
            wshape = re.sub(r'9+', '9', wshape)
            wshape = re.sub(r'-+', '-', wshape)
            if i == 0:
                feature[0] = 'BOS_WORD'
                feature[1] =  'BOS_TAG'
            else:
                feature[0] = 'PREV_WORD_'+ ''.join(list[i-1].split('/')[0:-2])
                feature[1] = 'PREV_TAG_'+list[i-1].split('/')[-2]
            feature[2] = 'CURR_WORD_'+ current
            feature[3] = 'CURR_TAG_'+item.split('/')[-2]
            if i == len(list) - 1:
                feature[4] = 'EOS_WORD'
                feature[5] = 'EOS_TAG'
            else:
                feature[4] = 'NEXT_WORD_'+''.join(list[i+1].split('/')[0:-2])
                feature[5] = 'NEXT_TAG_'+list[i+1].split('/')[-2]
            feature[6] = 'WSHAPE_'+wshape
            if len(current) < 3:
                feature[7] = 'SUFFIX3_'
            else:
                feature[7] = 'SUFFIX3_'+current[-3:]
            if len(current) < 2:
                feature[8] = 'SUFFIX2_'
            else:
                feature[8] = 'SUFFIX2_'+current[-2:]
            output.write(cls + ' ' + feature[0] + ' '+ feature[1] + ' ' + feature[2]+' '+feature[3] + ' '+ feature[4] + ' '+ feature[5]+' '+feature[6]+' '+ feature[7]+' '+feature[8]+'\n')
            i=i+1
            
def main(argv):
    if len(argv) == 2:
        if not os.path.exists(argv[0]) :
            print(argv[0] + ' does not exist')
            sys.exit()
        if not os.path.isfile(argv[0]):
            print(argv[0] + ' not a file')
            sys.exit()
        args = ['neresptrain'] + [argv[1]]
        train = open(argv[0], 'r', errors='ignore')
        train_temp = open('neresptrain', 'w')
        createtempfile(train, train_temp)
        perceplearn.main(args)
        os.remove('neresptrain')
    elif len(argv) == 4 and argv[2]  == '-h':
        if not os.path.exists(argv[0]) :
            print(argv[0] + ' does not exist')
            sys.exit()
        if not os.path.isfile(argv[0]):
            print(argv[0] + ' not a file')
            sys.exit()
        if not os.path.exists(argv[3]) :
            print(argv[3] + ' does not exist')
            sys.exit()
        if not os.path.isfile(argv[3]):
            print(argv[3] + ' not a file')
            sys.exit()
        train = open(argv[0], 'r', errors='ignore')
        dev = open(argv[3], 'r', errors='ignore')
        train_temp = open('neresptrain', 'w')
        dev_temp = open('nerespdev', 'w')
        createtempfile(train, train_temp)
        createtempfile(dev, dev_temp)
        args = ['neresptrain'] + [argv[1]] + [argv[2]] + ['nerespdev']
        perceplearn.main(args)
        os.remove('neresptrain')
        os.remove('nerespdev')
    else:
        print("Usage: python3 nelearn.py TRAININGFILE MODELFILE [-h DEVFILE]")
        sys.exit()
    
if __name__=="__main__":
    main(sys.argv[1:])
