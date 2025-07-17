from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="BodyTokenLoginApiAuthTokenPost")


@_attrs_define
class BodyTokenLoginApiAuthTokenPost:
    grant_type: str
    username: str
    password: str
    scope: Unset | str = ""
    client_id: None | Unset | str = UNSET
    client_secret: None | Unset | str = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        grant_type = self.grant_type

        username = self.username

        password = self.password

        scope = self.scope

        client_id: None | Unset | str
        if isinstance(self.client_id, Unset):
            client_id = UNSET
        else:
            client_id = self.client_id

        client_secret: None | Unset | str
        if isinstance(self.client_secret, Unset):
            client_secret = UNSET
        else:
            client_secret = self.client_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "grant_type": grant_type,
                "username": username,
                "password": password,
            }
        )
        if scope is not UNSET:
            field_dict["scope"] = scope
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        grant_type = d.pop("grant_type")

        username = d.pop("username")

        password = d.pop("password")

        scope = d.pop("scope", UNSET)

        def _parse_client_id(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        client_id = _parse_client_id(d.pop("client_id", UNSET))

        def _parse_client_secret(data: object) -> None | Unset | str:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | Unset | str, data)

        client_secret = _parse_client_secret(d.pop("client_secret", UNSET))

        body_token_login_api_auth_token_post = cls(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
        )

        body_token_login_api_auth_token_post.additional_properties = d
        return body_token_login_api_auth_token_post

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
