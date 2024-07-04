class ProviderNotConnected(Exception):
    def __init__(self, msg='Unable to connect RPC', *args: object, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = 400
        self.msg = msg
        self.errors = kwargs.get('errors', [])
        self.error_code = 'E_UNABLE_CONNECT_RPC'

    pass

