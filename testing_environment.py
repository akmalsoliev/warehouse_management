import pickle
import os 
import pathlib
import datetime

root_dir = os.path.dirname(os.path.abspath(__file__))
binary_file_location = str(pathlib.Path().joinpath(root_dir, r'__backup\__backup_timer.pickle'))
# write_file = open(binary_file_location, 'wb')
# pickle.dump(datetime.datetime.utcnow(), write_file)
# write_file.close()

load_file = open('__backup\__backup_timer.pickle', 'rb')
loader = pickle.load(load_file)
print(loader)