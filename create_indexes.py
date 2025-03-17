
from app import create_app
from db_init import db

def create_indexes():
    app = create_app()
    with app.app_context():
        # Create indexes for common queries
        db.session.execute('CREATE INDEX IF NOT EXISTS idx_events_start_date ON events (start_date)')
        db.session.execute('CREATE INDEX IF NOT EXISTS idx_events_status ON events (status)')
        db.session.execute('CREATE INDEX IF NOT EXISTS idx_events_category ON events (category)')
        db.session.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)')
        db.session.commit()

if __name__ == '__main__':
    create_indexes()
