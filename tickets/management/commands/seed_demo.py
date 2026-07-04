from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from tickets.models import Category, Ticket, Comment

User = get_user_model()

# Demo users, one per role. Passwords are intentionally simple FOR THE DEMO
# ONLY and are documented in the README for the marker.
DEMO_USERS = [
    {"username": "admin_denver", "role": "ADMIN", "department": "IT Services", "password": "DemoPass123!"},
    {"username": "agent_sam",   "role": "AGENT", "department": "Service Desk",  "password": "DemoPass123!"},
    {"username": "agent_priya", "role": "AGENT", "department": "Field Support", "password": "DemoPass123!"},
    {"username": "user_leeds",  "role": "USER",  "department": "Leeds Depot",   "password": "DemoPass123!"},
    {"username": "user_courier","role": "USER",  "department": "Courier Ops",   "password": "DemoPass123!"},
]

# EVRi-relevant IT categories.
CATEGORIES = [
    ("Handheld Scanner", "Zebra/handheld device faults at depots and on rounds."),
    ("Courier App",      "Issues with the courier mobile application."),
    ("Depot WMS",        "Warehouse management system used in depots."),
    ("Network",          "Connectivity, Wi-Fi and VPN issues."),
    ("Account / Access", "Logins, passwords and permissions."),
    ("Facilities",       "Printers, label machines and on-site hardware."),
]

# Sample tickets: (title, description, category, priority, status).
TICKETS = [
    ("Zebra TC52 scanner won't connect to depot Wi-Fi",
     "Scanner at Leeds depot fails to join the WLAN after the latest update.",
     "Handheld Scanner", "HIGH", "OPEN"),
    ("Courier app crashes on parcel scan-out",
     "App closes unexpectedly when scanning parcels out for delivery.",
     "Courier App", "URGENT", "IN_PROGRESS"),
    ("Depot WMS showing incorrect stock counts",
     "Stock levels in the WMS do not match physical counts at the hub.",
     "Depot WMS", "HIGH", "NEW"),
    ("Cannot log in to tracking portal",
     "User receives 'invalid credentials' despite a correct password.",
     "Account / Access", "MEDIUM", "OPEN"),
    ("Label printer offline at Leeds hub",
     "Zebra label printer not responding; couriers cannot print labels.",
     "Facilities", "LOW", "RESOLVED"),
    ("VPN disconnects every few minutes",
     "Remote depot manager loses VPN connection intermittently.",
     "Network", "MEDIUM", "OPEN"),
    ("New starter needs courier app access",
     "Onboarding a new courier who requires app credentials.",
     "Account / Access", "LOW", "NEW"),
    ("Handheld battery draining within two hours",
     "Field scanners not holding charge for a full shift.",
     "Handheld Scanner", "MEDIUM", "IN_PROGRESS"),
]


class Command(BaseCommand):
    help = "Seed the database with EVRi demo data (idempotent)."

    def handle(self, *args, **options):
        # --- Users ---
        users = {}
        for spec in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=spec["username"],
                defaults={"role": spec["role"], "department": spec["department"]},
            )
            if created:
                user.set_password(spec["password"])  # Hashes the password.
                user.save()
            users[spec["username"]] = user
        self.stdout.write(self.style.SUCCESS(f"Users ready: {len(users)}"))

        # --- Categories ---
        categories = {}
        for name, desc in CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                name=name, defaults={"description": desc}
            )
            categories[name] = cat
        self.stdout.write(self.style.SUCCESS(f"Categories ready: {len(categories)}"))

        # --- Tickets ---
        requesters = [users["user_leeds"], users["user_courier"]]
        agents = [users["agent_sam"], users["agent_priya"]]
        created_count = 0
        for i, (title, desc, cat_name, priority, status) in enumerate(TICKETS):
            ticket, created = Ticket.objects.get_or_create(
                title=title,
                defaults={
                    "description": desc,
                    "category": categories[cat_name],
                    "created_by": requesters[i % len(requesters)],
                    # Assign roughly half to an agent, leave the rest unassigned.
                    "assigned_to": agents[i % len(agents)] if i % 2 == 0 else None,
                    "priority": priority,
                    "status": status,
                },
            )
            if created:
                created_count += 1
                # Add a public comment, and one internal note, to the first ticket
                # so the internal-visibility rule has data to demonstrate.
                if i == 0:
                    Comment.objects.create(
                        ticket=ticket, author=agents[0],
                        body="Investigating — looks like a WLAN profile issue.",
                    )
                    Comment.objects.create(
                        ticket=ticket, author=agents[0], is_internal=True,
                        body="Internal: escalate to network team if not fixed by EOD.",
                    )
        self.stdout.write(self.style.SUCCESS(f"Tickets created: {created_count}"))
        self.stdout.write(self.style.SUCCESS("Seed complete."))