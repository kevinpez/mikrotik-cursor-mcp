#!/bin/bash
#
# Daily Operations Script for Multi-Site Manager
# Run this daily via cron for automated management
#
# Add to crontab: 0 2 * * * /path/to/daily_operations.sh
#

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANAGER_DIR="$(dirname "$SCRIPT_DIR")"
REPORT_DIR="$MANAGER_DIR/reports"
LOG_FILE="$MANAGER_DIR/logs/daily_operations.log"

# Email settings (configure if you want email notifications)
SEND_EMAIL=false
EMAIL_TO="admin@example.com"

# Create necessary directories
mkdir -p "$REPORT_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "===== Starting Daily Operations ====="

cd "$MANAGER_DIR" || exit 1

# 1. Backup all sites
log "Creating backups..."
if python site_manager.py backup create --all >> "$LOG_FILE" 2>&1; then
    log "✓ Backups completed successfully"
else
    log "✗ Backup failed!"
fi

# 2. Health check
log "Performing health checks..."
TODAY=$(date '+%Y-%m-%d')
HEALTH_REPORT="$REPORT_DIR/health_${TODAY}.html"

if python site_manager.py health --all --format html --output "$HEALTH_REPORT" >> "$LOG_FILE" 2>&1; then
    log "✓ Health check completed: $HEALTH_REPORT"
else
    log "✗ Health check failed!"
fi

# 3. Get all sites status
log "Checking site status..."
if python site_manager.py status >> "$LOG_FILE" 2>&1; then
    log "✓ Status check completed"
else
    log "✗ Status check failed!"
fi

# 4. Cleanup old backups (keep 30 days)
log "Cleaning up old backups..."
find "$MANAGER_DIR/backups" -name "*.rsc" -type f -mtime +30 -delete 2>> "$LOG_FILE"
log "✓ Old backups cleaned up"

# 5. Cleanup old reports (keep 14 days)
log "Cleaning up old reports..."
find "$REPORT_DIR" -name "*.html" -type f -mtime +14 -delete 2>> "$LOG_FILE"
log "✓ Old reports cleaned up"

# 6. Send email notification (if configured)
if [ "$SEND_EMAIL" = true ]; then
    log "Sending email notification..."
    SUBJECT="MikroTik Multi-Site Daily Report - $TODAY"
    BODY="Daily operations completed. Health report attached."
    
    # Simple email (requires mail command)
    if command -v mail &> /dev/null; then
        echo "$BODY" | mail -s "$SUBJECT" -A "$HEALTH_REPORT" "$EMAIL_TO"
        log "✓ Email sent to $EMAIL_TO"
    else
        log "⚠ mail command not found, skipping email"
    fi
fi

log "===== Daily Operations Completed ====="
log ""

exit 0

