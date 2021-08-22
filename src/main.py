import router


def lambda_handler(event, context):
    return router.route(event, context)
