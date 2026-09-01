from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


# ---------------------------------------------------------
# 1. DATABASE CONNECTION
# ---------------------------------------------------------

DATABASE_URL = "mariadb+pymysql://root:lechu@localhost/school"

engine = create_engine(DATABASE_URL)


# ---------------------------------------------------------
# 2. BASE CLASS
# ---------------------------------------------------------

class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------
# 3. MODEL
# ---------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int]


# ---------------------------------------------------------
# 4. CREATE TABLES
# ---------------------------------------------------------

Base.metadata.create_all(engine)


# ---------------------------------------------------------
# 5. CREATE SESSION
# ---------------------------------------------------------

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------

user = User(
    name="Ananthu",
    age=20
)

session.add(user)
session.commit()

print("Created user:", user.id)


# ---------------------------------------------------------
# READ
# ---------------------------------------------------------

users = session.execute(
    select(User)
).scalars().all()

print("\nAll users:")

for user in users:
    print(user.id, user.name, user.age)


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

user = session.execute(
    select(User)
    .where(User.id == 1)
).scalar_one_or_none()

if user:
    user.age = 21
    session.commit()

    print("\nUser updated")


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------

user = session.execute(
    select(User)
    .where(User.id == 1)
).scalar_one_or_none()

if user:
    session.delete(user)
    session.commit()

    print("User deleted")


# ---------------------------------------------------------
# CLOSE SESSION
# ---------------------------------------------------------

session.close()

