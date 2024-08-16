import re


def remove_chars_regex(behavior):
    return re.sub(r'[()\s]', '', behavior)


def trans(behavior):
    behavior_new = {"match": "", "path": {"path_exp": []}}
    behavior = remove_chars_regex(behavior)
    behavior = behavior.split(",")
    behavior_new["match"] = behavior[0]
    behavior_new["path"]["path_exp"] = behavior[1]
    # print(behavior_new["path"]["path_exp"])
    return behavior_new


# trans("(exist >= 1, Singapore.*London)")
