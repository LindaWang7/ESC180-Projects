import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    vec1_size=0
    vec2_size=0

    if len(vec1) == 0 or len(vec2) == 0:
        return 0

    for value in vec1.values():
        vec1_size+=value**2

    for value in vec2.values():
        vec2_size+=value**2

    uv_maginitude=math.sqrt(vec1_size * vec2_size)

    dot_values=[]
    dot_value=0
    for key in vec1:
        if key in vec2:
            # dot_values.append((vec1[key],vec2[key]))
            dot_value += (vec1[key]*vec2[key])

    return dot_value/uv_maginitude

def build_semantic_descriptors(sentences): #change
    allword_dict = {}
    for sentence in sentences:
        set_sentence=set(sentence)
        for word in set_sentence:
            temp = {}
            for w in sentence:
                if w != word:
                    temp[w]=1

            if word in allword_dict.keys():
                for key in temp.keys():
                    if key in allword_dict[word]:
                        allword_dict[word][key]+=1
                    else:
                        allword_dict[word][key]=1
            else:
                allword_dict[word] = temp

    return allword_dict


def build_semantic_descriptors_from_files(filenames):

    all_list=[]
    for i in range (len(filenames)):
        # sentence_list=[]
        f=open(filenames[i],"r",encoding="latin1")
        text=f.read()
        sentence_list = text.replace("!", ".").replace("?", ".").lower().split(".")
        all_list.extend(sentence_list)
    #print(all_list)
    all_list=list(filter(None,all_list))

    sentence_list_strip=[]
    word_lists=[]

    for sentence in all_list:
        sentence_list_strip.append(sentence.strip())
        new=sentence.replace(",", " ").replace("-", " ").replace("--", " ").replace(";", " ").replace(":", " ").replace('"'," ").replace("\n"," ").split()

        word_lists.append(new)

    # print(word_lists)
    count_dict=build_semantic_descriptors(word_lists)

    # print(count_dict['â\x80\x9d'])
    # print(count_dict)
    return count_dict

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    if word not in semantic_descriptors.keys():
        return choices[0]

    choice_simlarity=[0 for i in range (len(choices))]

    for i in range (len(choices)):
        if choices[i] not in semantic_descriptors.keys():
            choice_simlarity[i]=-1
        else:
            simlarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[i]])
            choice_simlarity[i]=simlarity

    highest=max(choice_simlarity)
    best_match_index=choice_simlarity.index(highest)

    # max_index=-1
    # max_same=0
    # for i in range(len(choices)):
    #     simlarity=similarity_fn(semantic_descriptors[word],semantic_descriptors[choices[i]])
    #     if max_same<simlarity:
    #         max_same=simlarity
    #         max_index=i

    #print( similarity_fn (semantic_descriptors["man"],semantic_descriptors["i"] ) )
    return choices[best_match_index]

def run_similarity_test(filename, semantic_descriptors, similarity_fn):

    f=open(filename)
    all_questions=[]
    for line in f.readlines():
        all_questions.append(line.strip().split())

    # print(all_questions)

    correct_answers=[]
    found_answers=[]
    for q in all_questions:
        question=q[0]
        choices=q[1:]
        correct_answers.append(q[1])
        word = most_similar_word(question, choices, semantic_descriptors, similarity_fn)
        found_answers.append(word)

    correct_count=0
    for i in range (len(correct_answers)):
        if correct_answers[i]==found_answers[i]:
            correct_count+=1

    return correct_count/len(correct_answers)*100
    # print(semantic_descriptors)


if __name__=="__main__":

    v1 = {"a": 1, "b": 2, "c": 3}
    v2 = {"b": 4, "c": 5, "d": 6}

    sentences=[["i", "am", "a", "sick", "man"],
    ["i", "am", "a", "spiteful", "man"],
    ["i", "am", "an", "unattractive", "man"],
    ["i", "believe", "my", "liver", "is", "diseased"],
    ["however", "i", "know", "nothing", "at", "all", "about", "my",
    "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]

    a=cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6})
    print(a)
    #part a
    #print(cosine_similarity(v1,v2))

    # part b
    #me=build_semantic_descriptors(sentences)


    #part c
    # files=["testText.txt","testText2.txt"]
    # print(build_semantic_descriptors_from_files(files))

    #part d
    # word="man"
    # choices=["a","i","sick"]
    # most_similar_word(word, choices, build_semantic_descriptors(sentences), cosine_similarity)

    # filename="test.txt"
    # sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    # # sem_descriptors = build_semantic_descriptors_from_files(["Harry_potter.txt"])
    #
    #sem_descriptors = build_semantic_descriptors_from_files(["testText.txt","testText2.txt"])
    #
    # a=run_similarity_test(filename, sem_descriptors, cosine_similarity)
    # print(a)


    # if two words doesn't exist in the txt, thus, dictionary doesn't exist just return -1