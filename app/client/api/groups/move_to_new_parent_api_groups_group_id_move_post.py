from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.group_move import GroupMove
from ...models.group_public_get import GroupPublicGet
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    group_id: UUID,
    *,
    body: GroupMove,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/groups/{group_id}/move",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[GroupPublicGet, HTTPValidationError] | None:
    if response.status_code == 200:
        response_200 = GroupPublicGet.from_dict(response.json())

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
) -> Response[Union[GroupPublicGet, HTTPValidationError]]:
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
    body: GroupMove,
) -> Response[Union[GroupPublicGet, HTTPValidationError]]:
    """Move To New Parent

     Moves the current group to a new parent.

    Args:
        group_id (UUID):
        body (GroupMove):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupPublicGet, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: UUID,
    *,
    client: AuthenticatedClient,
    body: GroupMove,
) -> Union[GroupPublicGet, HTTPValidationError] | None:
    """Move To New Parent

     Moves the current group to a new parent.

    Args:
        group_id (UUID):
        body (GroupMove):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupPublicGet, HTTPValidationError]
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    group_id: UUID,
    *,
    client: AuthenticatedClient,
    body: GroupMove,
) -> Response[Union[GroupPublicGet, HTTPValidationError]]:
    """Move To New Parent

     Moves the current group to a new parent.

    Args:
        group_id (UUID):
        body (GroupMove):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GroupPublicGet, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: UUID,
    *,
    client: AuthenticatedClient,
    body: GroupMove,
) -> Union[GroupPublicGet, HTTPValidationError] | None:
    """Move To New Parent

     Moves the current group to a new parent.

    Args:
        group_id (UUID):
        body (GroupMove):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GroupPublicGet, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            body=body,
        )
    ).parsed
