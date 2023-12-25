Base = []


def dist(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def mat(i):
    mi = []
    for x in range(4):
        for y in range(4):
            if dist((x, y), (i // 4, i % 4)) <= 2:
                mi.append(1)
            else:
                mi.append(0)
    return mi


def gen_mat():
    for item in range(4 * 4):
        Base.append(mat(item))


def add(m1, m2):
    new_m = []
    for i in range(4 * 4):
        new_m.append((m1[i] + m2[i]) % 2)
    return new_m


def prt():
    for i in range(4 * 4):
        for j in range(4 * 4 + 1):
            print(Base[j][i], end=' ')
        print()


def row_add(i, j):
    # 第i行加到第j行里
    for x in range(4 * 4 + 1):
        Base[x][j] = (Base[x][j] + Base[x][i]) % 2


def row_change(i, j):
    # i, j行交换
    for x in range(4 * 4 + 1):
        mid = Base[x][i]
        Base[x][i] = Base[x][j]
        Base[x][j] = mid


def row_simplified():
    # 高斯消元法行化简
    for j in range(4 * 4):
        position = []   # 第j列里1的位置
        for i in range(4 * 4):
            if Base[j][i] == 1:
                position.append(i)
        c_pos = -1      # 第1个大于等于j的非0元
        for f in position:
            if f >= j:
                c_pos = f
                break
        # print(c_pos)
        # print(position)
        if c_pos == -1:
            continue
        elif len(position) > 1:
            for p in range(len(position)):
                if position[p] != c_pos:
                    row_add(c_pos, position[p])
            if c_pos != j:
                row_change(j, c_pos)
        else:
            if c_pos != j:
                row_change(j, c_pos)
        # prt()
        # print('----------------------------------')


def exam():
    # 检查阶梯型是否满秩
    flag = True
    for i in range(4 * 4):
        if Base[i][i] == 0:
            flag = False
        else:
            continue
    if not flag:
        return False
    else:
        return True


def answer(init, target):
    gen_mat()
    det_s = add(init, target)
    Base.append(det_s)
    row_simplified()
    if exam():
        asw = []
        for i in range(4 * 4):
            if Base[4 * 4][i] == 1:
                asw.append(i + 1)
        return asw


if __name__ == '__main__':
    org = [0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0]
    tgt = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    aw = answer(org, tgt)
    prt()
    print(aw)
