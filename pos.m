load('positionmatrix.mat')
pm=positionmatrix;pm=cell2mat(pm);
walls=double(walls);

acclTime=0.5;
bodyFactor=120000;
F=2000;
delta=0.08;
k=240000;
walltestmat=[0,0];
veltestmat=[0,0];
pm(:,5)=0.8;

% for veltest=2.5:0.5:5
for walltest=12:-0.1:0.5
    walls(4,4)=7.5-walltest/2;
    walls(5,4)=7.5+walltest/2;

%     negwall=[15 7-5-walltest/2 15 7.5+walltest/2];
%     pm(:,5)=veltest;
time=0;
am=pm; am(:,[5,6,7,8])=0;
am(:,9)=1;
finalmat=am;

for i=1:50000
    af=actualforce(nr_agents,am,acclTime,bodyFactor,F,delta,k,pm);
    swf=wallforce(nr_agents,am,acclTime,bodyFactor,F,delta,k,pm,walls);
%     swf=swf-wallforce(nr_agents,am,acclTime,bodyFactor,F,delta,k,pm,negwall);
    spf=peopleforce(nr_agents,am,acclTime,bodyFactor,F,delta,k);
    dt=0.05;

% am=[posx,posy,mass,radius*50,velx,vely,time,nr_agent,goal_check]
    change=(af+spf+swf)./pm(:,3)*dt;
    change(change>2)=0;
    am(:,[5,6])=am(:,[5,6])+change;
    am(:,[1,2])=am(:,[1,2])+am(:,[5,6]).*dt;
    time=time+dt;
    am(:,7)=time;
    am(:,8)=[1:nr_agents];
    am(:,9)=(am(:,1)<15 & am(:,1)>0 & am(:,2)<15 & am(:,2)>0);
%     numberOfZeros = sum(am(:,9)==0)

    if am(:,9)==0
        break
    end

    % 
        % insert tunnel and update positions
    % 
    finalmat=[finalmat;am];
%     time
end
    save(['finalmatwall' num2str(walltest) '.mat'],'finalmat')
%       save(['finalmatvel' num2str(veltest) '.mat'],'finalmat')
%       veltestmat=[veltestmat;veltest,time]
%     walls
    walltestmat=[walltestmat;walltest,time]
end
% save('finalmat.mat','finalmat')

function [dist,npw]=test_walldistance(point, wall)
    p0=wall(1,[1,2]);
    p1=wall(1,[3,4]);
    d=p1-p0;
    % disp(wall)
    ymp0=point-p0;
    t=zdot(d,ymp0)./zdot(d,d);

    if t>=0 && t<=1
        cross = p0 + t.*d;
    elseif t>1
        cross=p1;
    else
        cross=p0;
    end
    a=cross-point;
    dist = zmod(a);
    
    npw = znorm(a);
%     table(point,wall,dist,npw)
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

function spldot=spldot(a,b)
    spldot=a(1,1).*b(:,1)+a(1,2).*b(:,2);
end

function spf= peopleforce(nr_agents,am,acclTime,bodyFactor,F,delta,k)
    spf=zeros(nr_agents,2);
    for i=1:nr_agents
        pf=zeros(1,2);
        r_i=am(i,4);
        d_i=am(i,[1,2]);

        for j=1:nr_agents
            r_ij=r_i+am(j,4);
            d_ij=d_i-am(j,1:2);

            mod_d_ij=zmod(d_ij);
            e_ij=d_ij./mod_d_ij;

            t_ij=[-e_ij(2),e_ij(1)];
            am_temp=(am(j,5:6)-am(i,5:6));
%         isNan(spldot(t_ij,am_temp))=0
            pf=F.*exp((r_ij-mod_d_ij)/(delta)).*e_ij+bodyFactor.*max(r_ij-mod_d_ij,0).*e_ij+k*max(r_ij-mod_d_ij,0).*dot(t_ij,am_temp).*t_ij;
            pf(isnan(pf))=0;
            pf=pf.*am(i,9);

            spf(i,:)=spf(i,:)+(pf);
        end
    end
    spf;

end

function swf= wallforce(nr_agents,am,acclTime,bodyFactor,F,delta,k,pm,walls)

    swf=zeros(nr_agents,2);
    for i=1:nr_agents
        wf=zeros(1,2);
        r_i=am(i,4);

            for j=1:size(walls)
                [d_iw,e_iw]=test_walldistance(am(i,[1,2]),walls(j,:));

                  t_iw=[-e_iw(2),e_iw(1)];

                wf=1*(-F.*exp((r_i-d_iw)/(delta)).*e_iw-bodyFactor.*max(r_i-d_iw,0).*e_iw)-k*max(r_i-d_iw,0).*dot(am(i,5:6),t_iw).*t_iw;
                wf(isnan(wf))=0;
                wf=wf.*am(i,9);

                swf(i,:)=swf(i,:)+wf;
            end
    end

end

function af = actualforce(nr_agents,am,acclTime,bodyFactor,F,delta,k,pm)
    af=zeros(nr_agents,2);
    direc=znorm(pm(:,[6,7])-am(:,[1,2]));
    af=(pm(:,5).*direc-am(:,[5,6])).*pm(:,3)/acclTime;
    af=af.*am(:,9);

end