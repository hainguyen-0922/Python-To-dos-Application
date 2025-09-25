"""generate company table

Revision ID: 9829ea719e70
Revises: 
Create Date: 2025-09-23 15:57:11.764506

"""
from datetime import datetime
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9829ea719e70'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users = op.create_table(
        "users",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("hashed_password", sa.String),
        sa.Column("is_active", sa.Boolean, nullable=True),
        sa.Column("is_admin", sa.Boolean, nullable=False),
        sa.Column("company_id", sa.UUID, nullable=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )
    companies = op.create_table(
        "companies",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("name", sa.String, nullable=True),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("mode", sa.String, nullable=False),
        sa.Column("rating", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )    
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID, nullable=False, primary_key=True),
        sa.Column("summary", sa.String, nullable=True),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("status", sa.String, nullable=False),
        sa.Column("priority", sa.String, nullable=False),
        sa.Column("user_id", sa.UUID, nullable=False),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )

    op.create_foreign_key("fk_employee", "users", "companies", ["company_id"], ["id"])
    op.create_foreign_key("fk_employee_task", "tasks", "users", ["user_id"], ["id"])

    op.bulk_insert(companies, [
        {
            "id": uuid4(),
            "name": "company_A",
            "description": "company_A",
            "mode":"Work",
            "rating": 1,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": uuid4(),
            "name": "company_B",
            "description": "company_B",
            "mode":"Work",
            "rating": 2,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "id": uuid4(),
            "name": "company_C",
            "description": "company_C",
            "mode":"Work",
            "rating": 3,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
    ])


def downgrade() -> None:    
    op.drop_constraint("fk_employee_task", "tasks", type_="foreignkey")
    op.drop_constraint("fk_employee", "users", type_="foreignkey")
    
    op.drop_table("tasks")
    op.drop_table("users")
    op.drop_table("companies")

