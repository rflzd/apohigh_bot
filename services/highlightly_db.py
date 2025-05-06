from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import DATABASE_URL  # Database URL .env-dən alınır
import sqlite3

# SQLAlchemy üçün Base təyin edilir
Base = declarative_base()

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

# Verilənlər bazası bağlantısı
def get_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()

# Verilənlər bazasında cədvəl yaratmaq
def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

# Verilənlər bazasına yeni admin əlavə etmək
def add_admin(user_id, db):
    db_admin = Admin(user_id=user_id)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

# Liqaların, komandaların və matçların verilənlər bazasına yazılması
def save_leagues_to_db(leagues):
    session = get_session()
    for league in leagues:
        existing_league = session.query(League).filter(League.name == league['name']).first()
        if not existing_league:
            new_league = League(name=league['name'], country=league['country'])
            session.add(new_league)
    session.commit()
    session.close()

def save_teams_to_db(teams):
    session = get_session()
    for team in teams:
        existing_team = session.query(Team).filter(Team.name == team['name']).first()
        if not existing_team:
            league = session.query(League).filter(League.name == team['league']).first()
            new_team = Team(name=team['name'], country=team['country'], league_id=league.id)
            session.add(new_team)
    session.commit()
    session.close()

def save_matches_to_db(matches):
    session = get_session()
    for match in matches:
        existing_match = session.query(Match).filter(Match.team1_id == match['team1_id'], Match.team2_id == match['team2_id'], Match.date == match['date']).first()
        if not existing_match:
            new_match = Match(team1_id=match['team1_id'], team2_id=match['team2_id'], score=match['score'], date=match['date'], league_id=match['league_id'])
            session.add(new_match)
    session.commit()
    session.close()

# İstifadəçi abunəliyini yoxlamaq
def get_subscription_status(user_id):
    """
    İstifadəçinin abunəlik statusunu gətirir.
    
    :param user_id: İstifadəçinin ID-si
    :return: True - abunəlik aktivdir, False - abunəlik aktiv deyil
    """
    session = get_session()
    user = session.query(User).filter(User.user_id == user_id).first()  # User cədvəlində istifadəçi yoxlanır
    session.close()
    
    if user:
        return user.is_subscribed
    return False

# İstifadəçinin abunəliyini aktivləşdirmək
def update_subscription_status(user_id, is_active, payment_receipt):
    """
    İstifadəçinin abunəlik statusunu yeniləyir.
    
    :param user_id: İstifadəçinin ID-si
    :param is_active: Abunəlik aktiv olduğu halda True, deaktiv olduqda False
    :param payment_receipt: Ödənişə dair təsdiq məlumatı
    """
    session = get_session()
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        user.is_subscribed = is_active
        user.payment_receipt = payment_receipt
        session.commit()
    session.close()

def activate_subscription(user_id):
    """
    İstifadəçinin abunəliyini aktivləşdirir.
    
    :param user_id: İstifadəçi ID-si
    :return: Heç bir şey qaytarmır
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE subscriptions SET is_active=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()