# create-backup.sh
#!/bin/bash
BACKUP_DIR="backups"
mkdir -p $BACKUP_DIR
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

echo "Backing up PostgreSQL database..."
docker exec workout_postgres pg_dumpall -U workoutuser > $BACKUP_FILE

echo "Backup created: $BACKUP_FILE"
echo "Size: $(du -h $BACKUP_FILE | cut -f1)"