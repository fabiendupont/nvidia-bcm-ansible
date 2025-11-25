#
# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
#

from __future__ import annotations

import logging

from lxml import etree

LOGGER = logging.getLogger(__name__)


class ValidateXML:
    """
    Validate an XML against an XSD schema.
    """

    @classmethod
    def check(cls, xml: str | bytes, xsd_path=None) -> bool:
        try:
            if isinstance(xml, str):
                xml = xml.encode("utf-8", errors="strict")
            xml_doc = etree.XML(xml)
            if xsd_path is not None:
                xmlschema_doc = etree.parse(xsd_path)
                xmlschema = etree.XMLSchema(xmlschema_doc)
                return xmlschema.validate(xml_doc)
            return True
        except Exception as e:
            LOGGER.error(f"XML validation failed:\n {xml}\n{e}")
            return False
