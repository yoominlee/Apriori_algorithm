import sys
from itertools import combinations

def calculate_support_confidence():
    output_file = open(sys.argv[3], 'w')
    for i in list(total_l_k.keys()):  # frequent set 선택
        if type(i) != int:  # frequent set 두 덩어리로 나누어야 하니 크기가 2 이상인 것들만 # print(type(i)) -> 크기 1은 int, 2 이상은 tuple 형태
            final_output_3 = round(total_l_k[i] / len(transaction_2dlist), 2)
            for j in range(1, len(i)):  # set의 크기가 4이면 1 2 3 반복.   ## 2이상의 frequent set에서 두 덩어리로
                ass_item_comb = list(combinations(i, j))  # frequent set인 한 itemset에서, j 개의 combination --> tuple이 들어있는 list 형태
                for one_comb in ass_item_comb:  # ass_item_comb: [(1, 8), (1, 16), (8, 16)], one_comb: {8, 1}, {16, 1}, {8, 16}
                    final_output_1 = "{" + str(sorted(set(one_comb)))[1:-1] + "}"

                    whole_s = set(i)
                    second_comb = whole_s
                    for item in one_comb:  # 첫번째 덩어리에 들어있는 각각 item 전체에서 뺀게 두번째 덩어리.
                        second_comb.remove(item)
                    final_output_2 = "{" + str(sorted(set(second_comb)))[1:-1] + "}"
                    if len(one_comb) == 1:  # associate 계산 할 첫번째 덩어리의 크기가 1인 경우 한번 더 처리 해줘야함
                        one_comb = (list(one_comb)[0])

                    final_output_4 = round(total_l_k[i] / total_l_k[one_comb], 2)

                    output_file.write(f'{str(final_output_1):12} {str(final_output_2):12} {final_output_3:5} {final_output_4:5}\n')

    output_file.close()

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
        candidate_list = set()
        for a in prev_list:
            for b in prev_list:
                if a != b:
                    c = list(set(a).union(set(b)))
                    if len(c) == itemset_size:
                        c = sorted(c)
                        candidate_list.add(tuple(c))
        candidate_list = list(candidate_list)

    return candidate_list

def until_size1_freq_list(min_sup_perc, total_l_k):
    input_file = open(sys.argv[2], 'r') # open(파일 이름, 열기모드(r/w/a))

    raw_data = input_file.readlines() # list 형태임.

    transaction_2dlist=[]

    count = 0
    for one_transaction in raw_data:
        t = one_transaction.replace("\n", "").split()
        templist = []
        for item in t:
            templist.append(int(item))

        transaction_2dlist.append(templist)
        count += 1

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

    l_1.sort() # 정렬 제대로 안되어 있음 1,11,14 등 1로 시작하는 것 나오고 2나옴
    # ---------- 여기까지) size 1인 frequent list 찾음
    return input_file, l_1, transaction_2dlist, total_l_k, minsup_int

if __name__ == '__main__':
    min_sup_perc = sys.argv[1]

    total_l_k = {}
    input_file, l_1, transaction_2dlist, total_l_k, minsup_int = until_size1_freq_list(min_sup_perc,total_l_k)
    input_file.close()

    l_k_not_empty = True
    if len(l_1) == 0:
        l_k_not_empty = False
    k = 2
    l_k = []
    while l_k_not_empty:

        # (pseudo-code line 5)generate candidate (C_k+1 = candidates generated from L_k)
        if k == 2:
            c_k1 = candidate(l_1,2)
        else:
            c_k1 = candidate(l_k,k)

        # (pseudo-code line 6)CANDIDATE 각각과 DB 확인해서 COUNT 세는 과정(for each transaction t in database do)
        item_size_k = {}
        for one_c in c_k1: # k길이의 candidate의 개수만큼 반복
            for transaction in transaction_2dlist: # 한 candidate db에 있는지 db 하나씩 확인
                if len(transaction) >= len(one_c):
                    check = 0
                    c_num = 0
                    while c_num < len(one_c):
                        if one_c[c_num] in transaction:
                            check += 1
                            c_num += 1
                            continue
                        c_num += 1

                    if check == k:
                        if tuple(one_c) in item_size_k:
                            item_size_k[tuple(one_c)] += 1
                        else:
                            item_size_k[tuple(one_c)] = 1

        l_k = []
        for item in item_size_k:
            if item_size_k[item] > minsup_int:
                l_k.append(item)
                total_l_k[item] = item_size_k[item]

        l_k.sort()
        if len(l_k) == 0:
            l_k_not_empty = False
        k += 1

    # 여기까지가 frequent set 구한 것.
    # 여기서부터 frequent set 사용해서 association rule
    calculate_support_confidence()