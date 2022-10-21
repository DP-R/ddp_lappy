load('positionmatrix.mat')
pm=positionmatrix;
% walls=walls;
pm=cell2mat(pm);
acclTime=0.5;
bodyFactor=120000;
F=2000;
delta=0.05;
r_i=pm(:,4);
d_i=pm(:,[1,2]);

r_ij=r_i+r_i(1);
d_ij=d_i-d_i(1,:);

mod_d_ij=sqrt(d_ij(:,1).^2+d_ij(:,2).^2);
e_ij=d_ij./mod_d_ij;
pf=F.*exp((r_ij-mod_d_ij)/(delta)).*e_ij+bodyFactor.*max(r_ij-mod_d_ij,0).*e_ij
pf(isnan(pf))=0

wf=zeros(size(pf))
for i=1:size(walls)
    [d_iw,e_iw]=test_walldistance(pm(:,[1,2]),walls(i,:));
    wf=wf+F.*exp((r_i-d_iw)/(delta)).*e_iw+bodyFactor.*max(r_i-d_iw,0).*e_iw

end

dt=0.1
am=pm; am(:,[5,6,7,8])=0
af=(pm(:,5).*pm(:,[6,7])-am(:,[5,6])).*pm(:,3)/acclTime
am(:,[5,6])=am(:,[5,6])+(af+pf+wf).*dt
am(:,[1,2])=am(:,[5,6])*dt

function [dist,npw]=test_walldistance(point, wall)
    p0=wall(1,[1,2]);
    p1=wall(1,[3,4]);
    d=p1-p0;
    ymp0=point-p0;
%     point=pm(1,[1,2])
    t=d(1)*ymp0(:,1)+d(2)*ymp0(:,2);
    t=t./dot(d,d);
%     t = dot(d,ymp0)./dot(d,d)

    if t <= 0.0
        dist = sqrt(dot(ymp0',ymp0')');
        cross = p0 + t.*d;
%         npw = (cross-point)
    elseif t >= 1.0
        ymp1 = point-p1;
        dist = sqrt(dot(ymp1',ymp1')');
        cross = p0 + t.*d;
%         npw = normalize(cross-point)
    else
        cross = p0 + t.*d;
        a=cross-point;
        dist = sqrt(a(:,1).*a(:,1)+a(:,2).*a(:,2));
    end
    a=cross-point;
    npw = a./sqrt(dot(a',a')');

    end