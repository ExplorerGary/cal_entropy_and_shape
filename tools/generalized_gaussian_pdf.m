function y = generalized_gaussian_pdf(x, Mu, Beta, Gamma)
    % GENERALIZED_GAUSSIAN_PDF 
    %
    % inputs:
    %   x     - vertor
    %   Mu    - location parameter 
    %   Beta - scale parameter
    %   Gamma  - shape parameter

    gamma_val = gamma(1 / Gamma);
    norm_const = Gamma / (2 * Beta * gamma_val);

    abs_diff = abs(x - Mu);
    exp_term = exp(-(abs_diff ./ Beta).^Gamma);

    y = norm_const .* exp_term;

    y(y < eps) = eps;

    y = double(y);

end