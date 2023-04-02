load('rawop/mat_init_pos.mat')
pm=positionmatrix;pm=cell2mat(pm);
walls=double(walls);
walls=[walls;[15 7 30 7];[15 8 30 8]];
nr_agents=size(pm,1);
acclTime=0.5;
bodyFactor=120000;
F=2000;
delta=0.08;
k=240000;
given_param=struct('ip',{acclTime,bodyFactor,F,delta,k,walls,nr_agents,pm});

iter=1
dt=0.1
walltestmat=[0,0];
veltestmat=[0,0];
pm(:,5)=0.8; 

% for veltest=2.5:0.5:5
% for walltest=12:-0.1:0.5
%     walls(4,4)=7.5-walltest/2;
%     walls(5,4)=7.5+walltest/2;

%     negwall=[15 7-5-walltest/2 15 7.5+walltest/2];
%     pm(:,5)=veltest;
    mat_pos=matcalc(given_param,iter,dt);
    save('rawop/mat_pos.mat','mat_pos')
%     save(['finalmatwall' num2str(walltest) '.mat'],'finalmat')
%       save(['finalmatvel' num2str(veltest) '.mat'],'finalmat')
%       veltestmat=[veltestmat;veltest,time]
%     walls
%     walltestmat=[walltestmat;walltest,time]
% end
% save('finalmat.mat','finalmat')

% am=[posx,posy,mass,radius*50,velx,vely,time,nr_agent,goal_check]
function mat_pos=matcalc(given_param,iter,dt)
   [acclTime,bodyFactor,F,delta,k,walls,nr_agents,pm]=given_param.ip;
    time=0;
    am=pm; am(:,[5,6,7,8])=0;
    am(:,9)=1;am(:,10)=0;
    mat_pos=am;

    mat_wf_x=zeros(nr_agents,size(walls,1));mat_wf_y=mat_wf_x;
    mat_pf_x=zeros(nr_agents,nr_agents);mat_pf_y=mat_pf_x;

    for i=1:iter
        af=actualforce(given_param,am);
        [wf_x,wf_y]=wallforce(given_param,am);  swf=[sum(wf_x,2) sum(wf_y,2)];
        [pf_x,pf_y]=peopleforce(given_param,am);spf=[sum(pf_x,2) sum(pf_y,2)];

        mat_wf_x=[mat_wf_x;wf_x];
        mat_wf_y=[mat_wf_y;wf_y];
        mat_pf_x=[mat_pf_x;pf_x];
        mat_pf_y=[mat_pf_y;pf_y];

        change=(af+spf+swf)./pm(:,3)*dt;
        change(change>2)=0;
        am(:,[5,6])=am(:,[5,6])+change;
        am(:,[1,2])=am(:,[1,2])+am(:,[5,6]).*dt;
        time=time+dt;
        am(:,7)=time;
        am(:,8)=[1:nr_agents];
%         modify this
        am(:,9)=(am(:,1)<15 & am(:,1)>0 & am(:,2)<30 & am(:,2)>0);
    %     numberOfZeros = sum(am(:,9)==0)

        if am(:,9)==0
            break
        end

        mat_pos=[mat_pos;am];
    end
save('rawop/mat_force.mat','mat_wf_x','mat_wf_y','mat_pf_x','mat_pf_y')
end

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

function [pf_x,pf_y]= peopleforce(given_param,am)
   [acclTime,bodyFactor,F,delta,k,walls,nr_agents,pm]=given_param.ip;
    pf_x=zeros(nr_agents,nr_agents);
    pf_y=zeros(nr_agents,nr_agents);
    for i=1:nr_agents
        pf=zeros(1,2);
        r_i=am(i,4);
        d_i=am(i,[1,2]);

        for j=i:nr_agents
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

            pf_x(i,j)=pf(1);
            pf_y(i,j)=pf(2);
        end
    end
    pf_x=pf_x-pf_x';
    pf_y=pf_y-pf_y';
%     spf;

end

function [wf_x,wf_y]= wallforce(given_param,am)
   [acclTime,bodyFactor,F,delta,k,walls,nr_agents,pm]=given_param.ip;
    wf_x=zeros(nr_agents,size(walls,1));
    wf_y=zeros(nr_agents,size(walls,1));
%     swf=zeros(nr_agents,2);
    for i=1:nr_agents
        wf=zeros(1,2);
        r_i=am(i,4);

            for j=1:size(walls)
                [d_iw,e_iw]=test_walldistance(am(i,[1,2]),walls(j,:));

                  t_iw=[-e_iw(2),e_iw(1)];

                wf=1*(-F.*exp((r_i-d_iw)/(delta)).*e_iw-bodyFactor.*max(r_i-d_iw,0).*e_iw)-k*max(r_i-d_iw,0).*dot(am(i,5:6),t_iw).*t_iw;
                wf(isnan(wf))=0;
                wf=wf.*am(i,9);

                wf_x(i,j)=wf(1);
                wf_y(i,j)=wf(2);
            end
    end

end

function af_xy = actualforce(given_param,am)
   [acclTime,bodyFactor,F,delta,k,walls,nr_agents,pm]=given_param.ip;
   af_xy=zeros(nr_agents,2); 
   af=zeros(1,2);
    for i=1:nr_agents
        direc=znorm(pm(i,[6,7])-am(i,[1,2]));
        af=(pm(i,5).*direc-am(i,[5,6])).*pm(i,3)/acclTime;
%         blindcheck
        if am(i,10)==1
            af(i,1)=0;
        end
      
        af=af.*am(i,9);
        af_xy(i,:)=af;
    end
end