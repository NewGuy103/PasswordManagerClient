from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast, Union
from uuid import UUID


T = TypeVar("T", bound="GroupPublicModify")


@_attrs_define
class GroupPublicModify:
    """Leave out `child_groups` list for operations like create and rename."""

    group_name: str
    parent_id: Union[None, UUID]
    group_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        group_name = self.group_name

        parent_id: Union[None, str]
        if isinstance(self.parent_id, UUID):
            parent_id = str(self.parent_id)
        else:
            parent_id = self.parent_id

        group_id = str(self.group_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "group_name": group_name,
                "parent_id": parent_id,
                "group_id": group_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        group_name = d.pop("group_name")

        def _parse_parent_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                parent_id_type_0 = UUID(data)

                return parent_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        group_id = UUID(d.pop("group_id"))

        group_public_modify = cls(
            group_name=group_name,
            parent_id=parent_id,
            group_id=group_id,
        )

        group_public_modify.additional_properties = d
        return group_public_modify

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
