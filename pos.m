load('positionmatrix.mat')
pm=positionmatrix;pm=cell2mat(pm);
walls=double(walls);
acclTime=0.5;
bodyFactor=120000;
F=2000;
delta=0.08*50;

  negativewall=[700 375 700 425];
time=0;
am=pm; am(:,[5,6,7,8])=0;
am(:,9)=1;
finalmat=am;
for i=1:1000

    [swf,spf,af]=deal(zeros(nr_agents,2));
%     spf=zeros(nr_agents,2);
%     af=zeros(nr_agents,2);

for j=1:nr_agents
    r_i=am(:,4);
    d_i=am(:,[1,2]);
    r_ij=r_i+r_i(j);
    d_ij=d_i(j,:)-d_i;

    mod_d_ij=zmod(d_ij);
    e_ij=d_ij./mod_d_ij;
    pf=F.*exp((r_ij-mod_d_ij)/(delta)).*e_ij+bodyFactor.*max(r_ij-mod_d_ij,0).*e_ij;
    pf(isnan(pf))=0;
    pf=pf.*am(:,9);

    spf(j,:)=sum(pf);
end
    
    wf=swf;
for i=1:size(walls)
    d_iw=zeros(nr_agents,1);
    e_iw=zeros(nr_agents,2);
    for p = 1:nr_agents
%     disp('start')
    [a,b]=test_walldistance(pm(p,[1,2]),walls(i,:));
    d_iw(p)=a;
    e_iw(p,:)=b;
    end
%     zt
%     np
%     [d_iw,e_iw]=test_walldistance(am(:,[1,2]),walls(i,:));
    wf=wf+1*(+F.*exp((r_i-d_iw)/(delta)).*e_iw+bodyFactor.*max(r_i-d_iw,0).*e_iw);
	wf;
end

% [d_iw,e_iw]=test_walldistance(am(:,[1,2]),negativewall);

% wf=wf-(+F.*exp((r_i-d_iw)/(delta)).*e_iw+bodyFactor.*max(r_i-d_iw,0).*e_iw);

    wf=wf.*am(:,9);
    swf=wf;   

    dt=0.01;
    direc=znorm(pm(:,[6,7])-am(:,[1,2]));

    af=(pm(:,5).*direc-am(:,[5,6])).*pm(:,3)/acclTime;
    af=af.*am(:,9);
	swf;
    am(:,[5,6])=am(:,[5,6])+(af+spf+swf)./pm(:,3)*dt;
    am(:,[1,2])=am(:,[1,2])+am(:,[5,6]).*dt;
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
    t=zdot(d,ymp0)./zdot(d,d);

    if t <= 0.0
        dist = zmod(ymp0);
        cross = p0 + t.*d;

    elseif t >= 1.0
        ymp1 = point-p1;
        dist = zmod(ymp1);
        cross = p0 + t.*d;

    else
        cross = p0 + t.*d;
        a=cross-point;
        dist = zmod(a);
    end
    a=cross-point;
    npw = znorm(a);
%     disp(dist)
%    disp(npw)
    % doubtful on direction of normal force from the wall when crowd is away from the edge
end

function zdot=zdot(a,b)
    zdot=a(:,1).*b(:,1)+a(:,2).*b(:,2);
end

function znorm=znorm(a)
    znorm=a./zmod(a);
end

function zmod=zmod(a)
    zmod=sqrt(zdot(a,a));
end
