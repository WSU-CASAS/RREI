from irl import *
global input_healthy_dir1
global root_dir


class MDP:
        def __init__(self, x=0, y=0, a = np.zeros(9), p = np.zeros(9)):
            self.x = x
            self.y = y 
            self.a = a
            self.p = p


def make_new_dir(input_path):
    try: 
        os.makedirs(input_path)
    except OSError:
        if not os.path.isdir(input_path):
            raise

def look_for_room(cell_id, home_name):
    if home_name == "tm002":
        room_cell_match = rooms_cells.tm002_room_cell_match
    elif home_name == "tm001":
        room_cell_match = rooms_cells.tm001_room_cell_match
    elif home_name == "hh105":
        room_cell_match = rooms_cells.hh105_room_cell_match
    elif home_name == "hh109":
        room_cell_match = rooms_cells.hh109_room_cell_match
    elif home_name == "hh107":
        room_cell_match = rooms_cells.hh107_room_cell_match
    elif home_name == "hh127":
        room_cell_match = rooms_cells.hh127_room_cell_match
    elif home_name == "aruba":
        room_cell_match = rooms_cells.aruba_room_cell_match
    elif home_name == "hh124":
        room_cell_match = rooms_cells.hh124_room_cell_match
    elif home_name == "hh104":
        room_cell_match = rooms_cells.hh104_room_cell_match
    elif home_name == "hh122":
        room_cell_match = rooms_cells.hh122_room_cell_match

    return_names = []
    for name, cell_ids in room_cell_match.items():
        if cell_id in cell_ids: 
            return_names.append(name)
        
    return return_names


def calculate_feature_matrix(data, home_name):
    room_duration ={}
    room_names = rooms_cells.room_names

    for name in room_names:
        room_duration[name] = 0.0

    feature_values = []

    for d in data: 
        l_split = re.split(',', d)

        if len(l_split) == 1:
            l_split = re.split('\t', d)

        step_duration = float(l_split[2].strip())

        cell_id = [int(l_split[0]), int(l_split[1])]
        room_name = look_for_room(cell_id, home_name)
        if room_name == None: 
            continue
        for i in room_name:
            room_duration[i] += step_duration

    for name in room_names: 
        feature_values.append(room_duration[name])
    return feature_values


def output_parameters(dir_name, input_healthy_dir1):
    if dir_name == input_healthy_dir1:
        if home_id in ['tm001', 'tm002']:
            out_name = "H"
        else: 
            out_name = 'H1'
    else: 
        if home_id in ['tm001', 'tm002']:
            out_name = "NH"
        else:
            out_name = "H2"
    return out_name


def file_home_name(file):
    flag = True
    fin_file_path = re.split(r'\/', file)
    file_name = str(fin_file_path[-1][6:-4])
    home_name = str(fin_file_path[-1][:5]) #home name
    return file_name,home_name, flag

def dir_path_split(path):
    flag = True
    fin_file_path = re.split(r'\/', path)
    folder = str(fin_file_path[-1])
    home_id = str(fin_file_path[-2]) #home name

    print("home_id", home_id)
    return home_id

def readin_data(file):                
    fin = open(file, 'r')
    data = fin.readlines()
    fin.close()
    return data

def one_traj_feature(file):
    data = readin_data(file)
    for l in data: 
        l_split = re.split(',', l)
        if len(l_split) == 1:
            l_split = re.split('\t', l)
        one_traj.append([int(l_split[0].strip()), int(l_split[1].strip())])
        one_feature.append([float(l_split[2].strip())])
    return data, one_traj, one_feature

def transform_feature_expectationxpectation(feature_matrix):
    scaler = MinMaxScaler()
    new_scaler = scaler.fit(feature_matrix)
    transformed_feature = new_scaler.transform(feature_matrix)
    feature_expectationxpectation =sum(transformed_feature)/len(feature_matrix)

    return transformed_feature, feature_expectationxpectation

