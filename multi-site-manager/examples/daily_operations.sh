#!/bin/bash
#
# Daily Operations Script for Multi-Site Manager
#
# Purpose: Automated backups, health checks, and cleanup
# Schedule: Add to crontab with: 0 2 * * * /path/to/daily_operations.sh
#
# Features:
# - Creates backups of all sites
# - Generates HTML health report
# - Cleans up old backups (30+ days)
# - Cleans up old reports (14+ days)
# - Optional email notifications

# ============================================================================
# CONFIGURATION - Edit these values
# ============================================================================

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANAGER_DIR="$(dirname "$SCRIPT_DIR")"
REPORT_DIR="$MANAGER_DIR/reports"
LOG_FILE="$MANAGER_DIR/logs/daily_operations.log"

# Email settings
SEND_EMAIL=false                    # Set to true to enable email
EMAIL_TO="admin@example.com"        # Your email address
EMAIL_FROM="mikrotik@example.com"   # From address

# Retention policies (days)
BACKUP_RETENTION=30
REPORT_RETENTION=14

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

# 4. Cleanup old backups
log "Cleaning up old backups (keeping $BACKUP_RETENTION days)..."
find "$MANAGER_DIR/backups" -name "*.rsc" -type f -mtime +$BACKUP_RETENTION -delete 2>> "$LOG_FILE"
BACKUP_COUNT=$(find "$MANAGER_DIR/backups" -name "*.rsc" -type f | wc -l)
log "✓ Old backups cleaned up ($BACKUP_COUNT backups remaining)"

# 5. Cleanup old reports
log "Cleaning up old reports (keeping $REPORT_RETENTION days)..."
find "$REPORT_DIR" -name "*.html" -type f -mtime +$REPORT_RETENTION -delete 2>> "$LOG_FILE"
REPORT_COUNT=$(find "$REPORT_DIR" -name "*.html" -type f | wc -l)
log "✓ Old reports cleaned up ($REPORT_COUNT reports remaining)"

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

