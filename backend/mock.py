from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
)


def create_mock_database():
    engine = create_engine("sqlite:///:memory:")
    metadata = MetaData()

    employees_table = Table(
        "employees",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(16), nullable=False),
        Column("department", String(16)),
        Column("salary", Integer),
    )
    metadata.create_all(engine)

    with engine.connect() as connection:
        connection.execute(
            employees_table.insert(),
            [
                {"name": "Alice", "department": "Engineering", "salary": 90000},
                {"name": "Bob", "department": "Engineering", "salary": 110000},
                {"name": "Charlie", "department": "Marketing", "salary": 70000},
                {"name": "Diana", "department": "Sales", "salary": 85000},
            ],
        )
        connection.commit()

    return engine