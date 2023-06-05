from api.api import TraderApi



if __name__ == '__main__':
    api = TraderApi()

    data = api.get_account_info()
    print(data)