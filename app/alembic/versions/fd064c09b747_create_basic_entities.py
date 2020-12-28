"""create basic entities

Revision ID: fd064c09b747
Revises: 45157ab8d36e
Create Date: 2020-12-28 13:48:12.799357

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'fd064c09b747'
down_revision = '45157ab8d36e'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "INSERT INTO permissions VALUES (1, 'admin', 'You have privileges as a god')"
    )
    op.execute(
        "INSERT INTO permissions VALUES (2, 'user', 'You have the standar privileges')"
    )
    op.execute("INSERT INTO groups VALUES (1, 'admin')")
    op.execute("INSERT INTO groups VALUES (2, 'user')")
    op.execute("INSERT INTO group_permissions VALUES (1, 1)")
    op.execute("INSERT INTO group_permissions VALUES (2, 2)")


def downgrade():
    op.execute("DELETE FROM user_groups WHERE 1=1")
    op.execute("DELETE FROM group_permissions WHERE 1=1")
    op.execute("DELETE FROM groups WHERE 1=1")
    op.execute("DELETE FROM permissions WHERE 1=1")
