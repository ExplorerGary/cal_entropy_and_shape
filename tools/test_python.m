% test_python.m
% Purpose: Test py_utilities and entropy calculation on .pt files

% === Step 1: 添加 Python 模块路径（仅第一次需要） ===
py_utils_path = '/gpfsnyu/scratch/zg2598/HELPER_FUNCTIONS/cal_entropy_and_shape/tools';
if count(py.sys.path, py_utils_path) == 0
    insert(py.sys.path, int32(0), py_utils_path);
end

% === Step 2: 导入 py_utilities 模块 ===
pyu = py.importlib.import_module('py_utilities');

% === Step 3: 使用 scan_pt() 扫描 .pt 文件 ===
target_dir = '/gpfsnyu/scratch/zg2598/Qwen/OUT/COMMUNICATION_LOG/';
pt_files = pyu.scan_pt(target_dir);

% 转为 MATLAB cell 数组（便于索引）
pt_files_cell = cell(pt_files);

% 限制最多处理前 10 个文件
n_files = min(10, numel(pt_files_cell));

fprintf('找到 %d 个 pt 文件，处理前 %d 个：\n\n', numel(pt_files_cell), n_files);

% === Step 4: 逐个读取 pt 文件并计算熵 ===
for i = 1:n_files
    pt_path = char(pt_files_cell{i});  % Python str → MATLAB char
    try
        % Step 4.1: 调用 read_pt() 读取 numpy array
        arr_np = pyu.read_pt(pt_path);
        arr = double(arr_np);  % 转为 MATLAB array

        % Step 4.2: 调用 cal_entropy 计算熵
        H = cal_entropy(arr);

        % Step 4.3: 显示结果
        fprintf('[%02d] %s\n    entropy = %.5f\n\n', i, pt_path, H);
    catch ME
        warning('[%02d] 处理失败: %s', i, pt_path);
        disp(getReport(ME));
    end
end