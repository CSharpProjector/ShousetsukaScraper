from request_parameter import RequestParameter


def create_request(base_url: str, *parameters: RequestParameter) -> str:
    url = base_url

    for i, parameter in enumerate(parameters):
        url += f"{parameter.name}={parameter.value}"
        if i + 1 != len(parameters):
            url += "&"

    return url
