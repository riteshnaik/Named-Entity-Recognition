import sys
import pickle
import re
import codecs
from collections import Counter

def TagWord(line, feature_list, class_list, weight):
        tag = class_list.get(1)
        list = line.split()
        prod = [0] *len(class_list)
        count = Counter(list)
        for key,  value in count.items():
            if key in feature_list:
                for i in range(0, len(weight)):
                     prod[i] = prod[i] + value * weight[i][feature_list[key]]
        z = prod.index(max(prod))
        for key,  value in class_list.items():
            if value == z:
                tag = key
        return tag

def main(argv):
    model_file = open(argv[0], 'rb')
    model = pickle.load(model_file)
    feature_list = model['features']
    class_list = model['class']
    weight = model['weight']
    feature = {}
    sys.stdin = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')
    for line in sys.stdin:
        list = line.split()
        i = 0
        for item in list:
            current_word = ''.join(item.split('/')[0:-1])
            current_tag = item.split('/')[-1]
            wshape = re.sub(r'[A-Z]', 'A', current_word)
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
                feature[0] = 'PREV_WORD_'+ ''.join(list[i-1].split('/')[0:-1])
                feature[1] = 'PREV_TAG_'+list[i-1].split('/')[-1]
            feature[2] = 'CURR_WORD_'+ current_word
            feature[3] = 'CURR_TAG_'+ current_tag
            if i == len(list) - 1:
                feature[4] = 'EOS_WORD'
                feature[5] = 'EOS_TAG'
            else:
                feature[4] = 'NEXT_WORD_'+''.join(list[i+1].split('/')[0:-1])
                feature[5] = 'NEXT_TAG_'+list[i+1].split('/')[-1]
            feature[6] = 'WSHAPE_'+wshape
            if len(current_word) < 3:
                feature[7] = 'SUFFIX3_'
            else:
                feature[7] = 'SUFFIX3_'+current_word[-3:]
            if len(current_word) < 2:
                feature[8] = 'SUFFIX2_'
            else:
                feature[8] = 'SUFFIX2_'+current_word[-2:]
            feature_line = feature[0] + ' '+ feature[1] + ' '+ feature[2]+' '+feature[3] + ' '+ feature[4] + ' '+ feature[5]+' '+feature[6]+' '+ feature[7]+' '+feature[8]
            tag= TagWord(feature_line, feature_list, class_list, weight)
            if i == len(list) - 1:
                 print(item+'/'+tag+'\n', end='')
            else:
                 print(item+'/'+tag+' ', end='')
            i=i+1
if __name__ == "__main__":
    main(sys.argv[1:])
