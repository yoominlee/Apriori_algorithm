#######################################################################
# 구현 완료 파일
# 명세에 나온대로 파일 입출력 완료
# 파일 제출용으로 main4.py에서 지저분한것 정리 필요
#######################################################################
import sys

def output_txt(total_l_k):
    # f = open("output.txt", 'a')
    # print(type(list(total_l_k.keys())))
    # print(len(list(total_l_k.keys())))
    for i in list(total_l_k.keys()): # 같은 사이즈 모인 set 선택
        # for j in i: # 그 크기 set 아이템 한개식 (한 set)
        # print(i," ",total_l_k(i))
        print(i, " ", total_l_k[i])

            # data = "%d번째 줄입니다.\n" % i
            # f.write(data)
    # f.close()

from itertools import combinations

def candidate(prev_list, itemset_size):
    if itemset_size == 2:
        candidate_list = []
        temp_c_2 = list(combinations(prev_list, 2))
        # temp_c_2 = list(temp_c_2) # 중복제거용으로 set으로 만든 후 다시 list로 --> 제대로 적용 안되는 것 같아 main 부분에서
        for i in temp_c_2:
            one_itemset_size2 = []
            for item in i:
                one_itemset_size2.append(item)

            candidate_list.append(one_itemset_size2)
    else:
        # temp_c_k = list(combinations(prev_list, k))
        # candidate_list = set(temp_c_k)
        candidate_list = set()
        for a in prev_list:
            for b in prev_list:
                if a != b:
                    c = list(set(a).union(set(b)))
                    # print("c: ",c)
                    # c = a.union(b)
                    if len(c) == itemset_size:
                        c = sorted(c)
                        print(c)
                        candidate_list.add(tuple(c))
        candidate_list = list(candidate_list)

    # print(candidate_list)
    return candidate_list

def until_size1_freq_list(min_sup_perc, total_l_k):
    input_file = open(sys.argv[2], 'r') # open(파일 이름, 열기모드(r/w/a))

    ## 한 줄씩 3번 읽고 각각 출력
    # line = input_file.readline()
    # line2 = input_file.readline()
    # line3 = input_file.readline()
    #
    # print(line)
    # print(line2)
    # print(line3)

    raw_data = input_file.readlines() # list 형태임.

    transaction_2dlist=[]

    # split_test = raw_data[0].split('\t')
    count = 0
    for one_transaction in raw_data:
        t = one_transaction.replace("\n", "").split()
        templist = []
        for item in t:
            print(item)
            templist.append(int(item))
        print(templist)
        # print(templist)

        transaction_2dlist.append(templist)
        count += 1

    # print(count) # 500
    # print(len(transaction_2dlist)) # 500

    # ---------- 여기까지) 파일 읽어서 2d리스트의 각 행은 한 transaction, 각 행 속에는 item 각각이 구분되어 들어가 있음

    minsup_int = (int(min_sup_perc) / 100) * len(transaction_2dlist)
    item_size_1 = {}
    for items in transaction_2dlist:
        for item in items:
            # item = int(item)
            if item in item_size_1:
                item_size_1[item] += 1
            else:
                item_size_1[item] = 1

    l_1 = []
    for item in item_size_1:
        if item_size_1[item] > minsup_int:
            l_1.append(int(item))
            total_l_k[item] = item_size_1[item]

    # print(len(l_1))
    # print(l_1)
    l_1.sort() # 정렬 제대로 안되어 있음 1,11,14 등 1로 시작하는 것 나오고 2나옴
    # print(l_1)
    # ---------- 여기까지) size 1인 frequent list 찾음
    return input_file, l_1, transaction_2dlist, total_l_k, minsup_int

