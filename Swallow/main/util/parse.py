

class Parse:
    def __init__(self, file_path):
        self.file_path = file_path
        self.preparations = []

    def get_preparation(self):
        return self.preparations

    def set_preparation(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        current_prep = None
        for line in lines:
            preparation = line.strip()
            if preparation.startswith("preparation"):
                if current_prep:
                    self.preparations.append(current_prep)
                current_prep = {"preparation": preparation}
            elif ":" in preparation:
                key, value = preparation.split(':', 1)
                if key.strip() == "all_paths":
                    current_prep[key.strip()] = [value.strip()]
                else:
                    current_prep[key.strip()] = value.strip()
            else:
                if preparation:
                    if 'all_paths' in current_prep:
                        current_prep['all_paths'].append(preparation.strip())
                        if 'all_paths' in current_prep:
                            current_prep['all_paths'] = [path for path in current_prep['all_paths'] if path]
                    else:
                        current_prep['all_paths'] = [preparation.strip()]
        if current_prep:
            self.preparations.append(current_prep)
        # for prep in self.preparations:
        #     print(prep)