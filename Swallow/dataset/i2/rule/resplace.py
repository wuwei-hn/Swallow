# 定义文件名
filename = "wash"

# 读取文件内容并过滤行
with open(filename, 'r') as file:
    lines = file.readlines()

# 过滤掉包含“xe”的行
filtered_lines = [line for line in lines if "." not in line]

# 将过滤后的内容写回文件
with open(filename, 'w') as file:
    file.writelines(filtered_lines)

print(f"已删除包含 'xe' 的行并将结果写回文件 '{filename}'")
