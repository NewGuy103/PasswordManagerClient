from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.generic_success import GenericSuccess
from ...models.http_validation_error import HTTPValidationError
from uuid import UUID


def _get_kwargs(
    group_id: UUID,
    entry_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/groups/{group_id}/entries/{entry_id}".format(
            group_id=group_id,
            entry_id=entry_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GenericSuccess, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GenericSuccess.from_dict(response.json())

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
) -> Response[Union[GenericSuccess, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: UUID,
    entry_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GenericSuccess, HTTPValidationError]]:
    """Delete Password Entry

    Args:
        group_id (UUID):
        entry_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GenericSuccess, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        entry_id=entry_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: UUID,
    entry_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GenericSuccess, HTTPValidationError]]:
    """Delete Password Entry

    Args:
        group_id (UUID):
        entry_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GenericSuccess, HTTPValidationError]
    """

    return sync_detailed(
        group_id=group_id,
        entry_id=entry_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    group_id: UUID,
    entry_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GenericSuccess, HTTPValidationError]]:
    """Delete Password Entry

    Args:
        group_id (UUID):
        entry_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GenericSuccess, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        entry_id=entry_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: UUID,
    entry_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GenericSuccess, HTTPValidationError]]:
    """Delete Password Entry

    Args:
        group_id (UUID):
        entry_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GenericSuccess, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            entry_id=entry_id,
            client=client,
        )
    ).parsed
