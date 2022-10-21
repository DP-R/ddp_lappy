load('positionmatrix.mat')
pm=positionmatrix;
pm=cell2mat(pm);

acclTime=0.5;
bodyFactor=12000;
F=2000;
delta=4;


time=0;
am=pm; am(:,[5,6,7,8])=0;
am(:,9)=1;
finalmat=am;
for i=1:10000

    swf=zeros(nr_agents,2);
    spf=zeros(nr_agents,2);
    af=zeros(nr_agents,2);

for j=1:nr_agents
    r_i=am(:,4);
    d_i=am(:,[1,2]);
    r_ij=r_i+r_i(j);
    d_ij=d_i(j,:)-d_i;

    mod_d_ij=dista(d_ij);
    e_ij=d_ij./mod_d_ij;
    pf=F.*exp((r_ij-mod_d_ij)/(delta)).*e_ij+bodyFactor.*max(r_ij-mod_d_ij,0).*e_ij;
    pf(isnan(pf))=0;
    pf=pf.*am(:,9);

    spf(j,:)=sum(pf);
end
    
    wf=zeros(size(pf));
for i=1:size(walls)
    [d_iw,e_iw]=test_walldistance(am(:,[1,2]),walls(i,:));
    wf=wf-F.*exp((r_i-d_iw)/(delta)).*e_iw+bodyFactor.*max(r_i-d_iw,0).*e_iw;

end
    wf=wf.*am(:,9);
    swf=wf;    

    dt=0.01;
    direc=dotta(pm(:,[6,7])-am(:,[1,2]));


    af=(pm(:,5).*direc-am(:,[5,6])).*pm(:,3)/acclTime;
    af=af.*am(:,9);
    am(:,[5,6])=am(:,[5,6])+(af+spf+swf)./pm(:,3)*dt;
    am(:,[1,2])=am(:,[1,2])+am(:,[5,6]).*am(:,9)*dt;
    time=time+dt;
    am(:,7)=time;
    am(:,8)=[1:nr_agents];
    am(:,9)=(am(:,1)<700);
    if am(:,9)==0
        break
    end
    finalmat=[finalmat;am];
end

save('finalmat.mat','finalmat')
function [dist,npw]=test_walldistance(point, wall)
    p0=wall(1,[1,2]);
    p1=wall(1,[3,4]);
    d=p1-p0;
    ymp0=point-p0;

    t=d(1).*ymp0(:,1)+d(2).*ymp0(:,2);
    t=t./dista(d);

    if t <= 0.0
        dist = dista(ymp0);
        cross = p0 + t.*d;
%         npw = (cross-point)
    elseif t >= 1.0
        ymp1 = point-p1;
        dist = dista(ymp1);
        cross = p0 + t.*d;
%         npw = normalize(cross-point)
    else
        cross = p0 + t.*d;
        a=cross-point;
        dist = dista(a);
    end
    a=cross-point;
    npw = dotta(a);

end

function dotta=dotta(mat)
    dotta=mat./dista(mat);
end

function dista=dista(mat)
    dista=sqrt(mat(:,1).^2+mat(:,2).^2);
end