def select_spot_cell_by_home_name(home_name):
    res = ''
    if home_name == 'tm001':
        res = rooms_cells.tm001_spot_cell_match
    elif home_name == 'tm002':
        res = rooms_cells.tm002_spot_cell_match
    elif home_name == 'hh105':
        res = rooms_cells.hh105_spot_cell_match
    elif home_name == "hh109":
        res = rooms_cells.hh109_spot_cell_match
    elif home_name == "hh107":
        res = rooms_cells.hh107_spot_cell_match
    elif home_name == "hh127":
        res = rooms_cells.hh127_spot_cell_match
    elif home_name == "aruba":
        res = rooms_cells.aruba_spot_cell_match
    elif home_name == "hh124":
        res = rooms_cells.hh124_spot_cell_match
    elif home_name == "hh104":
        res = rooms_cells.hh104_spot_cell_match
    elif home_name == "hh122":
        res = rooms_cells.hh122_spot_cell_match
    return res

def number_events(home_name, data):

    event_list = rooms_cells.number_activities
    spot_cell_match = select_spot_cell_by_home_name(home_name)

    numbers = {}
    res = []

    for d in data: 
        # print("d",d)
        
        d_split = re.split(',', d)
        if len(d_split) == 1: 
            d_split = re.split('\t', d)

        sensor_id = str(d_split[1].strip())
        for k, v in spot_cell_match.items():
            if sensor_id == v:
                numbers[k] = numbers.get(k, 0) + 1
    for event in event_list:
        if event in numbers.keys():
            res.append(numbers[event])
        else: 
            res.append(0)

    return res

def other_features(home_name,out_name, file_name):

    path = root_dir
    if home_name in ['hh104', 'hh122', 'aruba', 'hh124']:
        file = path + home_name + "/uh_daily_segment_jitters/" + file_name + ".txt"
    else:
        file = path + home_name + "/h_daily_segment_jitters/" + file_name + ".txt"

    f = open(file, 'r')
    data = f.readlines()
    f.close()

    return number_events(home_name, data)


if __name__ == '__main__':

    home_name, month = sys.argv[1], sys.argv[2]
    input_healthy_dir1 = "../hh109_temp_test2/"
    root_dir = "../"

    if home_name in ['hh105', 'hh109', 'hh107', 'hh127']:
        fout_path1 = root_dir + "healthy_labelled.txt"
        fout_path2 = root_dir + "date_healthy_labelled.txt" 
        label = "1"
    else: 
        fout_path1 = root_dir + "uhealthy_labelled.txt"
        fout_path2 = root_dir + "date_uhealthy_labelled.txt"
        label = "-1"


    fout1 = open(fout_path1, 'w')
    fout2 = open(fout_path2, 'w')

    theta_list = []

    home_id = home_name

    theta_dictionary = {}

    new_sub_dir_path = input_healthy_dir1 + str(month) + "/" 
    for dir_name in [new_sub_dir_path]:
        out_name = output_parameters(dir_name, input_healthy_dir1)
        cases,feature_matrix = [],[]
        print("")          
        print("dir_name", dir_name)

    	
        for file in glob.glob(os.path.join(dir_name, '*.txt')):
            file_name, home_name, flag = file_home_name(file)
            print("home_name, file_name", home_name, file_name)
            if not flag: continue
            if os.stat(file).st_size == 0:
                continue
            one_traj,one_feature = [],[]
            data, one_traj, one_feature = one_traj_feature(file)
            temp_feature = calculate_feature_matrix(data, home_name) + other_features(home_name,out_name,file_name)
            feature_matrix.append(temp_feature)
            cases.append([one_traj])

        objs = [MDP() for i in range(0, 72)]
        count_from_traj(cases, objs)
        policy_from_traj(objs)

        ratio=calculate_ratio_from_policies(cases,1/9.0,objs)
        transformed_feature, feature_expectation = transform_feature_expectationxpectation(feature_matrix)
        theta =gradient_func(ratio, transformed_feature ,0.9, feature_expectation, 1e-100)
        theta_dictionary[out_name] = theta

    print("theta", theta_dictionary)

    theta_str = ','.join(str(i) for i in theta)
    date_write_out_str = home_name + "_" + file_name + "\t" + theta_str + "\t" + label
    write_out_str = theta_str + "\t" + label

    fout1.write(write_out_str + "\n")
    fout2.write(date_write_out_str + "\n")
    fout1.close()
    fout2.close()
