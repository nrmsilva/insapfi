-- Download database image
docker pull container-registry.oracle.com/database/express:latest

-- Create network inside docker
docker network create ords-database-network

-- Run Docker Oracle Databse
docker run -d --name apex_database --hostname apex_database --network=ords-database-network -p 1521:1521 -p 8080:8080 container-registry.oracle.com/database/express:latest

-- Connect to docker container and execute the folowing commands as sysdba
docker exec -it -u oracle apex_database sqlplus / as sysdba
> show pdbs
>			CON_ID CON_NAME                       OPEN MODE  RESTRICTED
>		---------- ------------------------------ ---------- ----------
>				 2 PDB$SEED                       READ ONLY  NO
>				 3 XEPDB1                         READ WRITE NO
> exit

--Execute script to set password
docker exec apex_database ./setPassword.sh apex_database_pw

-- Download ORDS image
docker pull container-registry.oracle.com/database/ords:latest

-- Create folder for Apex configuration
mkdir ./APEX

-- Create file with Apex configuration
echo 'CONN_STRING=sys/apex_database_pw@apex_database:1521/XEPDB1' > $(pwd)/APEX/conn_string.txt

-- Run ORDS image to initiate installation
docker run --name apex -v $(pwd)/APEX:/opt/oracle/variables --network=ords-database-network -p 8181:8181 container-registry.oracle.com/database/ords:latest
>INFO : Use below login credentials to first time login to APEX service:
>        Workspace: internal
>        User:      ADMIN
>		Password:  Welcome_1
-- Change password for APEX_PUBLIC_USER
docker exec -it -u oracle apex_database sqlplus sys/apex_database_pw@//localhost:1521/XEPDB1 as sysdba
> alter user APEX_PUBLIC_USER identified by apex_public_user_pw;
exit

-- Connect to APEX in the Browser
http://localhost:8181/ords
>Workspace: internal
>User:      ADMIN
>Password:  Welcome_1
--Change Password
-- NEW PW: Oracle123!
-- More info
https://medium.com/@luca-bindi/oracle-xe-and-apex-in-a-docker-container-25f00a2b8306
https://docs.oracle.com/en/database/oracle/oracle-rest-data-services/18.3/aelig/ORDS-reference.html#GUID-E4476C14-01B1-4EA4-94D3-73B92C8C9AB3


