# coding: utf-8
#
# Copyright 2024 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for EntityVoiceoversModel models."""

from __future__ import annotations

from core import feconf
from core.platform import models
from core.tests import test_utils

MYPY = False
if MYPY: # pragma: no cover
    from mypy_imports import base_models
    from mypy_imports import voiceover_models

(base_models, voiceover_models) = models.Registry.import_models([
    models.Names.BASE_MODEL, models.Names.VOICEOVER
])


class EntityVoiceoversModelTest(test_utils.GenericEmailTestBase):
    """Unit tests for EntityVoiceoversModel class."""

    def test_create_new_model(self) -> None:
        dummy_manual_voiceover_dict: voiceover_models.VoiceoverDict = {
            'filename': 'filename1.mp3',
            'file_size_bytes': 3000,
            'needs_update': False,
            'duration_secs': 6.1
        }
        dummy_autogenerated_voiceover_dict: voiceover_models.VoiceoverDict = {
            'filename': 'filename2.mp3',
            'file_size_bytes': 3500,
            'needs_update': False,
            'duration_secs': 5.9
        }
        entity_voiceovers_model = (
            voiceover_models.EntityVoiceoversModel.create_new(
                feconf.ENTITY_TYPE_EXPLORATION, 'exp_id', 1, 'en-US', {
                    'content_0': {
                        'manual': dummy_manual_voiceover_dict,
                        'auto': dummy_autogenerated_voiceover_dict
                        }
                    }))

        self.assertEqual(entity_voiceovers_model.entity_type, 'exploration')
        self.assertEqual(entity_voiceovers_model.entity_id, 'exp_id')
        self.assertEqual(entity_voiceovers_model.entity_version, 1)
        self.assertEqual(entity_voiceovers_model.language_accent_code, 'en-US')
        voiceovers = entity_voiceovers_model.voiceovers
        self.assertEqual(
            voiceovers['content_0']['manual'], dummy_manual_voiceover_dict)
        self.assertEqual(
            voiceovers['content_0']['auto'], dummy_autogenerated_voiceover_dict)

    def test_get_voiceover_model_returns_correctly(self) -> None:
        dummy_manual_voiceover_dict: voiceover_models.VoiceoverDict = {
            'filename': 'filename1.mp3',
            'file_size_bytes': 3000,
            'needs_update': False,
            'duration_secs': 6.1
        }
        dummy_autogenerated_voiceover_dict: voiceover_models.VoiceoverDict = {
            'filename': 'filename2.mp3',
            'file_size_bytes': 3500,
            'needs_update': False,
            'duration_secs': 5.9
        }
        voiceover_models.EntityVoiceoversModel.create_new(
            feconf.ENTITY_TYPE_EXPLORATION, 'exp_id', 1, 'en-US', {
                'content_0': {
                    'manual': dummy_manual_voiceover_dict,
                    'auto': dummy_autogenerated_voiceover_dict
                    }
                }
        ).put()

        entity_voiceovers_model = (
            voiceover_models.EntityVoiceoversModel.get_model(
                entity_type=feconf.ENTITY_TYPE_EXPLORATION,
                entity_id='exp_id',
                entity_version=1,
                language_accent_code='en-US'))

        self.assertEqual(entity_voiceovers_model.entity_type, 'exploration')
        self.assertEqual(entity_voiceovers_model.entity_id, 'exp_id')
        self.assertEqual(entity_voiceovers_model.entity_version, 1)
        self.assertEqual(entity_voiceovers_model.language_accent_code, 'en-US')
        voiceovers = entity_voiceovers_model.voiceovers
        self.assertEqual(
            voiceovers['content_0']['manual'], dummy_manual_voiceover_dict)
        self.assertEqual(
            voiceovers['content_0']['auto'], dummy_autogenerated_voiceover_dict)

    def test_get_export_policy_not_applicable(self) -> None:
        self.assertEqual(
            voiceover_models.EntityVoiceoversModel.get_export_policy(),
            {
                'created_on': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'deleted': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'last_updated': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'entity_id': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'entity_type': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'entity_version': base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'language_accent_code':
                    base_models.EXPORT_POLICY.NOT_APPLICABLE,
                'voiceovers': base_models.EXPORT_POLICY.NOT_APPLICABLE
            }
        )

    def test_get_deletion_policy_not_applicable(self) -> None:
        self.assertEqual(
            voiceover_models.EntityVoiceoversModel.get_deletion_policy(),
            base_models.DELETION_POLICY.NOT_APPLICABLE)

    def test_get_model_association_to_user_not_corresponding_to_user(
        self
    ) -> None:
        model_cls = voiceover_models.EntityVoiceoversModel
        self.assertEqual(
            model_cls.get_model_association_to_user(),
            base_models.MODEL_ASSOCIATION_TO_USER.NOT_CORRESPONDING_TO_USER)