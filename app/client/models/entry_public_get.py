from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="EntryPublicGet")


@_attrs_define
class EntryPublicGet:
    entry_name: str
    entry_data: str
    entry_id: UUID
    group_name: str
    group_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entry_name = self.entry_name

        entry_data = self.entry_data

        entry_id = str(self.entry_id)

        group_name = self.group_name

        group_id = str(self.group_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entry_name": entry_name,
                "entry_data": entry_data,
                "entry_id": entry_id,
                "group_name": group_name,
                "group_id": group_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        entry_name = d.pop("entry_name")

        entry_data = d.pop("entry_data")

        entry_id = UUID(d.pop("entry_id"))

        group_name = d.pop("group_name")

        group_id = UUID(d.pop("group_id"))

        entry_public_get = cls(
            entry_name=entry_name,
            entry_data=entry_data,
            entry_id=entry_id,
            group_name=group_name,
            group_id=group_id,
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
