from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import DATABASE_URL  # Database URL .env-dən alınır

# SQLAlchemy üçün Base təyin edilir
Base = declarative_base()

# Verilənlər bazası bağlantısı
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Liqa cədvəli
class League(Base):
    __tablename__ = 'leagues'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    # Komandalarla əlaqə
    teams = relationship("Team", back_populates="league")

# Komanda cədvəli
class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    league_id = Column(Integer, ForeignKey('leagues.id'))
    country = Column(String(100), nullable=False)

    # Liqa ilə əlaqə
    league = relationship("League", back_populates="teams")

# Matç cədvəli
class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    team1_id = Column(Integer, ForeignKey('teams.id'))
    team2_id = Column(Integer, ForeignKey('teams.id'))
    score = Column(String(20))
    date = Column(DateTime)
    league_id = Column(Integer, ForeignKey('leagues.id'))

    # Komandalar ilə əlaqə
    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])
    league = relationship("League")

# Admin cədvəli
class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    admin_status = Column(Boolean, default=True)

# İstifadəçi cədvəli
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), unique=True, nullable=False)
    is_subscribed = Column(Boolean, default=False)
    payment_receipt = Column(String(255))  # Ödəniş təsdiqi (opsional)

# Verilənlər bazasında cədvəl yaratmaq
def init_db():
    Base.metadata.create_all(bind=engine)

# Sessiya əldə etmək üçün kontekst meneceri
def get_session():
    """
    Sessiya əldə etmək üçün kontekst meneceri.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Verilənlər bazasına yeni admin əlavə etmək
def add_admin(user_id):
    """
    Yeni admin əlavə edir.
    """
    with SessionLocal() as session:
        db_admin = Admin(user_id=user_id)
        session.add(db_admin)
        session.commit()
        session.refresh(db_admin)
        return db_admin

# Liqaların verilənlər bazasına yazılması
def save_leagues_to_db(leagues):
    """
    Liqaları verilənlər bazasına əlavə edir.
    """
    with SessionLocal() as session:
        for league in leagues:
            existing_league = session.query(League).filter(League.name == league['name']).first()
            if not existing_league:
                new_league = League(name=league['name'], country=league['country'])
                session.add(new_league)
        session.commit()

# Komandaların verilənlər bazasına yazılması
def save_teams_to_db(teams):
    """
    Komandaları verilənlər bazasına əlavə edir.
    """
    with SessionLocal() as session:
        for team in teams:
            existing_team = session.query(Team).filter(Team.name == team['name']).first()
            if not existing_team:
                league = session.query(League).filter(League.name == team['league']).first()
                new_team = Team(name=team['name'], country=team['country'], league_id=league.id)
                session.add(new_team)
        session.commit()

# Matçların verilənlər bazasına yazılması
def save_matches_to_db(matches):
    """
    Matçları verilənlər bazasına əlavə edir.
    """
    with SessionLocal() as session:
        for match in matches:
            existing_match = session.query(Match).filter(
                Match.team1_id == match['team1_id'],
                Match.team2_id == match['team2_id'],
                Match.date == match['date']
            ).first()
            if not existing_match:
                new_match = Match(
                    team1_id=match['team1_id'],
                    team2_id=match['team2_id'],
                    score=match['score'],
                    date=match['date'],
                    league_id=match['league_id']
                )
                session.add(new_match)
        session.commit()

# İstifadəçi abunəliyini yoxlamaq
def get_subscription_status(user_id):
    """
    İstifadəçinin abunəlik statusunu gətirir.
    """
    with SessionLocal() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            return user.is_subscribed
        return False

# İstifadəçinin abunəliyini yeniləmək
def update_subscription_status(user_id, is_active, payment_receipt):
    """
    İstifadəçinin abunəlik statusunu yeniləyir.
    """
    with SessionLocal() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            user.is_subscribed = is_active
            user.payment_receipt = payment_receipt
            session.commit()

# İstifadəçinin abunəliyini aktivləşdirmək
def activate_subscription(user_id):
    """
    İstifadəçinin abunəliyini aktivləşdirir.
    """
    with SessionLocal() as session:
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            user.is_subscribed = True
            session.commit()