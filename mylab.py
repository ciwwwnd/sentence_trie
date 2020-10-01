import re
import string


global poses_tags
filename = 'mother.conllu'

def build_tree(filename):

    """"Функция принимает на вход файл и создает дерево с вершиной 0. root"""

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.read().translate(str.maketrans('', '', string.punctuation)).split('\n')
    for k in range(4):
        del lines[0]
    words = [l.split('\t') for l in lines[:-1]]
    del words[-1]
    some_tags = [word[3] for word in words]
    ttokenz = [w[0] + '. ' + w[2] for w in words]
    global poses_tags
    poses_tags = {}
    for i in range(len(ttokenz)):
        poses_tags[ttokenz[i]] = some_tags[i]
    nds = [('0. root', [])]
    nds.extend([(t, []) for t in ttokenz])
    for i, word in enumerate(words):
        nds[int(word[6])][1].append(nds[i + 1])

    return nds[0]

print(build_tree(filename))

def get_noun_or_verb_group(node):

    """"Функция принтит именные и глагольные группы, но еще у них есть список"""

    pattern = '\d+\.\s'
    pattern_re = re.sub(pattern, '', node[0])
    global poses_tags
    res_verb = []
    res_noun = []
    if poses_tags[node[0]] == 'VERB':
        if node[1] != []:
            for i in range(len(node[1])):
                pattern_re_re = re.sub(pattern, '', node[1][i][0])
                verbz = pattern_re, pattern_re_re
                res_verb.append(verbz)
                print('Глагольная группа: ' + pattern_re + ' - ' + pattern_re_re)
                if node[1][i][1] != []:
                    get_noun_or_verb_group(node[1][i])
    if poses_tags[node[0]] == 'NOUN':
        if node[1] != []:
            for i in range(len(node[1])):
                pattern_re_re = re.sub(pattern, '', node[1][i][0])
                nounz = pattern_re, pattern_re_re
                res_noun.append(nounz)
                print('Именная группа: ' + pattern_re + ' - ' + pattern_re_re)
                if node[1][i][1] != []:
                    get_noun_or_verb_group(node[1][i])


node = build_tree(filename)
get_noun_or_verb_group(node[1][0])
