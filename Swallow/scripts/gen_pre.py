from Planner import planner

if __name__ == "__main__":
    planner = planner.Planner()
    result = 1
    planner.read_topology_from_file("../dataset/Airtel1-2/topology")
    # 指定文件路径
    file_path = '../dataset/Airtel1-2/preparation'

    # 以写入模式 ('w') 打开文件以清空其内容
    with open(file_path, 'w') as file:
        pass  # 不需要写入任何内容，只需打开和关闭文件即可清空其内容

    result_que = planner.gen("335544320", "LAIX", ["Palermo"], "(exist >= 1, Palermo.*LAIX)", fault_scenes=None)
