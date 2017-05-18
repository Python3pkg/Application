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
from application.controller.notification_controller import NotificationController

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard

from test.controller.controller_test import ControllerTest

from unittest.mock import MagicMock


class CurrentControllerTest(ControllerTest):
    def setUp(self):
        self.TOKEN = 'CURRENT_TOKEN'

        controller = CurrentControllerTest.application.controller
        self.controller = controller(CurrentController)
        self.banks_controller = controller(BanksController)
        self.notifier = controller(NotificationController)

        self.controller.set_pedalboard(self.banks_controller.banks[0].pedalboards[0])

    @property
    def bank_with_pedalboard(self):
        bank = Bank('A bank')
        pedalboard = Pedalboard('A pedalboard')
        bank.append(pedalboard)

        return bank

    def test_current_pedalboard(self):
        current_bank = self.controller.current_bank
        current_pedalboard = self.controller.current_pedalboard

        self.assertIsNotNone(current_pedalboard)
        self.assertEqual(
            current_bank.pedalboards[0],
            current_pedalboard
        )

    def test_current_bank(self):
        current_bank = self.controller.current_bank

        self.assertIsNotNone(self.controller.current_bank)
        self.assertEqual(
            self.banks_controller.banks[0],
            current_bank
        )

    def test_is_current_bank(self):
        bank = self.bank_with_pedalboard
        self.banks_controller.create(bank)

        current_bank = self.controller.current_bank
        another_bank = self.banks_controller.banks[-1]

        self.assertTrue(self.controller.is_current_bank(current_bank))
        self.assertFalse(self.controller.is_current_bank(another_bank))

        self.banks_controller.delete(bank)

    def test_is_current_pedalboard(self):
        bank = self.bank_with_pedalboard
        self.banks_controller.create(bank)

        current_pedalboard = self.controller.current_pedalboard

        another_bank = self.banks_controller.banks[-1]
        another_pedalboard = another_bank.pedalboards[0]

        self.assertTrue(self.controller.is_current_pedalboard(current_pedalboard))
        self.assertFalse(self.controller.is_current_pedalboard(another_pedalboard))

        self.banks_controller.delete(bank)

    def test_to_before_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        pedalboard = Pedalboard('Other pedalboard')
        self.controller.current_bank.append(pedalboard)

        total_pedalboards = len(self.controller.current_bank.pedalboards)
        for id_pedalboard in reversed(range(total_pedalboards)):
            self.controller.to_before_pedalboard()
            self.assertEqual(id_pedalboard, self.controller.pedalboard_number)
            observer.on_current_pedalboard_changed.assert_called_with(self.controller.current_pedalboard, None)

        for id_pedalboard in reversed(range(total_pedalboards)):
            self.controller.to_before_pedalboard(self.TOKEN)
            self.assertEqual(id_pedalboard, self.controller.pedalboard_number)
            observer.on_current_pedalboard_changed.assert_called_with(self.controller.current_pedalboard, self.TOKEN)

        self.assertEqual(0, self.controller.pedalboard_number)

        self.controller.current_bank.pedalboards.remove(pedalboard)

        self.notifier.unregister(observer)

    def test_to_next_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        pedalboard = Pedalboard('Other pedalboard')
        self.controller.current_bank.append(pedalboard)

        total_pedalboards = len(self.controller.current_bank.pedalboards)
        pedalboard_initial_index = self.controller.pedalboard_number
        for id_pedalboard in range(total_pedalboards):
            self.assertEqual(id_pedalboard + pedalboard_initial_index, self.controller.pedalboard_number)
            self.controller.to_next_pedalboard()
            observer.on_current_pedalboard_changed.assert_called_with(self.controller.current_pedalboard, None)

        for id_pedalboard in range(total_pedalboards):
            self.assertEqual(id_pedalboard, self.controller.pedalboard_number)
            self.controller.to_next_pedalboard(self.TOKEN)
            observer.on_current_pedalboard_changed.assert_called_with(self.controller.current_pedalboard, self.TOKEN)

        self.assertEqual(0, self.controller.pedalboard_number)

        self.controller.current_bank.pedalboards.remove(pedalboard)

        self.notifier.unregister(observer)

    def test_set_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        pedalboard = Pedalboard('Other pedalboard')
        self.controller.current_bank.append(pedalboard)

        original_pedalboard = self.controller.current_pedalboard

        self.controller.set_pedalboard(pedalboard)
        self.assertEqual(pedalboard.index, self.controller.pedalboard_number)
        observer.on_current_pedalboard_changed.assert_called_with(pedalboard, None)

        self.assertNotEqual(original_pedalboard, self.controller.current_pedalboard)
        self.assertEqual(pedalboard, self.controller.current_pedalboard)

        self.controller.set_pedalboard(original_pedalboard, self.TOKEN)
        self.assertEqual(0, self.controller.pedalboard_number)
        observer.on_current_pedalboard_changed.assert_called_with(original_pedalboard, self.TOKEN)

        self.controller.current_bank.pedalboards.remove(pedalboard)

        self.notifier.unregister(observer)

    def test_set_pedalboard_other_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = self.bank_with_pedalboard
        self.banks_controller.create(bank)

        original_pedalboard = self.controller.current_pedalboard
        original_bank_number = self.controller.bank_number

        self.controller.set_pedalboard(bank.pedalboards[0])
        self.assertEqual(0, self.controller.pedalboard_number)
        self.assertEqual(self.banks_controller.banks.index(bank), self.controller.bank_number)
        observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], None)

        self.assertNotEqual(original_pedalboard, self.controller.current_pedalboard)
        self.assertEqual(bank.pedalboards[0], self.controller.current_pedalboard)
        self.assertEqual(len(self.banks_controller.banks) - 1, self.controller.bank_number)

        self.controller.set_pedalboard(original_pedalboard, self.TOKEN)
        self.assertEqual(0, self.controller.pedalboard_number)
        self.assertEqual(original_bank_number, self.controller.bank_number)
        observer.on_current_pedalboard_changed.assert_called_with(original_pedalboard, self.TOKEN)

        self.banks_controller.delete(bank)
        self.notifier.unregister(observer)

    def test_set_pedalboard_current_pedalboard(self):
        observer = MagicMock()
        self.notifier.register(observer)

        self.controller.set_pedalboard(self.controller.current_pedalboard)
        observer.on_current_pedalboard_changed.assert_not_called()

        self.notifier.unregister(observer)

    def test_set_pedalboard_not_added(self):
        bank = self.bank_with_pedalboard
        with self.assertRaises(ValueError):
            self.controller.set_pedalboard(bank.pedalboards[0])

    def test_before_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = self.bank_with_pedalboard
        self.banks_controller.create(bank)

        for b in reversed(self.banks_controller.banks):
            self.controller.to_before_bank()
            self.assertEqual(b, self.controller.current_bank)
            observer.on_current_pedalboard_changed.assert_called_with(b.pedalboards[0], None)

        for b in reversed(self.banks_controller.banks):
            self.controller.to_before_bank(self.TOKEN)
            self.assertEqual(b, self.controller.current_bank)
            observer.on_current_pedalboard_changed.assert_called_with(b.pedalboards[0], self.TOKEN)

        self.banks_controller.delete(bank)
        self.notifier.unregister(observer)

    def test_next_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = self.bank_with_pedalboard
        self.banks_controller.create(bank)

        self.controller.to_before_bank()
        for b in self.banks_controller.banks:
            self.controller.to_next_bank()
            self.assertEqual(b, self.controller.current_bank)
            observer.on_current_pedalboard_changed.assert_called_with(b.pedalboards[0], None)

        for b in self.banks_controller.banks:
            self.controller.to_next_bank(self.TOKEN)
            self.assertEqual(b, self.controller.current_bank)
            observer.on_current_pedalboard_changed.assert_called_with(b.pedalboards[0], self.TOKEN)

        self.controller.to_next_bank()

        self.banks_controller.delete(bank)
        self.notifier.unregister(observer)

    def test_set_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        bank = self.bank_with_pedalboard
        index = self.banks_controller.create(bank)

        first_bank = self.controller.current_bank

        self.controller.set_bank(bank)
        self.assertEqual(index, self.controller.bank_number)
        self.assertNotEqual(first_bank, self.controller.current_bank)
        observer.on_current_pedalboard_changed.assert_called_with(bank.pedalboards[0], None)

        # Pedalboard will be the first
        self.assertEqual(index, self.controller.bank_number)
        self.assertEqual(0, self.controller.pedalboard_number)

        self.controller.set_bank(first_bank, self.TOKEN)
        observer.on_current_pedalboard_changed.assert_called_with(first_bank.pedalboards[0], self.TOKEN)

        self.banks_controller.delete(bank)
        self.notifier.unregister(observer)

    def test_set_bank_not_added(self):
        bank = self.bank_with_pedalboard
        with self.assertRaises(ValueError):
            self.controller.set_bank(bank)

    def test_set_bank_current_bank(self):
        observer = MagicMock()
        self.notifier.register(observer)

        self.controller.set_bank(self.controller.current_bank)
        observer.on_current_pedalboard_changed.assert_not_called()

        self.notifier.unregister(observer)
