# 测试电脑性能
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# 计算斐波那契数列的第30个数
result = fibonacci(36)
print(result)
