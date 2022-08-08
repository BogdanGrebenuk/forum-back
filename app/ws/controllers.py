import jwt
from aiohttp.web import WebSocketResponse, WSMsgType


async def check_authentication(
        authentication_message,
        user_mapper,
        config,
        logger
        ):
    token = authentication_message.get('token')
    if token is None:
        message = '\'token\' field is missing in message.'
        logger.info(message)
        return False, message
    try:
        decoded = jwt.decode(
            token,
            config['secret'],
            algorithms=config['algorithm']
        )
    except Exception as e:
        message = str(e)
        logger.info(message)
        return False, message

    user_id = decoded.get('user_id')
    if user_id is None:
        message = '\'user_id\' field is missing in payload.'
        logger.info(message)
        return False, message

    user = await user_mapper.get_one_by(id=user_id)
    if user is None:
        message = 'User is not found.'
        logger.info(message)
        return False, message

    if user.token != token:
        message = 'Token is expired.'
        logger.info(message)
        return False, message

    return True, ''


async def index(
        request,
        ws_pool,
        user_mapper,
        token_config,
        logger
        ):
    ws = WebSocketResponse()
    await ws.prepare(request)

    authentication_message = await ws.receive_json(timeout=3)
    authenticated, reason = await check_authentication(authentication_message, user_mapper, token_config, logger)
    logger.info(f'Authentication status: {authenticated}. Additional info: {reason}')
    if not authenticated:
        await ws.send_json({
            'status': False,
            'description': reason
        })
        await ws.close(message=reason.encode())
        return ws
    await ws.send_json({
        'status': True,
        'description': 'Successfully authenticated'
    })
    ws_pool.add(ws)

    try:
        async for message in ws:
            continue
    finally:
        if not ws.closed:
            await ws.close()
        ws_pool.remove(ws)

    return ws
