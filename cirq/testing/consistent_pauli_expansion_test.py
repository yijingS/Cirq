# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict

import numpy as np
import pytest

import cirq

X = np.array([[0, 1], [1, 0]])
Y = np.array([[0, -1j], [1j, 0]])
Z = np.diag([1, -1])


class GoodGateExplicitPauliExpansion(cirq.SingleQubitGate):
    def _unitary_(self) -> np.ndarray:
        return np.sqrt(1/2) * X + np.sqrt(1/3) * Y + np.sqrt(1/6) * Z

    def _pauli_expansion_(self) -> cirq.LinearDict[str]:
        return cirq.LinearDict({'X': np.sqrt(1/2),
                                'Y': np.sqrt(1/3),
                                'Z': np.sqrt(1/6)})


class GoodGateImplicitPauliExpansion(cirq.SingleQubitGate):
    def _unitary_(self) -> np.ndarray:
        return np.eye(2)


class GoodGateNoPauliExpansion(cirq.MultiQubitGate):
    def __init__(self) -> None:
        super().__init__(num_qubits=4)

    def _unitary_(self) -> np.ndarray:
        return np.eye(16)


class GoodGateNoUnitary(cirq.SingleQubitGate):
    def _pauli_expansion_(self) -> cirq.LinearDict[str]:
        return cirq.LinearDict({'X': np.sqrt(1/2), 'Y': np.sqrt(1/2)})


class GoodGateNoPauliExpansionNoUnitary(cirq.SingleQubitGate):
    pass


class BadGateInconsistentPauliExpansion(cirq.SingleQubitGate):
    def _unitary_(self) -> np.ndarray:
        return np.sqrt(1/2) * X + np.sqrt(1/3) * Y + np.sqrt(1/6) * Z

    def _pauli_expansion_(self) -> cirq.LinearDict[str]:
        return cirq.LinearDict({'X': np.sqrt(1/6),
                                'Y': np.sqrt(1/3),
                                'Z': np.sqrt(1/2)})


def test_assert_pauli_expansion_is_consistent_with_unitary():
    cirq.testing.assert_pauli_expansion_is_consistent_with_unitary(
            GoodGateExplicitPauliExpansion())
    cirq.testing.assert_pauli_expansion_is_consistent_with_unitary(
            GoodGateImplicitPauliExpansion())
    cirq.testing.assert_pauli_expansion_is_consistent_with_unitary(
            GoodGateNoPauliExpansion())
    cirq.testing.assert_pauli_expansion_is_consistent_with_unitary(
            GoodGateNoUnitary())
    cirq.testing.assert_pauli_expansion_is_consistent_with_unitary(
            GoodGateNoPauliExpansionNoUnitary())

    with pytest.raises(AssertionError):
        cirq.testing.assert_pauli_expansion_is_consistent_with_unitary(
                BadGateInconsistentPauliExpansion())
