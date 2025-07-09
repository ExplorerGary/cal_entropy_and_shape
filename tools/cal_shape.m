function [params_opt, iter_exceeded] = cal_shape(data)
    % GGD
    num_bins = 10000;
    [bin_counts, bin_edges] = histcounts(data, num_bins, 'Normalization', 'pdf');
    x_centers = (bin_edges(1:end-1) + bin_edges(2:end)) / 2;

    initial_guess = [mean(data), std(data), 2];

    % 清空历史警告
    lastwarn('');

    % 执行拟合
    params_opt = mle(data, ...
        'pdf', @(x, mu, beta, gamma) generalized_gaussian_pdf(x, mu, beta, gamma), ...
        'start', initial_guess, ...
        'options', statset('MaxIter', 5000, 'MaxFunEvals', 5000));

    % 捕捉警告是否为 max_iter 超限
    [warnMsg, ~] = lastwarn;
    if contains(warnMsg, 'Iteration limit exceeded')
        iter_exceeded = 1;
    else
        iter_exceeded = 0;
    end
end