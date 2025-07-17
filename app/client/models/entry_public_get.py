from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from dateutil.parser import isoparse
from typing import cast
from uuid import UUID
import datetime


T = TypeVar("T", bound="EntryPublicGet")


@_attrs_define
class EntryPublicGet:
    title: str
    username: str
    password: str
    url: None | str
    notes: str
    entry_id: UUID
    group_id: UUID
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        username = self.username

        password = self.password

        url: None | str
        url = self.url

        notes = self.notes

        entry_id = str(self.entry_id)

        group_id = str(self.group_id)

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "username": username,
                "password": password,
                "url": url,
                "notes": notes,
                "entry_id": entry_id,
                "group_id": group_id,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        username = d.pop("username")

        password = d.pop("password")

        def _parse_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        url = _parse_url(d.pop("url"))

        notes = d.pop("notes")

        entry_id = UUID(d.pop("entry_id"))

        group_id = UUID(d.pop("group_id"))

        created_at = isoparse(d.pop("created_at"))

        entry_public_get = cls(
            title=title,
            username=username,
            password=password,
            url=url,
            notes=notes,
            entry_id=entry_id,
            group_id=group_id,
            created_at=created_at,
        )

        entry_public_get.additional_properties = d
        return entry_public_get

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
