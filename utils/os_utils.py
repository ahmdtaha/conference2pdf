import os
import csv
import errno
import pickle
import os.path as osp
from shutil import copyfile
from scipy.io import loadmat
from scipy.io import savemat

def get_project_name():
    project_name = osp.basename(osp.abspath('./'))

def get_last_part(path):
    return os.path.basename(os.path.normpath(path))

def copy_file(f,dst,rename=None):
    touch_dir(dst)
    # for f_idx,f in enumerate(src_file_lst):
    if os.path.exists(f):
        # print(f)
        if rename ==None:
            copyfile(f, os.path.join(dst,get_last_part(f)))
        else:
            _,ext = get_file_name_ext(f)
            copyfile(f, os.path.join(dst, rename+ext ))
    else:
        raise Exception('File not found')

def copy_files(src_file_lst,dst,rename=None):
    touch_dir(dst)
    for f_idx,f in enumerate(src_file_lst):
        if os.path.exists(f):
            # print(f)
            if rename ==None:
                copyfile(f, os.path.join(dst,get_last_part(f)))
            else:
                _,ext = get_file_name_ext(f)
                copyfile(f, os.path.join(dst, rename[f_idx]+ext ))
        else:
            raise Exception('File not found')

def dataset_tuples(dataset_path):
    return dataset_path + '_tuples_class'


def get_dirs(base_path):
    return sorted([f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))])


def get_files(base_path,extension,append_base=False):
    if (append_base):
        files =[os.path.join(base_path,f) for f in os.listdir(base_path) if (f.endswith(extension) and not f.startswith('.'))];
    else:
        files = [f for f in os.listdir(base_path) if (f.endswith(extension) and not f.startswith('.'))];
    return sorted(files);

def csv_read(csv_file,has_header=False):
    rows = []
    with open(csv_file, 'r') as csvfile:
        file_content = csv.reader(csvfile)
        if has_header:
            header = next(file_content, None)  # skip the headers
        for row in file_content:
            rows.append(row)

    return rows

def csv_write(csv_file,rows):
    with open(csv_file, mode='w') as file:
        rows_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            rows_writer.writerow(row)



def txt_read(path):
    with open(path) as f:
        content = f.readlines()
    lines = [x.strip() for x in content]
    return lines

def mat_read(path):
    file_content = loadmat(path)
    return file_content

def mat_write(path,dict):
    savemat(path,dict)

def txt_write(path,lines):
    out_file = open(path, "w")
    for line in lines:
        out_file.write(line)
        out_file.write('\n')
    out_file.close()

def pkl_write(path,data):
    pickle.dump(data, open(path, "wb"))


def hot_one_vector(y, max):
    import numpy as np
    labels_hot_vector = np.zeros((y.shape[0], max),dtype=np.int32)
    labels_hot_vector[np.arange(y.shape[0]), y] = 1
    return labels_hot_vector

def pkl_read(path):
    if(not os.path.exists(path)):
        return None;

    data = pickle.load(open(path, 'rb'))
    return data;

def touch_dir(path):
    if(not os.path.exists(path)):
        os.makedirs(path)

def touch_file_dir(file_path):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise




def last_tuple_idx(path):
    files =[f for f in os.listdir(path) if (f.endswith('.jpg') and not f.startswith('.'))];
    return len(files);

def get_file_name_ext(inputFilepath):
    filename_w_ext = os.path.basename(inputFilepath)
    filename, file_extension = os.path.splitext(filename_w_ext)
    return filename, file_extension

def get_latest_file(path,extension=''):
    files = get_files(path,extension=extension,append_base=True);
    return max(files, key=os.path.getctime)

def dir_empty(path):
    if os.listdir(path) == []:
        return True;
    else:
        return False;

def chkpt_exists(path):
    files = [f for f in os.listdir(path) if (f.find('.ckpt') > 0 and not f.startswith('.'))];
    if len(files):
        return True;
    return False;