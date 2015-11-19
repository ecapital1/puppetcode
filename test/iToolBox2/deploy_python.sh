#/bin/sh

OLD_DIR=`pwd`
PROGRAM_DIR=`dirname $0`
SRC_DIR=$PROGRAM_DIR/src/
LOCAL_DST_DIR=/ittools/
REMOTE_DST_DIR=/ittools/
SHELL_DIR=$PROGRAM_DIR/shell

NFS_SERVER="epcau-srv-it"
NFS_USER="epoch"



# Copy to local directory.
echo "rsync -av --delete $SRC_DIR $LOCAL_DST_DIR"
rsync -av --delete $SRC_DIR $LOCAL_DST_DIR


# Make all python script executable.
find $LOCAL_DST_DIR -name *.py | xargs chmod ugo+x

echo "rsync -av --delete $SHELL_DIR $LOCAL_DST_DIR"
rsync -av --delete $SHELL_DIR $LOCAL_DST_DIR


# Start to delopy ittools to NFS Server.

echo "Start to delopy ittools to NFS Server"
rsync -avz --delete $LOCAL_DST_DIR ${NFS_USER}@${NFS_SERVER}:$REMOTE_DST_DIR


#PUSH TO RTS servers
RTSUSER=rts
RTSSERVERS="10.129.1.14"
#RTSSERVERS="10.128.1.12 10.128.1.14 10.129.1.14"
for server in $RTSSERVERS
do
	echo "pushing scripts to RTS server $server."
	rsync -avz --delete $LOCAL_DST_DIR ${RTSUSER}@${server}:/srv/ittools/python/
	echo "Done!"
done


cd $OLD_DIR
