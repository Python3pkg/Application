# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from application.controller.current_controller import CurrentController
from application.controller.banks_controller import BanksController
from application.controller.pedalboard_controller import PedalboardController, PedalboardError

from application.controller.notification_controller import NotificationController

from test.controller.controller_test import ControllerTest

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard
from pluginsmanager.model.update_type import UpdateType

import unittest
from unittest.mock import MagicMock


class PedalboardControllerTest(ControllerTest):

    def setUp(self):
        self.TOKEN = 'PATCH_TOKEN'

        controller = PedalboardControllerTest.application.controller

        self.controller = controller(PedalboardController)
        self.current = controller(CurrentController)
        self.banks = controller(BanksController)
        self.notifier = controller(NotificationController)

    def test_create_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_create_pedalboard - bank')
        pedalboard = Pedalboard('test_create_pedalboard')
        pedalboard2 = Pedalboard('test_create_pedalboard2')

        bank.append(pedalboard)
        self.banks.create(bank)

        self.controller.created(pedalboard)
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.CREATED, token=None, index=0, origin=bank)

        bank.append(pedalboard2)
        self.controller.created(pedalboard2, self.TOKEN)
        observer.on_pedalboard_updated.assert_called_with(pedalboard2, UpdateType.CREATED, token=self.TOKEN, index=1, origin=bank)

        self.controller.delete(pedalboard)
        self.controller.delete(pedalboard2)

        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_create_pedalboard_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_create_pedalboard_error - bank')
        pedalboard = Pedalboard('test_create_pedalboard')
        bank.append(pedalboard)

        with self.assertRaises(PedalboardError):
            self.controller.created(pedalboard)

        observer.on_pedalboard_updated.assert_not_called()

        self.notifier.unregister(observer)

    def test_update_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_update_pedalboard - bank')
        pedalboard = Pedalboard('test_update_pedalboard')

        self.banks.create(bank)

        bank.append(pedalboard)
        self.controller.created(pedalboard)

        pedalboard.name = 'test_update_pedalboard2'
        self.controller.update(pedalboard)

        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.UPDATED, token=None, index=0, origin=bank)

        pedalboard.name = 'test_update_pedalboard3'
        self.controller.update(pedalboard, self.TOKEN)
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.UPDATED, token=self.TOKEN, index=0, origin=bank)

        self.controller.delete(pedalboard)
        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_update_pedalboard_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_update_current_pedalboard - bank')
        pedalboard = Pedalboard('test_update_current_pedalboard')
        bank.append(pedalboard)

        with self.assertRaises(PedalboardError):
            self.controller.update(pedalboard)

        observer.on_pedalboard_updated.assert_not_called()

        self.notifier.unregister(observer)

    def test_update_current_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)
        original_pedalboard = self.current.current_pedalboard

        bank = Bank('test_update_current_pedalboard - bank')
        pedalboard = Pedalboard('test_update_current_pedalboard')

        self.banks.create(bank)

        bank.append(pedalboard)
        self.controller.created(pedalboard)

        self.current.set_pedalboard(pedalboard)

        pedalboard.name = 'test_update_current_pedalboard2'
        self.controller.update(pedalboard)

        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.UPDATED, token=None, index=0, origin=bank)

        self.assertEqual(self.current.current_pedalboard, pedalboard)
        self.assertEqual(self.current.current_bank, pedalboard.bank)

        self.assertEqual(self.current.pedalboard_number, pedalboard.index)
        self.assertEqual(self.current.bank_number, self.banks.banks.index(pedalboard.bank))

        pedalboard.name = 'test_update_current_pedalboard3'
        self.controller.update(pedalboard, self.TOKEN)
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.UPDATED, token=self.TOKEN, index=0, origin=bank)

        self.assertEqual(self.current.current_pedalboard, pedalboard)
        self.assertEqual(self.current.current_bank, pedalboard.bank)

        self.assertEqual(self.current.pedalboard_number, pedalboard.index)
        self.assertEqual(self.current.bank_number, self.banks.banks.index(pedalboard.bank))

        self.current.set_pedalboard(original_pedalboard)
        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_replace(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_replace - bank')
        pedalboard = Pedalboard('test_replace')
        pedalboard2 = Pedalboard('test_replace2')
        pedalboard3 = Pedalboard('test_replace3')

        bank.append(pedalboard)
        self.banks.create(bank)

        self.controller.replace(pedalboard, pedalboard2)
        observer.on_pedalboard_updated.assert_called_with(pedalboard2, UpdateType.UPDATED, token=None, index=0, origin=bank)

        self.controller.replace(pedalboard2, pedalboard3, self.TOKEN)
        observer.on_pedalboard_updated.assert_called_with(pedalboard3, UpdateType.UPDATED, token=self.TOKEN, index=0, origin=bank)

        self.controller.delete(pedalboard3)
        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_replace_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_replace - bank')
        pedalboard = Pedalboard('test_replace')
        pedalboard2 = Pedalboard('test_replace2')

        bank.append(pedalboard2)

        self.banks.create(bank)

        with self.assertRaises(PedalboardError):
            self.controller.replace(pedalboard, pedalboard2)

        observer.on_pedalboard_updated.assert_not_called()

        bank.append(pedalboard)

        with self.assertRaises(PedalboardError):
            self.controller.replace(pedalboard, pedalboard2)

        observer.on_pedalboard_updated.assert_not_called()

        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_delete_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_delete_pedalboard - bank')
        pedalboard = Pedalboard('test_delete_pedalboard')
        pedalboard2 = Pedalboard('test_delete_pedalboard2')

        self.banks.create(bank)

        bank.append(pedalboard)
        bank.append(pedalboard2)

        self.controller.created(pedalboard)
        self.controller.created(pedalboard2)

        self.controller.delete(pedalboard)
        observer.on_pedalboard_updated.assert_called_with(pedalboard, UpdateType.DELETED, token=None, index=0, origin=bank)
        self.controller.delete(pedalboard2, self.TOKEN)
        observer.on_pedalboard_updated.assert_called_with(pedalboard2, UpdateType.DELETED, token=self.TOKEN, index=0, origin=bank)

        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_delete_pedalboard_error(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_delete_pedalboard_error - bank')
        pedalboard = Pedalboard('test_delete_pedalboard')

        bank.append(pedalboard)
        with self.assertRaises(PedalboardError):
            self.controller.delete(pedalboard)

        observer.on_pedalboard_updated.assert_not_called()

        self.notifier.unregister(observer)

    def test_delete_current_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        original_pedalboard = self.current.current_pedalboard

        bank = Bank('test_delete_pedalboard - bank')
        pedalboard = Pedalboard('test_delete_pedalboard')
        pedalboard2 = Pedalboard('test_delete_pedalboard2')

        self.banks.create(bank)

        bank.append(pedalboard)
        bank.append(pedalboard2)

        self.controller.created(pedalboard)
        self.controller.created(pedalboard2)

        self.current.set_pedalboard(pedalboard)
        self.controller.delete(pedalboard)

        self.assertEqual(self.current.current_pedalboard, pedalboard2)
        self.assertEqual(self.current.current_bank, pedalboard2.bank)

        self.assertEqual(self.current.pedalboard_number, pedalboard2.index)
        self.assertEqual(self.current.bank_number, self.banks.banks.index(pedalboard2.bank))

        self.current.set_pedalboard(original_pedalboard)
        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_move(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_move - bank')
        self.banks.create(bank)

        bank.append(Pedalboard('Pedalboard 1'))
        bank.append(Pedalboard('Pedalboard 2'))
        bank.append(Pedalboard('Pedalboard 3'))
        bank.append(Pedalboard('Pedalboard 4'))

        pedalboard_moved = bank.pedalboards[-1]

        old_index = pedalboard_moved.index
        new_index = 1
        self.controller.move(pedalboard_moved, new_index)

        self.assertEqual(bank.pedalboards[new_index], pedalboard_moved)

        observer.on_pedalboard_updated.assert_any_call(
            pedalboard_moved,
            UpdateType.DELETED,
            index=old_index,
            origin=pedalboard_moved.bank,
            token=None
        )

        observer.on_pedalboard_updated.assert_any_call(
            pedalboard_moved,
            UpdateType.CREATED,
            index=new_index,
            origin=pedalboard_moved.bank,
            token=None
        )

        # Token test
        old_index = new_index
        new_index = 3
        self.controller.move(pedalboard_moved, new_index, token=self.TOKEN)

        self.assertEqual(bank.pedalboards[new_index], pedalboard_moved)

        observer.on_pedalboard_updated.assert_any_call(
            pedalboard_moved,
            UpdateType.DELETED,
            index=old_index,
            origin=pedalboard_moved.bank,
            token=self.TOKEN
        )

        observer.on_pedalboard_updated.assert_any_call(
            pedalboard_moved,
            UpdateType.CREATED,
            index=new_index,
            origin=pedalboard_moved.bank,
            token=self.TOKEN
        )

        self.banks.delete(bank)
        self.notifier.unregister(observer)

    def test_move_current_pedalboard(self):
        original_current_pedalboard = self.current.current_pedalboard

        observer = MagicMock()
        self.notifier.register(observer)

        bank = Bank('test_move - bank')
        self.banks.create(bank)

        bank.append(Pedalboard('Pedalboard 1'))
        bank.append(Pedalboard('Pedalboard 2'))
        bank.append(Pedalboard('Pedalboard 3'))
        bank.append(Pedalboard('Pedalboard 4'))

        pedalboard_moved = bank.pedalboards[-1]
        new_index = 1

        self.current.set_pedalboard(pedalboard_moved)

        self.assertEqual(self.current.bank_number, pedalboard_moved.bank.index)
        self.assertEqual(self.current.pedalboard_number, pedalboard_moved.index)

        self.controller.move(pedalboard_moved, new_index)

        self.assertEqual(self.current.bank_number, pedalboard_moved.bank.index)
        self.assertEqual(self.current.pedalboard_number, pedalboard_moved.index)

        self.current.set_pedalboard(original_current_pedalboard)
        self.banks.delete(bank)
        self.notifier.unregister(observer)
