# services/admin_checker.py
from services.highlightly_db import Admin, session

def is_user_admin(user_id):
    """
    İstifadəçinin admin olub-olmamasını yoxlayır.
    
    :param user_id: İstifadəçi ID-si
    :return: True (admin) və ya False (admin deyil)
    """
    admin = session.query(Admin).filter_by(user_id=user_id).first()
    return admin is not None and admin.admin_status
