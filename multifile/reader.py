class MultiVCFReader:
    def __init__(self, input_paths):
        pass

    def __enter__(self):
        self._used_ctx_mgr = True
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __next__(self):
        if not getattr(self, '_used_ctx_mgr', False):
            raise BadUsageError


class BadUsageError(Exception):
    message = "Multi VCF reader should be used inside a context manager"
