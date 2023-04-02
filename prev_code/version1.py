#######################################################################
# 작업중 파일
# size 3인 candidate list 까지 만드는 것 성공.
# 함수화 하는것 시도는 main2 파일에서 XXXXXXXXXX
# 함수화 이전에 candidate 부분 잘못된것 같아서 수정 하면서 함수화
#######################################################################

'''
                변수명 정리
-------------------------------------------------
input_file = 파일 연것
raw_data = 줄별로 list 형태
	raw_data 한줄씩 one_transaction

transaction_2dlist = 크기 1 candidate
item_size_1 = dictionary 형태. 횟수랑 쌍
l_1 = item_size_1중에서 minsup_int 이상 인것들 list 형태

temp_c_2 = l_1로 만든 조합. tuple들이 들어있는 list
c_2 = 크기 2 candidate. 2d list
item_size_2 = dictionary 형태. 횟수랑 쌍
l_2 = item_size_2중에서 minsup_int 이상 인것들 list 형태


temp_c_3 = l_2로 만든 조합. tuple들이 들어있는 list               [('0', '1', '10'), ('0', '1', '11'), ('0', '1', '12'),
c_3 = 크기 3 candidate. 2d list                               [['0', '1', '10'], ['0', '1', '11'], ['0', '1', '12'],
-------------------------------------------------
temp는 항상 반복문 내부에 위치해서 다시 쓸 수 있게?
item도
'''
if __name__ == '__main__':
    # c_k = []
    # l_k = []
    # l_1 = []

    input_file = open("input.txt", 'r') # open(파일 이름, 열기모드(r/w/a))


    ## 한 줄씩 3번 읽고 각각 출력
    # line = input_file.readline()
    # line2 = input_file.readline()
    # line3 = input_file.readline()
    #
    # print(line)
    # print(line2)
    # print(line3)

    raw_data = input_file.readlines() # list 형태임.
    # print(len(raw_data)) # 500
    # print(len(raw_data[0])) # 5
    # print(len(raw_data[1])) # 2
    # print(raw_data[0]) # 7	14
    # print(raw_data[1]) # 9
    # print(raw_data[0][0]) # 7
    # print(type(raw_data[0]))  # <class 'str'>

    ## 각 줄 요소별 확인
    # k = 0
    # for i in raw_data[0]:
    #     print(k,": ",i)
    #     k+=1
    # print("------")
    # k = 0
    # for i in raw_data[1]:
    #     print(k, ": ", i)
    #     k+=1

    ''' output
    0 :  7
    1 :  	
    2 :  1
    3 :  4
    4 :  

    ------
    0 :  9
    1 :  
    '''
    transaction_2dlist=[]

    # split_test = raw_data[0].split('\t')
    count = 0
    for one_transaction in raw_data:
        t = one_transaction.replace("\n", "").split()
        transaction_2dlist.append(t)
        count += 1

    print(count) # 500
    print(len(transaction_2dlist)) # 500

    # ---------- 여기까지) 파일 읽어서 2d리스트의 각 행은 한 transaction, 각 행 속에는 item 각각이 구분되어 들어가 있음
    minsup_int = 1

    item_size_1 = {}
    for items in transaction_2dlist:
        for item in items:
            if item in item_size_1:
                item_size_1[item] += 1
            else:
                item_size_1[item] = 1

    l_1 = []
    for item in item_size_1:
        if item_size_1[item] > minsup_int:
            l_1.append(item)

    print(len(l_1))
    print(l_1)
    l_1.sort() # 정렬 제대로 안되어 있음 1,11,14 등 1로 시작하는 것 나오고 2나옴
    print(l_1)
    # ---------- 여기까지) size 1인 frequent list 찾음

    # from itertools import combinations
    # test = [1,3,5,7]
    # comb2 = list(combinations(test,2))
    # print(comb2)
    # comb3 = list(combinations(test,3))
    # print(comb3)
    #
    # comb23 = list(combinations(comb2, 3))
    # print(comb23) # 2 쌍 자체를 하나의 요소로 봄 (원하는 방향으로 못구함)

    from itertools import combinations

    print("item_size_1: ",item_size_1)
    print("l_1: ",l_1)


    c_2 = []

    temp_c_2 = list(combinations(l_1, 2))
    print("temp_c_2: ", temp_c_2)
    print(type(temp_c_2)) # <class 'list'>
    print(type(temp_c_2[0]))  # <class 'tuple'>

    c_2 = []
    for i in temp_c_2:
        one_itemset_size2 = []
        for item in i:
            one_itemset_size2.append(item)

        c_2.append(one_itemset_size2)

    print(c_2)
    print(type(c_2))
    print(type(c_2[0]))

    # ---------- 여기까지) size 2인 candidate list 찾음

    item_size_2 = {}

    ## 2 쌍이 아니라 요소 1개씩 확인하는것임. 잘못된것
    # for one_c_2 in c_2:
    #     for item in one_c_2:
    #         if item in item_size_2:
    #             item_size_2[item] += 1
    #         else:
    #             item_size_2[item] = 1

    for one_c_2 in c_2:
        # print("------------",range(len(one_c_2)))
        for i in range(len(one_c_2)):
            for transaction in transaction_2dlist:
                if len(transaction) < len(one_c_2):
                    break
                else:
                    check = True
                    for j in range(len(one_c_2)): # 위에서 선택한 한 transaction에 c_2 있는지 확인
                        if check == True:
                            if c_2[j] in transaction:
                                check == True
                            else:
                                check == False
                    if check == True:
                        if tuple(one_c_2) in item_size_2:
                            item_size_2[tuple(one_c_2)] += 1
                        else:
                            item_size_2[tuple(one_c_2)] = 1

    print(item_size_2)
                    # [te for te in len(one_c_2) if i==12]
                    #     print("fdsf")

    print("item_size_2: ",item_size_2)
    print("len(item_size_2): ",len(item_size_2))
    print("type(item_size_2): ",type(item_size_2))

    l_2 = []
    for item in item_size_2:
        if item_size_2[item] > minsup_int:
            l_2.append(item)

    print("l_2: ",l_2)
    print("len(l_2): ",len(l_2))

    # ---------- 여기까지) size 2인 frequent list 찾음

    before_comb = []
    for items in l_2:
        for item in items:
            if item not in before_comb:
                before_comb.append(item)

    temp_c_3 = list(combinations(before_comb, 3))
    print(temp_c_3)


    c_3 = []
    for i in temp_c_3:
        one_itemset_size3 = []
        for item in i:
            one_itemset_size3.append(item)

        c_3.append(one_itemset_size3)

    print(c_3)
    # ---------- 여기까지) size 3인 candidate list 찾음








    # split_test = raw_data[0].replace("\n", "").split()

    ## split 했을 때 각 요소 어떻게 들어가는지 확인, 마지막 줄바꿈도 하나로 인식되는것 확인-> replace 넣어줌
    # print(len(split_test))
    # temp = 0
    # for i in split_test:
    #     print(len(i))
    #     print(temp, ": ", i)
    #     temp += 1
    #     temp2 = 0
    #     for j in i:
    # 
    #         print("temp2) ", temp2, ": ",j)
    #         temp2 += 1
    '''
    2
    1
    0 :  7
    temp2)  0 :  7
    2
    1 :  14
    temp2)  0 :  1
    temp2)  1 :  4
    '''

    # for transaction in raw_data:
    #     print()

    input_file.close()


    ## 딕셔너리 형태로 support랑 짝 만들기?

    # 파일 읽기

    # k = 0
    # c = []
    # l = []

    # 길이 1짜리

    #
    # for k=1; l != []; k++:
    # while l != []:
    # while len(l) != 0:
    #     k += 1

        # l_k 가지고 c_k+1 (k+1 길이의 candidate를 k길이의 frequent 가지고 만들기)

        # for each transaction t in database do
        #     increment the count of all candidates in C_k+1 that are contained in t

        # l_k+1 = c_k+1 중에 min_support 이상인 것들

    # l들의 합 return