function [ lights ] = gen_sin( x, range_weight, npi, theta )
%GEN_SIN 此处显示有关此函数的摘要
%   此处显示详细说明
    LIGHT_NUMBER = 10;
    step = range_weight/npi/(LIGHT_NUMBER-1);
    delta = 0:step:step*(LIGHT_NUMBER-1);
    x_array = x+delta;
    if x_array(LIGHT_NUMBER)>1 || x_array(LIGHT_NUMBER)<-1
        x_array = x-delta;
    end
    height = sqrt(1-x_array.*x_array);
    weight = sin(npi*pi*x_array);
    y_array = height.*weight;
    xy_mat = [x_array; y_array];
    rotate_mat = [cos(theta),-sin(theta);sin(theta), cos(theta)];
    new_xy_mat = rotate_mat*xy_mat;
    temp = new_xy_mat.*new_xy_mat;
    temp = temp(1,:)+temp(2,:);
    temp = 1-temp;
    new_z = -sqrt(temp);
    lights = [new_xy_mat; new_z];
    lights = lights.';
    x = -1:0.001:1;
    y = sqrt(1-x.*x);
    plot(lights(:,1),lights(:,2),x,y,x,-y);
end

