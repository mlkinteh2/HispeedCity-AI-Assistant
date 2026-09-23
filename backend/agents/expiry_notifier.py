"""
Expiry Notifier Agent

Scans the MongoDB database for active parking subscriptions
that are expiring in the next 30 days and sends email reminders.
Can be run via cron or Windows Task Scheduler.
"""

import os
import sys
import argparse
import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests

from motor.motor_asyncio import AsyncIOMotorClient
import certifi
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env", override=True)
load_dotenv(ROOT_DIR / "parking-registration" / "backend" / ".env", override=True)

MONGO_URL = os.environ.get("MONGO_URL") or os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME", "hispeedcity")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

if not MONGO_URL:
    print("Error: MONGO_URL or MONGODB_URI must be set.")
    sys.exit(1)


def send_reminder_email(to_email: str, customer_name: str, plate: str, expiry_date: str, parking_type: str, portal_url: str = "https://www.hispeedcity.com/index.html") -> bool:
    """Send an expiry reminder email using Resend API."""
    if not RESEND_API_KEY:
        print("Error: RESEND_API_KEY not set. Cannot send email.")
        return False

    subject = f"Action Required: Your HispeedCity Parking Expires Soon ({plate})"
    
    text_body = (
        f"Dear {customer_name},\n\n"
        f"This is a friendly reminder that your {parking_type} parking for vehicle {plate} "
        f"will expire on {expiry_date}.\n\n"
        f"To ensure uninterrupted access, please renew your subscription via our portal: {portal_url}\n\n"
        "HISPEEDCITY SDN BHD\n"
        "We make things easy!\n"
        "Thank You"
    )
    
    html_body = (
        f"<p>Dear {customer_name},</p>"
        f"<p>This is a friendly reminder that your <strong>{parking_type}</strong> parking for vehicle <strong>{plate}</strong> "
        f"will expire on <strong>{expiry_date}</strong>.</p>"
        f"<p>To ensure uninterrupted access, please renew your subscription via our portal: <a href='{portal_url}'>HispeedCity Portal</a></p>"
        f"<p><strong>HISPEEDCITY SDN BHD</strong></p>"
        f"<p>We make things easy!</p>"
        f"<p>Thank You</p>"
    )

    payload = {
        "from": "hi@hispeedcity.com",
        "to": [to_email],
        "subject": subject,
        "text": text_body,
        "html": html_body
    }

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False


async def run_expiry_check(dry_run=False):
    print(f"Starting Expiry Notifier Agent (Dry Run: {dry_run})")
    print(f"Connecting to MongoDB...")
    
    client = AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where() if 'localhost' not in MONGO_URL else None)
    db = client[DB_NAME]
    
    today = datetime.now(timezone.utc)
    target_date_str = (today + timedelta(days=30)).strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")

    print(f"Scanning for active subscriptions expiring between {today_str} and {target_date_str}...")

    # We check both applications and renewals
    collections = ['applications', 'renewals']
    total_notified = 0

    for coll_name in collections:
        collection = db[coll_name]
        
        # Query: 
        # - Status is Approved or Active
        # - expiryDate exists and is <= target_date_str and >= today_str
        # - Not notified in the last 7 days
        
        query = {
            "status": {"$in": ["Approved", "Active"]},
            "expiryDate": {
                "$exists": True,
                "$gte": today_str,
                "$lte": target_date_str
            }
        }
        
        cursor = collection.find(query)
        docs = await cursor.to_list(length=1000)
        
        for doc in docs:
            email = doc.get("email")
            if not email:
                continue
                
            customer_name = doc.get("fullName") or doc.get("customerName") or doc.get("contactPerson") or "Valued Customer"
            parking_type = doc.get("parkingType") or doc.get("renewalType") or "Season Parking"
            expiry_date = doc.get("expiryDate")
            
            # Extract plate
            plate = None
            if doc.get("vehicleNumber"):
                plate = doc.get("vehicleNumber")
            elif doc.get("vehicles") and len(doc.get("vehicles")) > 0:
                plate = doc.get("vehicles")[0].get("vehicleNumber")
            elif doc.get("vehiclePlateNumbers") and len(doc.get("vehiclePlateNumbers")) > 0:
                plate = doc.get("vehiclePlateNumbers")[0]
                
            if not plate:
                plate = "your vehicle"
                
            # Check last notified
            last_notified = doc.get("expiryNotifiedAt")
            if last_notified:
                # If we notified them in the last 7 days, skip
                if isinstance(last_notified, str):
                    try:
                        last_notified_date = datetime.fromisoformat(last_notified)
                        if (today - last_notified_date).days < 7:
                            continue
                    except:
                        pass
                elif isinstance(last_notified, datetime):
                    if (today - last_notified).days < 7:
                        continue

            print(f"Need to notify {customer_name} ({email}) - {plate} expires {expiry_date}")
            
            if not dry_run:
                success = send_reminder_email(
                    to_email=email,
                    customer_name=customer_name,
                    plate=plate,
                    expiry_date=expiry_date,
                    parking_type=parking_type
                )
                
                if success:
                    await collection.update_one(
                        {"_id": doc["_id"]},
                        {"$set": {"expiryNotifiedAt": datetime.now(timezone.utc)}}
                    )
                    total_notified += 1
            else:
                total_notified += 1

    print(f"Finished. Total notifications {'would be' if dry_run else 'were'} sent: {total_notified}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run HispeedCity Expiry Notifier Agent")
    parser.add_argument("--dry-run", action="store_true", help="Print who would be notified without sending emails")
    args = parser.parse_args()
    
    asyncio.run(run_expiry_check(dry_run=args.dry_run))
