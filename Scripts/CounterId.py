class CounterId:
    def __init__(self):
        self.id_lst = list()

    @property
    def ids(self):
        return self.id_lst

    def __call__(self, msg_id, *args, **kwargs):
        self.id_lst.append(msg_id)