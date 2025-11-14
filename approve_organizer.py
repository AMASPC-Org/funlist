import sys
import logging
from datetime import datetime

from app import create_app
from db_init import db
from models import User, Organization

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def set_status(email: str, approve: bool) -> bool:
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            logger.error("User with email %s not found.", email)
            return False

        organization = user.organization
        if not organization:
            logger.error("User %s does not have an organizer application.", email)
            return False

        if approve:
            organization.status = "approved"
            organization.approved_at = datetime.utcnow()
            organization.denied_at = None
            user.organizer_status = "approved"
            user.organizer_approved_at = datetime.utcnow()
            user.organizer_denied_at = None
            user.is_organizer = True
            user._is_event_creator = True
            logger.info("Approved organizer application for %s", email)
        else:
            organization.status = "denied"
            organization.denied_at = datetime.utcnow()
            organization.approved_at = None
            user.organizer_status = "denied"
            user.organizer_denied_at = datetime.utcnow()
            user.organizer_approved_at = None
            user.is_organizer = False
            user._is_event_creator = False
            logger.info("Denied organizer application for %s", email)

        db.session.commit()
        return True


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in {"approve", "deny"}:
        print("Usage: python approve_organizer.py [approve|deny] user@example.com")
        sys.exit(1)

    action = sys.argv[1] == "approve"
    email = sys.argv[2]
    success = set_status(email, action)
    sys.exit(0 if success else 1)
