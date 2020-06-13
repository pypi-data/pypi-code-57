#  MIT License
#
#  Copyright (c) 2020 Parakoopa
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
from typing import Optional

from explorerscript.error import SsbCompilerError
from explorerscript.ssb_converting.compiler.compile_handlers.abstract import AbstractCompileHandler
from explorerscript.ssb_converting.compiler.compile_handlers.atoms.conditional_operator import \
    ConditionalOperatorCompileHandler
from explorerscript.ssb_converting.compiler.compile_handlers.atoms.integer_like import IntegerLikeCompileHandler
from explorerscript.ssb_converting.compiler.compile_handlers.atoms.value_of import ValueOfCompileHandler
from explorerscript.ssb_converting.compiler.utils import CompilerCtx, SsbLabelJumpBlueprint
from explorerscript.ssb_converting.ssb_data_types import SsbOperator, SsbOpParam
from explorerscript.ssb_converting.ssb_special_ops import OP_CASE_VARIABLE, OP_CASE, OP_CASE_VALUE


class CaseHeaderOpCompileHandler(AbstractCompileHandler):
    def __init__(self, ctx, compiler_ctx: CompilerCtx):
        super().__init__(ctx, compiler_ctx)
        self.operator: Optional[SsbOperator] = None
        self.value: Optional[SsbOpParam] = None
        self.value_is_a_variable = False

    def collect(self) -> SsbLabelJumpBlueprint:
        if self.operator is None:
            raise SsbCompilerError("No operator set for if condition.")
        if self.value is None:
            raise SsbCompilerError("No value set for if condition.")

        if self.value_is_a_variable:
            # CaseVariable
            return SsbLabelJumpBlueprint(
                self.compiler_ctx, self.ctx,
                OP_CASE_VARIABLE, [self.operator.value, self.value]
            )

        #if self.operator == SsbOperator.EQ:
        #    # Case
        #    return SsbLabelJumpBlueprint(
        #        self.compiler_ctx, self.ctx,
        #        OP_CASE, [self.value]
        #    )

        # CaseValue
        return SsbLabelJumpBlueprint(
            self.compiler_ctx, self.ctx,
            OP_CASE_VALUE, [self.operator.value, self.value]
        )

    def add(self, obj: any):
        if isinstance(obj, IntegerLikeCompileHandler):
            # (integer_like[1] | value_of) -> var to set to
            self.value = obj.collect()
            self.value_is_a_variable = False
            return
        if isinstance(obj, ConditionalOperatorCompileHandler):
            self.operator = obj.collect()
            return
        if isinstance(obj, ValueOfCompileHandler):
            self.value = obj.collect()
            self.value_is_a_variable = True
            return

        self._raise_add_error(obj)
