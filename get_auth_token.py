import requests
from pprint import pprint


class Require2FA(Exception):
    pass


class AuthError(Exception):
    pass


class Error2FA(Exception):
    pass


class TradingViewAPI:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.username = None
        self.password = None
        self.headers = {'Referer': 'https://www.tradingview.com'}

    def login(self, username: str, password: str):
        sign_in_url = 'https://www.tradingview.com/accounts/signin/'
        data = {"username": username, "password": password, "remember": "on"}

        response = self.session.post(url=sign_in_url, data=data, headers=self.headers)
        answer = response.json()
        if 'code' in answer and answer['code'] == '2FA_required':
            raise Require2FA
        elif 'user' in answer:
            return answer['user']['auth_token']
        else:
            raise AuthError("Ошибка аутентификации")

    def enter_2fa(self, code: str):
        two_factor_url = 'https://www.tradingview.com/accounts/two-factor/signin/totp/'
        data = {'code': code}
        response = self.session.post(url=two_factor_url, data=data, headers=self.headers).json()
        if 'user' in response:
            return response['user']['auth_token']
        else:
            raise Error2FA("Неправильный 2fa-код")


def main():
    api = TradingViewAPI()
    try:
        token = api.login(username='imExpelliarmus@yandex.ru', password='MyPass1821')
    except Require2FA:
        code = input('Введите код 2fa: ')
        token = api.enter_2fa(code)
    print(token)


if __name__ == '__main__':
    main()
