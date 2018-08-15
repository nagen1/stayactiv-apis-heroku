"""empty message

Revision ID: b4825f844917
Revises: 1d5494403fad
Create Date: 2018-08-14 00:03:18.583668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4825f844917'
down_revision = '1d5494403fad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Exercises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('difficulty', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('muscle', sa.String(), nullable=False),
    sa.Column('routine', sa.String(), nullable=False),
    sa.Column('previewLink', sa.String(), nullable=False),
    sa.Column('createdDate', sa.DateTime(), nullable=True),
    sa.Column('updatedDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('daily_routines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Difficulty', sa.Integer(), nullable=False),
    sa.Column('Duration', sa.String(length=4), nullable=True),
    sa.Column('ExerciseId', sa.Integer(), nullable=False),
    sa.Column('ExerciseName', sa.String(), nullable=False),
    sa.Column('Muscle', sa.Integer(), nullable=False),
    sa.Column('PreviewLink', sa.Integer(), nullable=False),
    sa.Column('Reps', sa.Integer(), nullable=True),
    sa.Column('RestTime', sa.Integer(), nullable=True),
    sa.Column('Routine', sa.Integer(), nullable=False),
    sa.Column('Sequence', sa.Integer(), nullable=True),
    sa.Column('Sets', sa.Integer(), nullable=True),
    sa.Column('Type', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['Difficulty'], [u'Exercises.difficulty'], ),
    sa.ForeignKeyConstraint(['ExerciseId'], [u'Exercises.id'], ),
    sa.ForeignKeyConstraint(['ExerciseName'], [u'Exercises.name'], ),
    sa.ForeignKeyConstraint(['Muscle'], [u'Exercises.muscle'], ),
    sa.ForeignKeyConstraint(['PreviewLink'], [u'Exercises.previewLink'], ),
    sa.ForeignKeyConstraint(['Routine'], [u'Exercises.routine'], ),
    sa.ForeignKeyConstraint(['Type'], [u'Exercises.type'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('daily_routines')
    op.drop_table('Exercises')
    # ### end Alembic commands ###
