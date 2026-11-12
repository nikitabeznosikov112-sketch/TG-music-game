
from database import User

def test_get_by_id(test_session, user_repo):
    user = User(tg_id=12345, name="Nikita")
    test_session.add(user)
    test_session.commit()
    repo = user_repo
    found = repo.get_by_id(12345)

    assert found is not None
    assert found.name == "Nikita"

def test_create_user(test_session, user_repo):
    repo = user_repo
    repo.create(12345, "Aleksei")
    found = test_session.query(User).filter_by(tg_id=12345).first()

    assert found is not None
    assert found.name == "Aleksei"

def test_add_points(test_session, user_repo):
    repo = user_repo
    user = User(tg_id=12345, name="Vladimir")
    test_session.add(user)
    test_session.commit()
    repo.add_points(12345, 145)
    assert user.score == 145
    repo.add_points(12345, 10)
    assert user.score == 155

def test_show_score(test_session, user_repo):
    repo = user_repo
    user = User(tg_id=12345, name="Matvei", score=456123)
    test_session.add(user)
    test_session.commit()
    score = repo.show_score(12345)
    assert score == 456123

def test_reset_user(test_session, admin_repo):
    repo = admin_repo
    user = User(tg_id=12345, name="Nikolay", score=999)
    test_session.add(user)
    test_session.commit()
    repo.reset_user(12345)
    assert user.score == 0

def test_delete_user(test_session, admin_repo):
    repo = admin_repo
    user = User(tg_id=12345, name="Nikolay", score=999)
    test_session.add(user)
    test_session.commit()
    repo.reset_user(12345)
    assert user.score == 0



    

