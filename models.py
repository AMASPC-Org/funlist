        import logging
        from app import db
        from datetime import datetime
        from flask_login import UserMixin
        from sqlalchemy import or_
        from slugify import slugify  # Import the slugify library

        logger = logging.getLogger(__name__) #add logger


        class SearchableResource:
            @classmethod
            def search(cls, query):
                """Enhanced search implementation with logging"""
                try:
                    searchable_columns = cls.__searchable__ if hasattr(cls, '__searchable__') else []
                    if not searchable_columns:
                        logger.warning(f"No searchable columns defined for {cls.__name__}")
                        return []

                    # Split the search query into words and add related terms
                    search_terms = query.lower().split()
                    expanded_terms = []
                    for term in search_terms:
                        expanded_terms.append(term)
                        # Add common related terms
                        if 'community' in term:
                            expanded_terms.extend(['chapter', 'local', 'regional'])
                        if 'sponsor' in term:
                            expanded_terms.extend(['partnership', 'support', 'advertiser'])
                        if 'member' in term:
                            expanded_terms.extend(['user', 'participant', 'subscriber'])

                    logger.info(f"Searching {cls.__name__} with terms: {expanded_terms}")

                    search_conditions = []
                    # For each column and term, create a search condition
                    for column in searchable_columns:
                        for term in expanded_terms:
                            # Add wildcards between words for partial matches
                            term = term.replace(' ', '%')
                            search_conditions.append(getattr(cls, column).ilike(f'%{term}%'))

                    # Create the query with logging
                    query = cls.query.filter(or_(*search_conditions))
                    logger.info(f"Generated SQL for {cls.__name__}: {query}")

                    return query

                except Exception as e:
                    logger.error(f"Search error in {cls.__name__}: {str(e)}")
                    return cls.query.filter(False)  # Return empty result set on error


        class HelpArticle(db.Model, SearchableResource):
            __tablename__ = 'help_articles'
            __searchable__ = ['title', 'content', 'category', 'tags']

            id = db.Column(db.Integer, primary_key=True)
            title = db.Column(db.String(200), nullable=False)
            content = db.Column(db.Text, nullable=False)
            category = db.Column(db.String(100), nullable=False)
            tags = db.Column(db.String(500))  # Comma-separated tags
            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


        class Role(db.Model):
            __tablename__ = 'roles'
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(50), unique=True, nullable=False)
            description = db.Column(db.String(255))
            users = db.relationship('User', backref='role', lazy=True)


        class MembershipTier(db.Model):
            __tablename__ = 'membership_tiers'
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(50), unique=True, nullable=False)
            description = db.Column(db.Text)
            price = db.Column(db.Float, nullable=False)
            features = db.Column(db.JSON)
            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            users = db.relationship('User', backref='membership_tier', lazy=True)


        class Chapter(db.Model, SearchableResource):
            __tablename__ = 'chapters'
            __searchable__ = ['name', 'location', 'description', 'leader_name']
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(100), nullable=False)
            location = db.Column(db.String(100), nullable=False)
            description = db.Column(db.Text)
            leader_name = db.Column(db.String(100))
            leader_email = db.Column(db.String(120))
            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            users = db.relationship('User', backref='chapter', lazy=True)
            sponsors = db.relationship('Sponsor', backref='chapter', lazy=True)
            slug = db.Column(db.String(100), unique=True, nullable=False) # Add slug field

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if 'name' in kwargs:  # Ensure slug is generated only when name is provided
                    self.slug = slugify(self.name)

            def __repr__(self): #added for clarity
                return f'<Chapter {self.name}>'

        class Sponsor(db.Model, SearchableResource):
            __tablename__ = 'sponsors'
            __searchable__ = ['name', 'company', 'email', 'website', 'sponsorship_level']
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(100), nullable=False)
            company = db.Column(db.String(100), nullable=False)
            email = db.Column(db.String(120), nullable=False)
            website = db.Column(db.String(200))
            logo_url = db.Column(db.String(200))
            sponsorship_level = db.Column(db.String(50))
            chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


        class Contact(db.Model):
            __tablename__ = 'contacts'
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(100), nullable=False)
            email = db.Column(db.String(120), nullable=False)
            subject = db.Column(db.String(200), nullable=False)
            message = db.Column(db.Text, nullable=False)
            created_at = db.Column(db.DateTime, default=datetime.utcnow)


        class CharterMember(db.Model, SearchableResource):
            __tablename__ = 'charter_members'
            __searchable__ = ['business_name', 'description', 'member_name']

            id = db.Column(db.Integer, primary_key=True)
            business_name = db.Column(db.String(100), nullable=False)
            business_logo = db.Column(db.String(200))  # URL to logo image
            website_url = db.Column(db.String(200))
            description = db.Column(db.Text)
            member_name = db.Column(db.String(100), nullable=False)
            member_since = db.Column(db.DateTime, default=datetime.utcnow)
            chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
            chapter = db.relationship('Chapter', backref='charter_members')
            is_active = db.Column(db.Boolean, default=True)

            def __repr__(self):
                return f'<CharterMember {self.business_name}>'


        class User(db.Model, UserMixin, SearchableResource):
            __tablename__ = 'users'
            __searchable__ = ['name', 'email']
            id = db.Column(db.Integer, primary_key=True)
            email = db.Column(db.String(120), unique=True, nullable=False)
            password = db.Column(db.String(200), nullable=False)
            name = db.Column(db.String(100))
            created_at = db.Column(db.DateTime, default=datetime.utcnow)
            role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
            membership_tier_id = db.Column(db.Integer, db.ForeignKey('membership_tiers.id'))
            chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
            is_active = db.Column(db.Boolean, default=True)
            email_verified = db.Column(db.Boolean, default=False)
            is_chapter_leader = db.Column(db.Boolean, default=False)
            is_investor = db.Column(db.Boolean, default=False)
            sponsor = db.relationship('Sponsor', backref='user', uselist=False)
            # Add trial access fields
            trial_access_used = db.Column(db.Integer, default=0) # How many times have they had a free hour
            trial_access_start = db.Column(db.DateTime)
            trial_access_end = db.Column(db.DateTime)
            # User preferences
            audience_type = db.Column(db.String(255))  # Comma-separated values
            preferred_locations = db.Column(db.String(255))  # Comma-separated city names
            event_interests = db.Column(db.String(255))

            # Profile fields
            username = db.Column(db.String(50), unique=True)
            first_name = db.Column(db.String(50))
            last_name = db.Column(db.String(50))
            # is_admin is already defined above
            bio = db.Column(db.Text)
            location = db.Column(db.String(100))
            interests = db.Column(db.String(200))
            birth_date = db.Column(db.Date)
            profile_updated_at = db.Column(db.DateTime)

            # Organizer fields
            is_organizer = db.Column(db.Boolean, default=False)
            company_name = db.Column(db.String(100))
            organizer_description = db.Column(db.Text)
            organizer_website = db.Column(db.String(200))
            advertising_opportunities = db.Column(db.Text)
            sponsorship_opportunities = db.Column(db.Text)
            organizer_profile_updated_at = db.Column(db.DateTime)

            # Vendor fields
            is_vendor = db.Column(db.Boolean, default=False)
            vendor_type = db.Column(db.String(50))
            vendor_description = db.Column(db.Text)
            vendor_profile_updated_at = db.Column(db.DateTime)

            def update_organizer_profile(self, organizer_data):
                for key, value in organizer_data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                self.is_organizer = True
                self.organizer_profile_updated_at = datetime.utcnow()

            def update_vendor_profile(self, vendor_data):
                for key, value in vendor_data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                self.is_vendor = True
                self.vendor_profile_updated_at = datetime.utcnow()

            def set_password(self, password):
                self.password_hash = generate_password_hash(password)

            def check_password(self, password):
                if not self.password_hash:
                    return False
                if not password:
                    return False
                result = check_password_hash(self.password_hash, password)
                return result

            def get_id(self):
                return str(self.id)

            def is_active(self):
                return self.account_active

            def update_profile(self, profile_data):
                for key, value in profile_data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
                self.profile_updated_at = datetime.utcnow()

            def __repr__(self):
                return f'<User {self.email}>'

            # Password reset token methods
            def get_reset_token(self, expires_in=3600):
                # Generate a secure token with 32 bytes of randomness
                token = secrets.token_hex(32)
                # Set expiration timestamp (current time + expiration in seconds)
                expiry = int(time.time()) + expires_in

                # Try setting the fields and handle missing column exceptions gracefully
                try:
                    self.reset_token = token
                    self.reset_token_expiry = datetime.fromtimestamp(expiry)
                    db.session.commit()
                except Exception as e:
                    logger.error(f"Error setting reset token: {e}")
                    # If the columns don't exist, we just return the token anyway
                    db.session.rollback()

                return token

            @staticmethod
            def verify_reset_token(token):
                try:
                    user = User.query.filter_by(reset_token=token).first()
                    if not user:
                        return None

                    # Check if token is expired
                    if datetime.utcnow() > user.reset_token_expiry:
                        # Clear expired token
                        user.reset_token = None
                        user.reset_token_expiry = None
                        db.session.commit()
                        return None

                    return user
                except Exception as e:
                    logger.error(f"Error verifying reset token: {e}")
                    return None

            def clear_reset_token(self):
                try:
                    self.reset_token = None
                    self.reset_token_expiry = None
                    db.session.commit()
                except Exception as e:
                    logger.error(f"Error clearing reset token: {e}")
                    db.session.rollback()