if __name__ == '__main__':
    min_sup_perc = sys.argv[1]
    # inpupfile = sys.argv[1]
    # min_sup_perc = sys.argv[2]
    print(min_sup_perc)
    # minsup_int = float(min_sup_perc) *

    total_l_k = {}
    input_file, l_1, transaction_2dlist, total_l_k, minsup_int = until_size1_freq_list(min_sup_perc,total_l_k)
    input_file.close()
    print("transaction_2dlist: ",transaction_2dlist)

    l_k_not_empty = True
    if len(l_1) == 0:
        l_k_not_empty = False
    k = 2
    l_k = []
    while l_k_not_empty:
        print("--------------", k, " str --------------")

        # generate candidate (C_k+1 = candidates generated from L_k)
        if k == 2:
            c_k1 = candidate(l_1,2)
        else:
            c_k1 = candidate(l_k,k)

            # c_k1 = []
            # # candidate 중복 제거
            # for c in temp_c_k1:
            #     if c not in c_k1:
            #         c_k1.append(c)
            # c_k1 = list(c_k1)
        print(c_k1)
        # CANDIDATE 각각과 DB 확인해서 COUNT 세는 과정(for each transaction t in database do)
        item_size_k = {}
        for one_c in c_k1: # k길이의 candidate의 개수만큼 반복
            # print("------------",range(len(one_c_2)))
            # for i in range(k):
            for transaction in transaction_2dlist: # 한 candidate db에 있는지 db 하나씩 확인
                if len(transaction) >= len(one_c):
                    # check = True
                    check = 0
                    c_num = 0
                    # for j in range(len(one_c)):  # 위에서 선택한 한 transaction에 c_2 있는지 확인
                    while c_num < len(one_c):
                        # if check == True:
                            # print(one_c[j])
                        if one_c[c_num] in transaction:
                            check += 1
                            c_num += 1
                            continue
                        c_num += 1
                        # for t in transaction:
                        #     if one_c[j] == t:
                        #         check += 1
                    # print(one_c, " in ", transaction, "-> count : ", check)
                                # check = True
                                # continue
                            # else:
                            #     check = False
                            # print(one_c[j], "==", t, " ", check)

                    # print(item_size_k)
                    if check == k:
                        # print("if check == True:", one_c)
                        if tuple(one_c) in item_size_k:
                            # print(tuple(one_c))
                            item_size_k[tuple(one_c)] += 1
                            # print("+")
                        else:
                            item_size_k[tuple(one_c)] = 1
                            # print("0")

        # item_size_k = item_size_k.sort()
        print(item_size_k)
        # print(len(item_size_k))
        # print(item_size_k.values())
        l_k = []
        for item in item_size_k:
            if item_size_k[item] > minsup_int:
                l_k.append(item)
                total_l_k[item] = item_size_k[item]
                # print(item)

        l_k.sort()

        # total_l_k.append(l_k)
        print("--------------", k, " fin --------------")
        # print("total_l_k", total_l_k)
        # print("l_k",l_k)
        if len(l_k) == 0:
            l_k_not_empty = False
        k += 1

    print(total_l_k) # ... , (3, 5, 8, 16): 33, (3, 7, 8, 16): 31}
    print(min_sup_perc)
    print(minsup_int)
    print(len(transaction_2dlist))

    ####################################### 여기까지가 frequent set 구한 것.
    # 여기서부터 association rule
    output_file = open("output.txt", 'w')

    for i in list(total_l_k.keys()): # frequent set 선택
        if type(i) != int: # frequent set 두 덩어리로 나누어야 하니 크기가 2 이상인 것들만 # print(type(i)) -> 크기 1은 int, 2 이상은 tuple 형태
            # print("======== ",i," ========")
            # print("n(A합B) [", i,"] : ",total_l_k[i])
            final_output_3 = round(total_l_k[i] / len(transaction_2dlist), 2)
            # print("final_output_3: ", final_output_3)
            for j in range(1,len(i)): # set의 크기가 4이면 1 2 3 반복.   ## 2이상의 frequent set에서 두 덩어리로
                ass_item_comb = list(combinations(i,j)) # frequent set인 한 itemset에서, j 개의 combination --> tuple이 들어있는 list 형태
                # print("---- size: ",j," combination ----")
                # print(ass_item_comb) # [(1, 8), (1, 16), (8, 16)]
                for one_comb in ass_item_comb: # ass_item_comb: [(1, 8), (1, 16), (8, 16)], one_comb: {8, 1}, {16, 1}, {8, 16}
                    # print("     ++      ")
                    final_output_1 = "{"+ str(sorted(set(one_comb)))[1:-1] +"}"

                    whole_s = set(i)
                    # print("whole_s: ", whole_s, ": ", total_l_k[i])
                    second_comb = whole_s
                    # one_s = set(sorted(set(one_comb)))
                    for item in one_comb: # 첫번째 덩어리에 들어있는 각각 item 전체에서 뺀게 두번째 덩어리.
                        second_comb.remove(item)
                    final_output_2 = "{"+ str(sorted(set(second_comb)))[1:-1] +"}"
                    # print("one_comb: ", one_comb, " ", type(one_comb), " ", len(one_comb))
                    if len(one_comb) == 1: # associate 계산 할 첫번째 덩어리의 크기가 1인 경우 한번 더 처리 해줘야함
                        one_comb = (list(one_comb)[0])
                    # print("one_comb: ", one_comb, ": ", total_l_k[one_comb])

                    final_output_4 = round(total_l_k[i] / total_l_k[one_comb], 2)
                    # print(final_output_1, " ", final_output_2, " ", final_output_3, " ", final_output_4)
                    # print(f'{str(final_output_1):12} {str(final_output_2):12} {final_output_3:5} {final_output_4:5}')
                    output_file.write(f'{str(final_output_1):12} {str(final_output_2):12} {final_output_3:5} {final_output_4:5}\n')

    output_file.close()