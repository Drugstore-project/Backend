from app.database import SessionLocal
from app.models.user import User
from app.models.role import UserRole

def fix_client_roles():
    db = SessionLocal()
    
    # Get Client Role ID
    client_role = db.query(UserRole).filter(UserRole.name == "client").first()
    if not client_role:
        print("Client role not found!")
        return

    print(f"Client Role ID: {client_role.id}")

    # Find users who look like clients but have wrong role
    # Specifically looking for the one in the screenshot or similar
    users = db.query(User).all()
    
    for user in users:
        # Check if user looks like a client (email domain or specific email)
        if "client" in user.email.lower() or "@client.store" in user.email:
            if user.role_id != client_role.id:
                print(f"Fixing user {user.name} ({user.email}). Role {user.role_id} -> {client_role.id}")
                user.role_id = client_role.id
                db.add(user)
    
    db.commit()
    print("Done fixing roles.")
    db.close()

if __name__ == "__main__":
    fix_client_roles()
