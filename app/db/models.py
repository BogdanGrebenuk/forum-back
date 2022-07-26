import sqlalchemy as sa

metadata = sa.MetaData()


User = sa.Table(
    'user',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('username', sa.Text, nullable=False, unique=True),
    sa.Column('avatar', sa.Text, nullable=True),
    sa.Column('password', sa.Text, nullable=False),
    sa.Column('token', sa.Text, nullable=True),
)

Post = sa.Table(
    'post',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('title', sa.Text, nullable=False),
    sa.Column('content', sa.Text, nullable=False),
    sa.Column('image', sa.Text, nullable=True),
    sa.Column('author_id', sa.Text, sa.ForeignKey('user.id'), nullable=False),
)

Comment = sa.Table(
    'comment',
    metadata,
    sa.Column('id', sa.Text, primary_key=True),
    sa.Column('content', sa.Text, nullable=False),
    sa.Column('author_id', sa.Text, sa.ForeignKey('user.id'), nullable=False),
    sa.Column('post_id', sa.Text, sa.ForeignKey('post.id'), nullable=False),
)
