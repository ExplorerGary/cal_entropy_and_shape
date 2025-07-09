% --- 辅助函数 ---
function H = cal_entropy(data)
    % convert to double:
    data = double(data);

    % 归一化到0~1
    data_r = rescale(double(data));

    % 计算熵，调用MATLAB内置函数
    H = entropy(data_r);
end