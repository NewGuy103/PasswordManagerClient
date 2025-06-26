from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.entry_public_get import EntryPublicGet
from ...models.http_validation_error import HTTPValidationError
from ...types import Unset
from uuid import UUID


def _get_kwargs(
    group_id: UUID,
    *,
    amount: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["amount"] = amount

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/groups/{group_id}/entries/".format(
            group_id=group_id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["EntryPublicGet"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = EntryPublicGet.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, list["EntryPublicGet"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: UUID,
    *,
    client: AuthenticatedClient,
    amount: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[HTTPValidationError, list["EntryPublicGet"]]]:
    """Get Group Entries

    Args:
        group_id (UUID):
        amount (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['EntryPublicGet']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        amount=amount,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: UUID,
    *,
    client: AuthenticatedClient,
    amount: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[HTTPValidationError, list["EntryPublicGet"]]]:
    """Get Group Entries

    Args:
        group_id (UUID):
        amount (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['EntryPublicGet']]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        amount=amount,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    group_id: UUID,
    *,
    client: AuthenticatedClient,
    amount: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Response[Union[HTTPValidationError, list["EntryPublicGet"]]]:
    """Get Group Entries

    Args:
        group_id (UUID):
        amount (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['EntryPublicGet']]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        amount=amount,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: UUID,
    *,
    client: AuthenticatedClient,
    amount: Union[Unset, int] = 100,
    offset: Union[Unset, int] = 0,
) -> Optional[Union[HTTPValidationError, list["EntryPublicGet"]]]:
    """Get Group Entries

    Args:
        group_id (UUID):
        amount (Union[Unset, int]):  Default: 100.
        offset (Union[Unset, int]):  Default: 0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['EntryPublicGet']]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            amount=amount,
            offset=offset,
        )
    ).parsed
