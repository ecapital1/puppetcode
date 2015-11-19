#/bin/sh
# add comment
OLD_DIR=`pwd`
PROGRAM_DIR=`dirname $0`
SRC_DIR=$PROGRAM_DIR/src/
LOCAL_DST_DIR=/ittools/
REMOTE_DST_DIR=/ittools/
SHELL_DIR=$PROGRAM_DIR/shell

NFS_SERVER="epcau-srv-it"
NFS_USER="epoch"

# Copy to local directory.
rsync -av --delete $SRC_DIR $LOCAL_DST_DIR

rsync -av --delete $SHELL_DIR $LOCAL_DST_DIR

# Copy other useful utilities files
#for script in `ls *.sh`
#do
#	chmod ugo+x $script
#	echo "Copying $script to $LOCAL_DST_DIR"
#	cp -p $script $LOCAL_DST_DIR
#done

# Start to delopy ittools to NFS Server.

#echo "Start to delopy ittools to NFS Server"
#rsync -avz --delete $LOCAL_DST_DIR ${NFS_USER}@${NFS_SERVER}:$REMOTE_DST_DIR


cd $OLD_DIR
