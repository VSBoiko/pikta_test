import requests


class PiktaNalog:
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    api = "https://service.nalog.ru/addrno-proc.json"

    def __init__(self):
        pass

    def get_info(self, ifns: str, oktmmf: str) -> dict:
        """
        Получить реквизиты на сайте налоговой службы

        :param ifns: код ИФНС
        :param oktmmf: код муниципального образование

        :return: словарь с результатами запроса
        """
        params = {
            "c": "next",
            "step": "1",
            "npKind": "fl",
            "objectAddr": "",
            "objectAddr_zip": "",
            "objectAddr_ifns": "",
            "objectAddr_okatom": "",
            "ifns": ifns,               # "7840"
            "oktmmf": oktmmf,           # "40913000"
            "PreventChromeAutocomplete": ""
        }

        return self._send_request(
            method="post",
            url=self.api,
            headers=self.headers,
            params=params,
            data={}
        )

    def _send_request(self, method: str, url: str, headers: dict, params: dict,
                      data: dict) -> dict:
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data
            )
            return self.__validate(response=response)
        except Exception as e:
            print(e)
            raise

    def __validate(self, response) -> dict:
        data = response.json()
        if not response.status_code == 200:
            data = {
                "error": data["ERROR"],
                "status_code": response.status_code,
            }

        return data
