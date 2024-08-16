import tracemalloc
import time
from verification.k_value import K_value

from util.parse import Parse
from verification.verify import Verify
if __name__ == "__main__":
    tracemalloc.start()
    file_path = '../dataset/i2'
    verify = Verify(file_path)
    verify.verify()
    result = verify.get_result()
    current, peak = tracemalloc.get_traced_memory()
    memory = (peak - current) / (1024 * 1024)
    print(f"Memory use: {memory} MB")
