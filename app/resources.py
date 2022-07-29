def setup_routes(app):
    container = app.container

    app.router.add_route(
        'POST', '/register', container.auth.register_user.as_view()
    )
    app.router.add_route(
        'POST', '/login', container.auth.authenticate_user.as_view()
    )
    app.router.add_route(
        'POST', '/logout', container.auth.logout_user.as_view()
    )
    app.router.add_route(
        'PUT', '/api/users/me', container.user.update_me.as_view()
    )
    app.router.add_route(
        'GET',  '/api/users/me', container.user.get_user_me.as_view()
    )
    app.router.add_route(
        'POST', '/api/posts', container.post.create_post.as_view()
    )
    app.router.add_route(
        'GET', '/api/posts', container.post.get_all_posts.as_view()
    )
    app.router.add_route(
        'POST', '/api/posts/{post_id}/comments', container.post.create_comment.as_view()
    )
