"""Add patient intake, appointment messaging, and doctor suspension.

Revision ID: b7ccfe31a1ae
Revises: 3b4bf7b52342
Create Date: 2026-10-10
"""
from alembic import op
import sqlalchemy as sa


revision = "b7ccfe31a1ae"
down_revision = "3b4bf7b52342"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("doctors") as batch_op:
        batch_op.add_column(
            sa.Column(
                "is_suspended",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false()
            )
        )

    op.create_table(
        "intakes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.Column("symptoms", sa.Text(), nullable=False),
        sa.Column("symptom_duration", sa.String(length=500), nullable=False),
        sa.Column("previous_illness", sa.Text(), nullable=True),
        sa.Column("specialty_id", sa.Integer(), nullable=True),
        sa.Column("recommended_doctor_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.ForeignKeyConstraint(["specialty_id"], ["specialties.id"]),
        sa.ForeignKeyConstraint(["recommended_doctor_id"], ["doctors.id"]),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index("ix_intakes_patient_id", "intakes", ["patient_id"])

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("appointment_id", sa.Integer(), nullable=False),
        sa.Column("sender_id", sa.Integer(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("flagged_terms", sa.String(length=255), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("reviewed_by_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["appointment_id"], ["appointments.id"]),
        sa.ForeignKeyConstraint(["sender_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["reviewed_by_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(
        "ix_messages_appointment_id",
        "messages",
        ["appointment_id"]
    )
    op.create_index("ix_messages_sender_id", "messages", ["sender_id"])


def downgrade():
    op.drop_index("ix_messages_sender_id", table_name="messages")
    op.drop_index("ix_messages_appointment_id", table_name="messages")
    op.drop_table("messages")
    op.drop_index("ix_intakes_patient_id", table_name="intakes")
    op.drop_table("intakes")
    with op.batch_alter_table("doctors") as batch_op:
        batch_op.drop_column("is_suspended")
