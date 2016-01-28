"""Programs utilities."""  # pylint: disable=missing-docstring


class ProgramCompletionChecker(object):
    """Utility for identifying completed programs.

    Arguments:
        programs (Program QuerySet): Candidates for completion.
        complete_run_modes (list of dict): Serialized representation of
            completed course runs, including the modes in which the runs were
            completed. Expected to be of the form:
            [
                {'course_id': 'foo', 'mode': 'bar'},
                ...
                {'course_id': 'baz', 'mode': 'qux'}
            ]

    Usage:
        >>> completion_checker = utils.ProgramCompletionChecker(programs, complete_run_modes)
        >>> completion_checker.completed_programs
        <list of completed program IDs>
    """
    def __init__(self, programs, complete_run_modes):
        self.programs = programs
        self.complete_run_modes = complete_run_modes

    @property
    def completed_programs(self):
        return [program.id for program in self.programs if self._is_program_complete(program)]

    def _is_program_complete(self, program):
        program_course_codes = program.programcoursecode_set.all()
        is_complete = all(
            [self._is_course_complete(program_course_code) for program_course_code in program_course_codes]
        )

        return is_complete

    def _is_course_complete(self, program_course_code):
        run_modes = program_course_code.run_modes.all()
        is_complete = any([self._serialize_run_mode(run_mode) in self.complete_run_modes for run_mode in run_modes])

        return is_complete

    def _serialize_run_mode(self, run_mode):
        serialized = {
            'course_id': run_mode.course_key,
            'mode': run_mode.mode_slug,
        }

        return serialized
